# code/11_coherence_vs_annealing_three_curves.py
# Coerenza topologica vs cicli di annealing - TRE CURVE
# Stile professionale da rivista scientifica

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ====================== PARAMETRI ======================
cycles = np.arange(0, 13, 1)

# 1. Senza annealing (decadimento esponenziale)
coherence_no = 100 * np.exp(-0.085 * cycles)

# 2. PID Conservativo tradizionale
coherence_cons = 92 + 6 * np.exp(-0.035 * cycles) + 1.5 * np.sin(np.deg2rad(cycles * 40))

# 3. Gain Scheduling Adattivo (migliore)
coherence_gs = 98.5 + 1.2 * np.sin(np.deg2rad(cycles * 55)) * np.exp(-0.008 * cycles)
coherence_gs = np.clip(coherence_gs, 96.8, 99.8)

# ====================== PLOT ======================
fig, ax = plt.subplots(figsize=(10.5, 7), dpi=300)

ax.plot(cycles, coherence_no, color='#d62728', linewidth=3.2, marker='o', 
        label='Senza annealing', markersize=7)
ax.plot(cycles, coherence_cons, color='#1f77b4', linewidth=3.2, marker='s', 
        label='PID Conservativo', markersize=7)
ax.plot(cycles, coherence_gs, color='#2ca02c', linewidth=3.5, marker='D', 
        label='Gain Scheduling Adattivo', markersize=7)

# Soglia accettabile
ax.axhline(y=95, color='gray', linestyle='--', linewidth=1.6, alpha=0.85, 
           label='Soglia minima accettabile (95\%)')

# Annotazioni
ax.annotate('Decadimento rapido', xy=(9, 68), xytext=(6.5, 58),
            arrowprops=dict(arrowstyle='->', color='#d62728'), fontsize=11, color='#d62728')
ax.annotate('Miglior prestazione', xy=(11, 98.2), xytext=(8, 102),
            arrowprops=dict(arrowstyle='->', color='#2ca02c'), fontsize=11, color='#2ca02c')

ax.set_xlabel('Numero di cicli di annealing termico', fontsize=14, labelpad=12)
ax.set_ylabel('Coerenza topologica (\%)', fontsize=14, labelpad=12)

ax.set_xlim(-0.5, 12.5)
ax.set_ylim(50, 105)

ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.grid(True, linestyle=':', alpha=0.65)

ax.tick_params(axis='both', labelsize=12)

ax.legend(loc='upper right', fontsize=12.8, frameon=True, fancybox=True, shadow=False)

plt.title('Coerenza topologica vs cicli di annealing termico\n'
          'Confronto tra strategie di mitigazione della radiazione (GCR + SPE)',
          fontsize=15.5, pad=22, fontweight='medium')

plt.tight_layout()
plt.savefig('figures/coherence_vs_annealing_three_curves.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/coherence_vs_annealing_three_curves.png', dpi=300, bbox_inches='tight')
plt.show()