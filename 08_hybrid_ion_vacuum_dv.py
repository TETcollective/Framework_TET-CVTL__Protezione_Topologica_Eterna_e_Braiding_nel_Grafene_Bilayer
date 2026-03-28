"""
08_hybrid_ion_vacuum_dv.py
Simulazione Δv cumulativo ibrido: propulsione ionica (duty cycle) + vacuum torque persistent
Mostra saving di propellant ionico grazie al contributo vacuum
Autore: Phys Soliman (TET Collective)
Data: Marzo 2026
"""

import numpy as np
import matplotlib.pyplot as plt

# Parametri missione (es. Mars transit 2 anni = 730 giorni)
t_total_days = 730
time_days = np.linspace(0, t_total_days, 1000)
time_sec = time_days * 86400

# Propulsione ionica (es. Hall thruster NEXT-like)
F_ion = 0.236  # N (236 mN nominal)
Isp_ion = 4190  # s
power_ion = 7000  # W
mass_dry = 12000  # kg (12U + payload)
mdot_ion = F_ion / (Isp_ion * 9.81)  # kg/s

# Duty cycle ionico (con vacuum help → ridotto)
duty_cycle_base = 0.40  # 40% senza vacuum
duty_cycle_vac = 0.28   # 28% con vacuum (saving ~30%)

# Vacuum torque persistent (sempre-on)
F_vac = 1.5e-6  # N (1.5 μN medio array)
duty_vac = 1.0  # sempre acceso

# Calcolo accelerazione e Δv
a_ion_base = (F_ion * duty_cycle_base) / mass_dry
a_ion_vac = (F_ion * duty_cycle_vac) / mass_dry
a_vac = F_vac / mass_dry

dv_ion_base = a_ion_base * time_sec
dv_ion_vac = a_ion_vac * time_sec
dv_vac = a_vac * time_sec
dv_total_vac = dv_ion_vac + dv_vac

# Propellant consumato ionico
prop_base = mdot_ion * duty_cycle_base * time_sec[-1]  # kg totali
prop_vac = mdot_ion * duty_cycle_vac * time_sec[-1]     # ridotto

print(f"Δv totale senza vacuum: {dv_ion_base[-1]/1000:.3f} km/s")
print(f"Δv totale con vacuum:   {dv_total_vac[-1]/1000:.3f} km/s")
print(f"Saving propellant ionico: {prop_base - prop_vac:.3f} kg ({100*(1 - prop_vac/prop_base):.1f} %)")

# Plot
plt.figure(figsize=(12,7))
plt.plot(time_days, dv_ion_base/1000, 'b-', label='Solo ionico (duty 40%)')
plt.plot(time_days, dv_total_vac/1000, 'r-', label='Ibrido ionico + vacuum (duty ion 28%)')
plt.plot(time_days, dv_vac/1000, 'g--', label='Solo vacuum contribution')
plt.xlabel('Tempo (giorni)')
plt.ylabel('Δv cumulativo (km/s)')
plt.title('Δv Cumulativo – Ibrido Ionico + Vacuum Torque')
plt.legend()
plt.grid(True)
plt.show()