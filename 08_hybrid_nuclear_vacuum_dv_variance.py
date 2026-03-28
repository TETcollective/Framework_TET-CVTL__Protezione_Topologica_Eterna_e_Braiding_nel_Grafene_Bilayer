import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

print("=== Simulazione Monte Carlo Δv Ibrido NTP/NEP + TET-CVTL (Varianza Coerenza) ===\n")

# ====================== PARAMETRI MISSIONE ======================
mission_duration = 730          # giorni (2 anni)
dt = 1.0                        # passo in giorni
times = np.arange(0, mission_duration + dt, dt)
n_sim = 200                     # numero di traiettorie Monte Carlo

# Massa veicolo di riferimento (Starship cargo-like)
m0 = 150000                     # kg

# ====================== PARAMETRI NTP/NEP (realistici) ======================
thrust_nuclear_peak = 50000     # 50 kN peak
isp_nuclear = 900
duty_cycle_nuclear = 0.00018    # ~0.018% → manovre impulsive brevi

# ====================== PARAMETRI TET-CVTL Vacuum Torque ======================
thrust_vacuum_mean = 0.012      # 12 mN medio (coerente con grafico precedente)
duty_cycle_vac = 0.70

coherence_levels = [0.75, 0.85, 0.92]   # bassa, media, alta (dopo annealing)
colors = ['#d62728', '#ff7f0e', '#2ca02c']
labels = ['Coerenza 75% (bassa)', 'Coerenza 85% (media)', 'Coerenza 92% (alta)']

# ====================== SIMULAZIONE MONTE CARLO ======================
plt.figure(figsize=(12, 7.5), dpi=300)

for idx, coh in enumerate(coherence_levels):
    dv_hybrid_all = np.zeros((n_sim, len(times)))

    for s in range(n_sim):
        mass = float(m0)
        dv = np.zeros_like(times, dtype=float)

        for i in range(1, len(times)):
            dt_sec = dt * 86400.0

            # Contributo Nucleare (impulsive)
            thrust_nuc_eff = thrust_nuclear_peak * duty_cycle_nuclear * 0.90
            dv_nuc_step = (thrust_nuc_eff * dt_sec) / mass

            # Contributo Vacuum Torque con varianza (propellantless)
            noise = 1 + 0.08 * np.random.normal(0, 1)
            thrust_vac_eff = thrust_vacuum_mean * duty_cycle_vac * coh * noise
            dv_vac_step = (thrust_vac_eff * dt_sec) / mass

            dv[i] = dv[i-1] + dv_nuc_step + dv_vac_step

            # Aggiornamento massa (solo nucleare consuma)
            mass_flow_rate = (thrust_nuclear_peak / (isp_nuclear * 9.81)) * duty_cycle_nuclear
            mass -= mass_flow_rate * dt_sec * 0.90

        dv_hybrid_all[s] = dv

    # Statistiche
    dv_mean = np.mean(dv_hybrid_all, axis=0)
    dv_std = np.std(dv_hybrid_all, axis=0)

    # Plot
    plt.plot(times, dv_mean, color=colors[idx], linewidth=3.0, label=labels[idx])
    plt.fill_between(times, dv_mean - dv_std, dv_mean + dv_std,
                     color=colors[idx], alpha=0.18)

# ====================== GRAFICO FINALE ======================
plt.xlabel('Tempo di missione (giorni)', fontsize=14, labelpad=12)
plt.ylabel(r'$Δ v$ cumulativo (m/s)', fontsize=14, labelpad=12)
plt.title(r'Simulazione Monte Carlo $Δ v$ Ibrido: NTP/NEP + Vacuum Torque TET--CVTL' '\n'
          'Confronto tra diversi livelli di coerenza macroscopica (200 traiettorie)',
          fontsize=15, pad=20, fontweight='medium')

ax = plt.gca() # Get the current Axes object
ax.xaxis.set_major_locator(MultipleLocator(100))
ax.yaxis.set_major_locator(MultipleLocator(500))
ax.grid(True, linestyle=':', alpha=0.6)

plt.legend(fontsize=12.5, loc='upper left', frameon=True, fancybox=True)

# Annotazione esempio sul caso migliore
final_mean_high = np.mean(dv_hybrid_all, axis=0)[-1]   # ultima simulazione del loop (alta coerenza)
plt.annotate(f'Coerenza 92%:\n$Δ v$ medio ≈ {final_mean_high:.0f} m/s\n'
             f'(banda di varianza ±1σ)',
             xy=(650, final_mean_high*0.82), xytext=(380, final_mean_high*0.55),
             arrowprops=dict(arrowstyle='->', color='gray', lw=1.5),
             fontsize=11.5, ha='left',
             bbox=dict(boxstyle="round,pad=0.6", facecolor="white", alpha=0.95))

plt.tight_layout()
plt.savefig('figures/hybrid_nuclear_vacuum_dv_variance.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/hybrid_nuclear_vacuum_dv_variance.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nSimulazione Monte Carlo completata con successo.")
print(f"Numero di traiettorie: {n_sim}")
print("Figura salvata come 'figures/hybrid_nuclear_vacuum_dv_variance.pdf/png'")