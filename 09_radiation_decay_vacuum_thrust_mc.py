"""
09_radiation_decay_vacuum_thrust_mc.py
Simulazione Monte Carlo del decadimento thrust vacuum torque dovuto a radiazione
con annealing ciclico + variabilità stocastica
Autore: Phys Soliman (TET Collective)
Data: Marzo 2026
"""

import numpy as np
import matplotlib.pyplot as plt

# Parametri missione (2 anni = 730 giorni)
days_total = 730
time_days = np.arange(0, days_total + 1)
n_sim = 200  # numero realizzazioni Monte Carlo

# Baseline thrust vacuum (senza decay)
F0 = 1.5e-6  # N (1.5 μN nominal)

# Parametri radiazione
dose_per_day = 40  # rad/giorno (GCR cruise)
decay_rate_per_krad = 0.008  # frazione coerenza persa per krad (0.8%/krad)

# Annealing: ogni 120 giorni, recovery 70% della perdita accumulata
anneal_interval = 120
recovery_fraction = 0.70

# Noise stocastico (variabilità dose e recovery)
sigma_dose = 5.0      # rad/giorno std
sigma_recovery = 0.08  # variabilità recovery

# Array per salvare tutte le traiettorie
thrust_trajectories = np.zeros((n_sim, len(time_days)))

for sim in range(n_sim):
    coherence = 1.0  # iniziale 100%
    thrust = np.zeros(len(time_days))
    thrust[0] = F0
    
    for d in range(1, len(time_days)):
        # Dose giornaliera stocastica
        dose_today = np.random.normal(dose_per_day, sigma_dose)
        dose_krad = dose_today / 1000
        
        # Decadimento proporzionale a dose
        loss = decay_rate_per_krad * dose_krad
        coherence *= (1 - loss)
        
        # Annealing ciclico
        if d % anneal_interval == 0:
            recovered = recovery_fraction * (1 - coherence)  # recupera % della perdita
            recovered *= np.random.normal(1.0, sigma_recovery)  # noise
            coherence += recovered
            coherence = min(coherence, 1.0)
        
        thrust[d] = F0 * coherence
    
    thrust_trajectories[sim, :] = thrust

# Statistiche
thrust_mean = np.mean(thrust_trajectories, axis=0)
thrust_std = np.std(thrust_trajectories, axis=0)
thrust_p10 = np.percentile(thrust_trajectories, 10, axis=0)
thrust_p90 = np.percentile(thrust_trajectories, 90, axis=0)

# Plot
plt.figure(figsize=(12,7))
plt.plot(time_days, thrust_mean * 1e6, 'b-', label='Thrust medio (μN)')
plt.fill_between(time_days, (thrust_mean - thrust_std)*1e6, (thrust_mean + thrust_std)*1e6,
                 color='b', alpha=0.2, label='±1σ')
plt.fill_between(time_days, thrust_p10*1e6, thrust_p90*1e6,
                 color='gray', alpha=0.15, label='10–90 percentile')
plt.axhline(F0*1e6, color='r', linestyle='--', label='Baseline senza decay')
plt.xlabel('Tempo (giorni)')
plt.ylabel('Thrust vacuum torque (μN)')
plt.title('Decadimento Thrust Vacuum Torque da Radiazione + Annealing (Monte Carlo)')
plt.legend()
plt.grid(True)
plt.show()

print(f"Thrust finale medio: {thrust_mean[-1]*1e6:.3f} ± {thrust_std[-1]*1e6:.3f} μN")
print(f"Retention coerenza media finale: {thrust_mean[-1]/F0*100:.1f} %")