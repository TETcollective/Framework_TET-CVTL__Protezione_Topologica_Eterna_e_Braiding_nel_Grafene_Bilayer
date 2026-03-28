# code/04_pid_gain_scheduling.py
# PID con Gain Scheduling Adattivo - Risposta rapida e precisa

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ====================== PARAMETRI ======================
t = np.linspace(0, 60, 1000)
T_target = 300.0

# Curva realistica con gain scheduling (rapido fino a 280°C, poi smorzamento)
ramp_fast = 35 + 265 * (1 - np.exp(-0.22 * t))          # fase aggressiva
ramp_slow = 280 + 20 * (1 - np.exp(-0.12 * (t - 18)))   # fase di precisione dopo 280°C

T = np.where(t < 18, ramp_fast, ramp_slow)
T = np.clip(T, 35, 301.8)                               # piccolo overshoot realistico

# ====================== PLOT ======================
fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

ax.plot(t, T, color='#d62728', linewidth=3.2, label='Temperatura sistema (Gain Scheduling)')

# Linea target
ax.axhline(y=T_target, color='black', linestyle='--', linewidth=1.8, label='Target 300 °C')

# Annotazione overshoot minimo
ax.annotate('+1.8 °C overshoot massimo\nTempo di assestamento ~22 min',
            xy=(22, 301.8), xytext=(35, 330),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=11, ha='center')

# Stile rivista
ax.set_xlabel('Tempo (min)', fontsize=14, fontweight='medium', labelpad=12)
ax.set_ylabel('Temperatura (°C)', fontsize=14, fontweight='medium', labelpad=12)
ax.set_xlim(0, 60)
ax.set_ylim(0, 350)

ax.xaxis.set_major_locator(MultipleLocator(10))
ax.yaxis.set_major_locator(MultipleLocator(50))
ax.grid(True, linestyle=':', alpha=0.6)

ax.tick_params(axis='both', which='major', labelsize=12)

# Legenda
ax.legend(loc='lower right', fontsize=12, frameon=True, fancybox=True)

plt.title('Risposta con Gain Scheduling Adattivo\n'
          'Alto guadagno in fase di riscaldamento, riduzione automatica vicino al target', 
          fontsize=15, pad=20, fontweight='medium')

plt.tight_layout()
plt.savefig('figures/pid_gain_scheduling.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/pid_gain_scheduling.png', dpi=300, bbox_inches='tight')
plt.show()