# =============================================================================
# 08_hybrid_nuclear_vacuum_dv.py   → VERSIONE FINALE PER IL PAPER
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

print("=== TET-CVTL Hybrid Δv Simulation - Final Paper Version ===\n")

mission_duration = 730
dt = 1.0
times = np.arange(0, mission_duration + dt, dt)

m0 = 150000                     # kg Starship cargo-like

# NTP/NEP - REALISTICO
thrust_nuclear_peak = 50000     # 50 kN
isp_nuclear = 900
duty_cycle_nuclear = 0.00018    # ~0.018% → circa 3.15 ore totali di firing in 2 anni

# TET-CVTL Vacuum Torque (array 5–10 m²)
thrust_vacuum_mean = 0.012      # 12 mN medio
duty_cycle_vac = 0.70
coherence_efficiency = 0.90

dv_nuclear = np.zeros_like(times, dtype=float)
dv_vacuum  = np.zeros_like(times, dtype=float)
dv_hybrid  = np.zeros_like(times, dtype=float)

mass = float(m0)

for i in range(1, len(times)):
    dt_sec = dt * 86400.0
    
    # Nuclear impulsive
    thrust_nuc_eff = thrust_nuclear_peak * duty_cycle_nuclear * 0.90
    dv_nuc_step = (thrust_nuc_eff * dt_sec) / mass
    dv_nuclear[i] = dv_nuclear[i-1] + dv_nuc_step
    
    # Vacuum persistent propellantless
    thrust_vac_eff = thrust_vacuum_mean * duty_cycle_vac * coherence_efficiency
    dv_vac_step = (thrust_vac_eff * dt_sec) / mass
    dv_vacuum[i] = dv_vacuum[i-1] + dv_vac_step
    
    dv_hybrid[i] = dv_hybrid[i-1] + dv_nuc_step + dv_vac_step
    
    # Mass update only for nuclear
    mass_flow_rate = (thrust_nuclear_peak / (isp_nuclear * 9.81)) * duty_cycle_nuclear
    mass -= mass_flow_rate * dt_sec * 0.90

# ====================== RISULTATI ======================
print(f"Δv solo NTP/NEP dopo 2 anni : {dv_nuclear[-1]:.0f} m/s")
print(f"Δv solo Vacuum Torque       : {dv_vacuum[-1]:.2f} m/s")
print(f"Δv totale ibrido            : {dv_hybrid[-1]:.0f} m/s")
print(f"Contributo vacuum torque    : {dv_vacuum[-1]/dv_hybrid[-1]*100:.3f} %")
print(f"Massa finale veicolo        : {mass:.0f} kg")
print(f"Propellente nucleare consumato: {m0 - mass:.0f} kg\n")

# ====================== PLOT ======================
fig, ax = plt.subplots(figsize=(11, 7), dpi=300)

ax.plot(times, dv_nuclear, color='#1f77b4', lw=3, label='Solo NTP/NEP')
ax.plot(times, dv_vacuum,  color='#ff7f0e', lw=2.8, label='Solo Vacuum Torque TET--CVTL')
ax.plot(times, dv_hybrid,  color='#2ca02c', lw=3.5, label='Ibrido NTP/NEP + TET--CVTL')

ax.set_xlabel('Tempo di missione (giorni)', fontsize=14, labelpad=12)
ax.set_ylabel(r'$\Delta v$ cumulativo (m/s)', fontsize=14, labelpad=12)
ax.set_title(r'Simulazione $\Delta v$ Ibrido: Propulsione Nucleare + Vacuum Torque TET--CVTL' '\n'
             'Missione di 2 anni (annealing adattivo e mitigazione radiativa)',
             fontsize=15, pad=20)

ax.xaxis.set_major_locator(MultipleLocator(100))
ax.yaxis.set_major_locator(MultipleLocator(500))
ax.grid(True, linestyle=':', alpha=0.6)

ax.legend(fontsize=12.5, loc='upper left')

final_hybrid = dv_hybrid[-1]
ax.annotate(f'$\Delta v$ totale ibrido: {final_hybrid:.0f} m/s\n'
            f'(contributo vacuum: {dv_vacuum[-1]:.2f} m/s)',
            xy=(650, final_hybrid*0.85), xytext=(380, final_hybrid*0.58),
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.5),
            fontsize=12, ha='left',
            bbox=dict(boxstyle="round,pad=0.6", facecolor="white", alpha=0.95))

plt.tight_layout()
plt.savefig('figures/hybrid_nuclear_vacuum_dv.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/hybrid_nuclear_vacuum_dv.png', dpi=300, bbox_inches='tight')
plt.show()