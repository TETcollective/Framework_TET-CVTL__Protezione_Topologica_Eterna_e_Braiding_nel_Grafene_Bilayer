# code/03_pid_no_overshoot.py
# PID conservativo - Risposta senza overshoot (stile rivista scientifica)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ====================== PARAMETRI ======================
t = np.linspace(0, 60, 1000)                    # tempo in minuti
T_target = 300.0                                # target temperature °C

# Curva realistica PID conservativo (no overshoot)
T = 35 + (T_target - 35) * (1 - np.exp(-0.085 * t)) * (1 - 0.12 * np.exp(-0.15 * t))

# ====================== PLOT ======================
fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

ax.plot(t, T, color='#1f77b4', linewidth=3.2, label='Temperatura sistema')

# Linea target
ax.axhline(y=T_target, color='black', linestyle='--', linewidth=1.8, label='Target 300 °C')

# Annotazioni
ax.annotate('Assestamento entro ±0.3 °C dopo ~45 min',
            xy=(48, 298), xytext=(35, 260),
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
ax.legend(loc='lower right', fontsize=12, frameon=True, fancybox=True, shadow=False)

plt.title('Risposta PID Conservativo – Senza Overshoot\n'
          'Tuning: $K_p=2.8$, $K_i=0.12$, $K_d=25$', 
          fontsize=15, pad=20, fontweight='medium')

plt.tight_layout()
plt.savefig('figures/pid_no_overshoot.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/pid_no_overshoot.png', dpi=300, bbox_inches='tight')
plt.show()