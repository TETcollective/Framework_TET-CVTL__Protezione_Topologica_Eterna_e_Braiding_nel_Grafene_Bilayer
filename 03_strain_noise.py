# =============================================================================
# 03_strain_noise.py
# Effetto del rumore di strain sul coupling anyonico in un modello toy a due parafermioni
# Stile professionale per il framework TET--CVTL
# =============================================================================

import numpy as np
import qutip as qt
import matplotlib.pyplot as plt
import os

# ====================== PARAMETRI FISICI ======================
N = 3                          # dimensione locale per ogni parafermione (1, τ, leakage)
times = np.linspace(0, 300, 800)   # tempo in unità arbitrarie (cicli di braiding)

# Parametri del sistema
J = 1.0                        # coupling nominale tra parafermioni
eps = 0.15                     # splitting energetico tra canali
V = 0.8                        # ampiezza del drive Floquet
omega_d = 2.0 * np.pi          # frequenza del drive

# Operatori locali
basis = [qt.basis(N, i) for i in range(N)]
idN = qt.qeye(N) # Renamed id3 to idN for clarity and consistency with N

# Local parafermionic lowering operator (e.g., standard annihilation operator)
alpha_local = qt.destroy(N)

alpha1 = qt.tensor(alpha_local, idN)      # operatore lowering per parafermione 1
alpha2 = qt.tensor(idN, alpha_local)      # operatore lowering per parafermione 2

# Operatore proxy del torque chiral (gravitomagnetico analogico)
# Ensure both parts of the tensor product are operators for N-level systems
# Replaced qt.sigmaz() with a compatible N-level operator (e.g., idN or a custom one)
Op_tau_grav = qt.tensor(basis[1]*basis[1].dag() - basis[0]*basis[0].dag(),
                        idN) * 0.5 # Using idN for dimensional consistency

# Stato iniziale
psi0 = qt.tensor(basis[0], basis[0])   # entrambi nel canale triviale

# Operatori di dissipazione (Lindblad)
gamma_th = 0.008               # poisoning termico
gamma_leak = 0.0008            # leakage
gamma_deph = 0.012             # decoerenza di fase

c_ops = [
    np.sqrt(gamma_th) * qt.tensor(basis[0]*basis[1].dag(), idN),   # poisoning
    np.sqrt(gamma_leak) * qt.tensor(basis[1]*basis[0].dag(), idN), # leakage 1
    np.sqrt(gamma_leak) * qt.tensor(idN, basis[1]*basis[0].dag()), # leakage 2
    # Dephasing operators must also be for N-level systems, replaced qt.sigmaz()
    np.sqrt(gamma_deph) * qt.tensor(basis[0]*basis[0].dag() - basis[1]*basis[1].dag(), idN),             # dephasing 1
    np.sqrt(gamma_deph) * qt.tensor(idN, basis[0]*basis[0].dag() - basis[1]*basis[1].dag())              # dephasing 2
]

# ====================== RUMORE DI STRAIN ======================
sigma_strain = 0.015           # rms strain (1.5%)
m_strain = 0.8                 # modulazione massima dello strain

np.random.seed(42)             # riproducibilità
strain_noise = np.random.normal(0, sigma_strain, len(times))

def J_t(t, args):
    """Coupling J(t) con rumore di strain"""
    idx = np.argmin(np.abs(times - t))
    return J * (1 + m_strain * strain_noise[idx])

# Function for J(t) without strain noise
def J_t_clean(t, args):
    """Coupling J(t) senza rumore di strain"""
    return J

# ====================== HAMILTONIANO CON RUMORE ======================
def H_t_noisy(t, args):
    J_current = J_t(t, args)

    # Hamiltoniano di interazione anyonica con coupling noisy
    H0_noisy = J_current * (alpha1.dag() * alpha2 + alpha1 * alpha2.dag())

    # Termini di splitting energetico
    H0_noisy += eps * (qt.tensor(basis[1]*basis[1].dag() + 2*basis[2]*basis[2].dag(), idN) +
                       qt.tensor(idN, basis[1]*basis[1].dag() + 2*basis[2]*basis[2].dag()))

    # Drive Floquet
    drive = V * np.cos(omega_d * t) * (alpha1 + alpha1.dag() + alpha2 + alpha2.dag())

    return H0_noisy + drive

def H_t_clean(t, args):
    J_current = J_t_clean(t, args) # Use the clean J_t function

    # Hamiltoniano di interazione anyonica con coupling clean
    H0_clean = J_current * (alpha1.dag() * alpha2 + alpha1 * alpha2.dag())

    # Termini di splitting energetico
    H0_clean += eps * (qt.tensor(basis[1]*basis[1].dag() + 2*basis[2]*basis[2].dag(), idN) +
                       qt.tensor(idN, basis[1]*basis[1].dag() + 2*basis[2]*basis[2].dag()))

    # Drive Floquet
    drive = V * np.cos(omega_d * t) * (alpha1 + alpha1.dag() + alpha2 + alpha2.dag())

    return H0_clean + drive

# ====================== SIMULAZIONE ======================
print("Esecuzione simulazione senza rumore di strain...")
result_clean = qt.mesolve(H_t_clean, # Use the explicitly clean Hamiltonian function
                          psi0, times, c_ops=c_ops, e_ops=[Op_tau_grav], options=qt.Options(store_states=True))

print("Esecuzione simulazione con rumore di strain...")
result_noisy = qt.mesolve(H_t_noisy, psi0, times, c_ops=c_ops, e_ops=[Op_tau_grav], options=qt.Options(store_states=True))

# ====================== PLOT ======================
expect_clean = qt.expect(Op_tau_grav, result_clean.states)
expect_noisy = qt.expect(Op_tau_grav, result_noisy.states)

plt.figure(figsize=(11, 7), dpi=300)

plt.plot(times, expect_clean, color='#1f77b4', linewidth=3.0,
         label='Senza strain noise')
plt.plot(times, expect_noisy, color='#d62728', linewidth=2.8, alpha=0.9,
         label=r'Con strain noise ($\sigma=1.5\%$)') # Fixed SyntaxWarning with raw string

plt.xlabel('Tempo (unità arbitrarie / cicli di braiding)', fontsize=14)
plt.ylabel(r'$\langle \tau_{\text{proxy}} \rangle$ (Torque chiral)', fontsize=14)
plt.title('Effetto del rumore di strain sul Torque Chiral\n'
          'Modello toy a due parafermioni Fibonacci', fontsize=15, pad=20)

plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=12.5, loc='lower right')

plt.tight_layout()

# Create 'figures' directory if it doesn't exist
os.makedirs('figures', exist_ok=True)

plt.savefig('figures/strain_noise_effect_on_torque.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/strain_noise_effect_on_torque.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nFigura salvata come 'figures/strain_noise_effect_on_torque.pdf'")
print("Simulazione completata con successo.")