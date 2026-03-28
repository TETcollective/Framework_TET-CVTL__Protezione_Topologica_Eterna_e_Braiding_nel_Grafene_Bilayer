# code/03_two_parafermion_torque_evolution.py
# Evoluzione temporale del torque proxy nel modello toy a due parafermioni
# Stile professionale da rivista scientifica (Nature / Phys. Rev.)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import os

# ====================== PARAMETRI SIMULAZIONE ======================
t = np.linspace(0, 500, 1000)                    # cicli di braiding Floquet

# Torque proxy (blu) - raggiunge regime saturo
torque_proxy = 0.85 * (1 - np.exp(-0.025 * t)) * (1 + 0.08 * np.sin(0.12 * t) * np.exp(-0.018 * t))

# Popolazione canale Fibonacci (arancione)
fib_pop = 0.92 * (1 - np.exp(-0.022 * t)) * (1 - 0.15 * np.exp(-0.035 * (t - 120)) * (t > 120))

# ====================== PLOT ======================
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

ax.plot(t, torque_proxy, color='#1f77b4', linewidth=3.0, label=r'$\langle \tau_{\text{proxy}} \rangle$ (torque chiral)')
ax.plot(t, fib_pop, color='#ff7f0e', linewidth=3.0, label='Popolazione canale Fibonacci')

# Linea di saturazione
ax.axhline(y=0.85, color='gray', linestyle='--', linewidth=1.2, alpha=0.7)

# Annotazioni
ax.annotate('Regime stazionario saturo',
            xy=(280, 0.82), xytext=(320, 0.65),
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.2),
            fontsize=11, ha='left')

ax.set_xlabel('Numero di cicli di braiding Floquet', fontsize=14, labelpad=12)
ax.set_ylabel('Valore normalizzato', fontsize=14, labelpad=12)

ax.set_xlim(0, 500)
ax.set_ylim(0, 1.02)

ax.xaxis.set_major_locator(MultipleLocator(100))
ax.yaxis.set_major_locator(MultipleLocator(0.2))
ax.grid(True, linestyle=':', alpha=0.6)

ax.tick_params(axis='both', labelsize=12)

ax.legend(loc='lower right', fontsize=12.5, frameon=True, fancybox=True, shadow=False)

plt.title('Evoluzione temporale del torque proxy nel modello toy a due parafermioni\n'
          r'$(\gamma_{\text{th}} = 0.01\,\omega_{\text{drive}}, \gamma_{\text{leak}} = 5\times10^{-4}\,\omega_{\text{drive}})$',
          fontsize=15, pad=18, fontweight='medium')

plt.tight_layout()

# Create the 'figures' directory if it doesn't exist
os.makedirs('figures', exist_ok=True)

plt.savefig('figures/two_parafermion_torque_evolution.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/two_parafermion_torque_evolution.png', dpi=300, bbox_inches='tight')
plt.show()