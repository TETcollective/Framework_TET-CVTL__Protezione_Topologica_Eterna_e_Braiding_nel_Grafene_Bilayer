"""
06_full_multi_site_strain_negativity.py
Modello ladder a 4 parafermioni Z3 con strain noise dinamico
Calcolo negativity multi-pair (tutte le coppie distanti) e coherence proxy
Autore: Phys Soliman (TET Collective)
Data: Marzo 2026
"""

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
from qutip import entropy_vn, negativity, ptrace, expect

# Parametri globali
N = 3           # Z3 per sito
n_sites = 4     # numero siti ladder
dim = N ** n_sites  # 81

# Operatori parafermionici (clock shift) per ogni sito
def para_op(site):
    ops = [qt.qeye(N)] * n_sites
    ops[site] = qt.Qobj(np.array([[0,0,1],[1,0,0],[0,1,0]], dtype=complex))
    return qt.tensor(ops)

alpha = [para_op(i) for i in range(n_sites)]

# Hamiltoniano base: hopping nearest-neighbor + splitting
J_nom = 0.30
eps = 0.08
H0 = eps * sum(qt.tensor([qt.qeye(N)]*i + [qt.basis(N,1)*qt.basis(N,1).dag() + 2*qt.basis(N,2)*qt.basis(N,2).dag()] + [qt.qeye(N)]*(n_sites-1-i)) for i in range(n_sites))

hop_terms = []
for i in range(n_sites-1):
    hop_terms.append(J_nom * (alpha[i].dag() * alpha[i+1] + alpha[i] * alpha[i+1].dag()))

H0 += sum(hop_terms)

# Floquet drive su tutti i siti
V = 0.25
omega_d = 2 * np.pi * 3.0

# Strain noise: fluttuazioni gaussiane su ogni coupling J_i(t)
np.random.seed(42)
sigma_strain = 0.018  # rms strain %
n_steps = 8000
times = np.linspace(0, 200, n_steps)
strain_noise = np.random.normal(0, sigma_strain, (n_sites-1, n_steps))  # uno per ogni bond

def H_t(t, args):
    idx = np.argmin(np.abs(times - t))
    H_drive = V * np.cos(omega_d * t) * sum(alpha[i] + alpha[i].dag() for i in range(n_sites))
    
    H_hop = 0
    for i in range(n_sites-1):
        J_current = J_nom * (1 + 0.8 * strain_noise[i, idx])  # sensitivity m_strain=0.8
        H_hop += J_current * (alpha[i].dag() * alpha[i+1] + alpha[i] * alpha[i+1].dag())
    
    return H0 + H_hop + H_drive

# Lindblad (poisoning nearest-neighbor + leak globale vacuum)
gamma_poison = 0.012
gamma_leak = 0.006
c_ops = [np.sqrt(gamma_poison) * (alpha[i] - alpha[i+1]) for i in range(n_sites-1)]
c_ops.append(np.sqrt(gamma_leak) * qt.tensor([qt.basis(N,0)*qt.basis(N,0).dag()]*n_sites))

# Osservabile torque proxy (chiral tra estremi)
Op_tau = 1j * (alpha[0].dag() * alpha[-1] - alpha[0] * alpha[-1].dag())

# Stato iniziale GHZ-like per massimizzare long-range entanglement
ghz_like = (qt.tensor([qt.basis(N,1)]*n_sites) + qt.tensor([qt.basis(N,2)]*n_sites)).unit()

print("Evoluzione in corso... (dim=81, può richiedere qualche secondo)")
result = qt.mesolve(H_t, ghz_like, times, c_ops=c_ops, e_ops=[Op_tau])

# Calcolo negativity multi-pair (coppie 0-1, 0-2, 0-3)
neg_pairs = {f'0-{k}': [] for k in range(1, n_sites)}
for state in result.states:
    for k in range(1, n_sites):
        rho_pair = ptrace(state, [0, k])
        neg = negativity(rho_pair, 2)  # log-negativity
        neg_pairs[f'0-{k}'].append(neg)

# Plot negativity multi-pair
plt.figure(figsize=(12,7))
for pair, neg_list in neg_pairs.items():
    plt.plot(times, neg_list, label=f'Negativity {pair}')
plt.axhline(0.05, color='r', linestyle='--', label='Threshold entanglement')
plt.xlabel('Tempo')
plt.ylabel('Logarithmic Negativity')
plt.title('Multi-pair Long-range Entanglement Witness (4-site ladder con strain noise)')
plt.legend()
plt.grid(True)
plt.show()

# Proxy coherence long-range (mean |<α0† α3>| normalizzato)
corr_03 = np.abs(expect(alpha[0].dag() * alpha[-1], result.states))
norm_corr = corr_03 / np.max(corr_03 + 1e-12)
print(f"Mean long-range coherence proxy (0-3): {np.mean(norm_corr[-len(norm_corr)//3:]):.4f}")