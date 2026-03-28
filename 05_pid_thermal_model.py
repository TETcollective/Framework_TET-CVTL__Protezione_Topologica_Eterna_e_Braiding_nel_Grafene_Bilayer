"""
05_pid_thermal_model.py
Simulazione PID per controllo temperatura annealing (300 °C target)
Autore: Phys Soliman (TET Collective)
Data: Marzo 2026
"""

import numpy as np
import matplotlib.pyplot as plt

# Parametri fisici
C = 120.0       # capacità termica J/K
k_loss = 0.05   # costante perdita termica W/K
P_max = 12.0    # potenza massima heater W
T_amb = 30.0    # temperatura ambiente °C
T_set = 300.0   # target °C

# Parametri PID (moderati)
Kp = 2.1
Ki = 0.002      # scalato per dt=1 s
Kd = 16.0

# Tempo simulazione
dt = 1.0        # s
t_total = 4*3600  # 4 ore
n_steps = int(t_total / dt)
time = np.arange(0, t_total, dt)

# Inizializzazione
T = np.zeros(n_steps)
T[0] = T_amb
integral = 0.0
prev_error = T_set - T[0]
P_history = np.zeros(n_steps)

for i in range(1, n_steps):
    error = T_set - T[i-1]
    integral += error * dt
    derivative = (error - prev_error) / dt
    
    P = Kp * error + Ki * integral + Kd * derivative
    P = np.clip(P, 0, P_max)  # saturation
    
    # Dinamica termica
    dT_dt = (P - k_loss * (T[i-1] - T_amb)) / C
    T[i] = T[i-1] + dT_dt * dt
    
    P_history[i] = P
    prev_error = error

# Plot
fig, ax1 = plt.subplots(figsize=(12,6))

ax1.plot(time/60, T, 'b-', label='Temperatura (°C)')
ax1.axhline(T_set, color='r', linestyle='--', label='Target 300 °C')
ax1.set_xlabel('Tempo (min)')
ax1.set_ylabel('Temperatura (°C)', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.legend(loc='upper left')

ax2 = ax1.twinx()
ax2.plot(time/60, P_history, 'g-', label='Potenza heater (W)')
ax2.set_ylabel('Potenza (W)', color='g')
ax2.tick_params(axis='y', labelcolor='g')
ax2.legend(loc='upper right')

plt.title('Simulazione PID Annealing – Moderate Gains')
plt.grid(True)
plt.show()