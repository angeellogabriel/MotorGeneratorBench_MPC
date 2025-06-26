# 🎯 Controle Preditivo em Tempo Real - Bancada Motor-Gerador

Este projeto implementa um controlador preditivo baseado em modelo (MPC) aplicado a uma bancada motor-gerador real, com o objetivo de manter a resposta do sistema próxima de um setpoint mesmo em presença de perturbações físicas externas.

## ⚙️ Tecnologias e Ferramentas

- Python 3
- OpenCV (para gráfico em tempo real)
- `cvxpy` para otimização no MPC
- `pyserial` para comunicação com a bancada
- Notebook com Arduino/driver PWM
- Bancada física motor-gerador (desenvolvida em laboratório)

## 🧪 Etapas do Projeto

1. **Coleta de dados com PRBS**
2. **Identificação de modelo ARX**
3. **Implementação do controlador MPC**
4. **Variação de referência (setpoint)**
5. **Teste com interferência física (frear eixo com o dedo)**
6. **Cálculo de métricas de desempenho**

## 📊 Resultados

- IAE: 413.71
- ISE: 880.14
- ITAE: 3188.29
- Energia do Controle: 14470.55

<p align="center">
  <img src="images/grafico_mpc.png" width="600">
</p>

## 📸 Fotos da bancada

<p align="center">
  <img src="images/bancada_real.jpg" width="500">
</p>

## 📂 Organização do Código

- `modelo_identificado.py`: identificação do modelo via PRBS
- `mpc_controle.py`: implementação do MPC com setpoint variável e restrições
- `salvar_csv.py`: coleta e exportação dos dados
- `dados/`: dados de entrada/saída
- `resultados/`: métricas de desempenho

## 👨‍🔧 Autor

Projeto desenvolvido por [Seu Nome] durante experimentos com controle em tempo real.

## 📎 Contato

- [LinkedIn](https://linkedin.com/in/seuusuario)
- [GitHub](https://github.com/seuusuario)
