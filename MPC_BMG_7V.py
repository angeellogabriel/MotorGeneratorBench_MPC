import numpy as np
import cvxpy as cp
import serial
import time
import matplotlib.pyplot as plt

# Modelo identificado
a = 0.7266
b = 0.3002
c = -0.4931
delta_u_max = 0.2  # limite máximo de variação por passo

# MPC
N = 10
lambda_u = 0.1
u_min = 3.0
u_max = 6.0

# Inicializações
y_k = 0
u_k_prev = 4.5
Ts = 0.03
max_iter = 500  # 500*0.03 ≈ 15s

# Comunicação serial
conexao = serial.Serial(port='COM5', baudrate=9600, timeout=0.01)
time.sleep(1)

# Gráficos
# Gráficos
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

# Controle
line1, = ax1.plot([], [], label='Controle (u)')
ax1.legend()
ax1.set_ylim([2.5, 6.5])
ax1.set_ylabel('u')
ax1.set_title('Controle MPC')

# Saída + setpoint
line2, = ax2.plot([], [], label='Saída (y)', color='orange')
line3, = ax2.plot([], [], label='Setpoint (r)', color='red', linestyle='--')
ax2.legend()
ax2.set_ylim([0, 7.5])
ax2.set_ylabel('y')
ax2.set_xlabel('Tempo (s)')
ax2.set_title('Resposta do Sistema')

# Armazenamento
tempo = []
us = []
ys = []
rs = []


for k in range(max_iter):
    t0 = time.time()
    t_atual = k * Ts

    # Setpoint variável
    if t_atual < 5:
        r = 4.0
    elif t_atual < 10:
        r = 3.0
    else:
        r = 4.5

    # Leitura
    if conexao.inWaiting() > 0:
        try:
            y_lido = float(conexao.readline().decode().strip())
            y_k = y_lido
        except:
            pass

    # MPC via cvxpy
    u = cp.Variable(N)
    y = cp.Variable(N+1)
    cost = 0
    constraints = [y[0] == y_k]

    for i in range(N):
        if i == 0:
            delta_u = u[i] - u_k_prev
        else:
            delta_u = u[i] - u[i-1]
        cost += cp.square(y[i+1] - r) + lambda_u * cp.square(delta_u)
        constraints += [cp.abs(delta_u) <= delta_u_max]

        constraints += [y[i+1] == a * y[i] + b * u[i] + c]
        constraints += [u[i] >= u_min, u[i] <= u_max]

    prob = cp.Problem(cp.Minimize(cost), constraints)
    prob.solve()

    u_aplicado = u.value[0]
    u_k_prev = u_aplicado
    pwm = int(u_aplicado * 255 / 7)
    conexao.write(str(pwm).encode())

    # Armazena
    us.append(u_aplicado)
    ys.append(y_k)
    tempo.append(t_atual)
    rs.append(r)

    # Atualiza gráfico
    line1.set_data(tempo, us)
    line2.set_data(tempo, ys)
    line3.set_data(tempo, rs)
    ax1.relim()
    ax2.relim()
    ax1.autoscale_view()
    ax2.autoscale_view()
    plt.draw()
    plt.pause(0.001)

    while time.time() - t0 < Ts:
        time.sleep(0.001)

# Finaliza
conexao.write(str(0).encode())
conexao.close()
plt.ioff()
plt.show()
import numpy as np

erro = np.abs(np.array(rs) - np.array(ys))
erro2 = (np.array(rs) - np.array(ys))**2
tempo_np = np.array(tempo)
u_np = np.array(us)

iae = np.sum(erro)
ise = np.sum(erro2)
itae = np.sum(tempo_np * erro)
energia_u = np.sum(u_np**2)

print('\n🔍 Métricas de Desempenho:')
print(f'IAE  = {iae:.2f}')
print(f'ISE  = {ise:.2f}')
print(f'ITAE = {itae:.2f}')
print(f'Energia do Controle (∑u²) = {energia_u:.2f}')

