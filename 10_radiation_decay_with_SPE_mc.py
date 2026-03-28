"""
10_radiation_decay_with_SPE_mc.py
Monte Carlo decadimento thrust vacuum torque con radiazione GCR + eventi SPE (spike dose)
Includi annealing ciclico e variabilità stocastica
Autore: Phys Soliman (TET Collective)
Data: Marzo 2026
"""

import numpy as np
import matplotlib.pyplot as plt

# Parametri missione
days_total = 730
time_days = np.arange(0, days_total + 1)
n_sim = 300  # realizzazioni MC

# Baseline
F0 = 1.5e-6  # N

# GCR baseline
dose_gcr_day = 40.0  # rad/giorno
sigma_gcr = 6.0

# SPE events: Poisson process, 0–3 eventi/anno, dose spike 100–1000 rad per evento
spe_rate_year = 1.5  # media eventi SPE significativi per anno
spe_rate_day = spe_rate_year / 365
spe_dose_mean = 400  # rad per evento medio
spe_dose_sigma = 200

# Decay rate
decay_per_krad = 0.008  # frazione perdita coerenza per krad

# Annealing
anneal_interval = 120  # giorni
recovery_frac = 0.70
sigma_recovery = 0.08

# Array risultati
thrust_mc = np.zeros((n_sim, len(time_days)))

for sim in range(n_sim):
    coherence = 1.0
    thrust = np.zeros(len(time_days))
    thrust[0] = F0
    
    for d in range(1, len(time_days)):
        # Dose GCR
        dose_today = np.random.normal(dose_gcr_day, sigma_gcr)
        
        # SPE spike (Poisson)
        spe_today = np.random.poisson(spe_rate_day)
        if spe_today > 0:
            dose_spe = np.random.normal(spe_dose_mean, spe_dose_sigma, spe_today)
            dose_today += np.sum(dose_spe)
        
        dose_krad = dose_today / 1000
        loss = decay_per_krad * dose_krad
        coherence *= (1 - loss)
        
        # Annealing ciclico
        if d % anneal_interval == 0:
            recovered = recovery_frac * (1 - coherence)
            recovered *= np.random.normal(1.0, sigma_recovery)
            coherence += recovered
            coherence = min(coherence, 1.0)
        
        thrust[d] = F0 * coherence
    
    thrust_mc[sim, :] = thrust

# Statistiche
mean_thrust = np.mean(thrust_mc, axis=0)
std_thrust = np.std(thrust_mc, axis=0)
p10 = np.percentile(thrust_mc, 10, axis=0)
p90 = np.percentile(thrust_mc, 90, axis=0)

# Plot
plt.figure(figsize=(12,7))
plt.plot(time_days, mean_thrust * 1e6, 'b-', label='Thrust medio (μN)')
plt.fill_between(time_days, (mean_thrust - std_thrust)*1e6, (mean_thrust + std_thrust)*1e6,
                 color='b', alpha=0.2)
plt.fill_between(time_days, p10*1e6, p90*1e6, color='gray', alpha=0.15, label='10–90 perc.')
plt.axhline(F0*1e6, color='r', linestyle='--', label='Baseline')
plt.xlabel('Tempo (giorni)')
plt.ylabel('Thrust (μN)')
plt.title('Decadimento Thrust Vacuum Torque – GCR + SPE Events (Monte Carlo)')
plt.legend()
plt.grid(True)
plt.show()

print(f"Thrust finale medio: {mean_thrust[-1]*1e6:.3f} ± {std_thrust[-1]*1e6:.3f} μN")
print(f"Retention coerenza finale media: {mean_thrust[-1]/F0*100:.1f} %")