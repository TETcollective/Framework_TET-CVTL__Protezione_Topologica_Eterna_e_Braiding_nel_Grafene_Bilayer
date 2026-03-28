"""
01_two_parafermions_basic.py
Modello toy a due parafermioni Z3 coupled per Fibonacci fusion
Autore: Phys Soliman (TET Collective)
Data: Marzo 2026
"""

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt

N = 3  # Z3 clock basis
id3 = qt.qeye(N)

# Basis states
basis = [qt.basis(N, i) for i in range(N)]

# Clock operator (parafermion shift)
clock = qt.Qobj(np.array([[0, 0, 1],
                          [1, 0, 0],
                          [0, 1, 0]], dtype=complex))

alpha1 = qt.tensor(clock, id3)
alpha2 = qt.tensor(id3, clock)

# Coupling Hamiltonian
J = 0.45
eps = 0.1
H0 = J * (alpha1.dag() * alpha2 + alpha1 * alpha2.dag())
H0 += eps * (qt.tensor(basis[1]*basis[1].dag() + 2*basis[2]*basis[2].dag(), id3) +
             qt.tensor(id3, basis[1]*basis[1].dag() + 2*basis[2]*basis[2].dag()))

# Floquet drive
V = 0.4
omega_d = 2 * np.pi * 4.5
def H_t(t, args):
    return H0 + V * np.cos(omega_d * t) * (alpha1 + alpha1.dag() + alpha2 + alpha2.dag())

# Lindblad operators
gamma_poison = 0.015
gamma_leak = 0.008
c_ops = [
    np.sqrt(gamma_poison) * (alpha1 - alpha2),
    np.sqrt(gamma_leak) * qt.tensor(basis[0]*basis[0].dag(), basis[0]*basis[0].dag())
]

# Torque observable (chiral + gravitomag proxy)
chiral_part = 1j * (alpha1.dag() * alpha2 - alpha1 * alpha2.dag())
L_z_proxy = 0.6 * (qt.tensor(basis[1]*basis[1].dag() + 2*basis[2]*basis[2].dag(), id3) -
                   qt.tensor(id3, basis[1]*basis[1].dag() + 2*basis[2]*basis[2].dag()))
g_chiral = 1.0
g_grav = 0.35
Op_tau_grav = g_chiral * chiral_part + g_grav * L_z_proxy

# Initial state (Fibonacci-like superposition)
psi0 = (qt.tensor(basis[1], basis[1]) + qt.tensor(basis[2], basis[2])).unit()

times = np.linspace(0, 250, 10000)

result = qt.mesolve(H_t, psi0, times, c_ops=c_ops, e_ops=[Op_tau_grav])

# Plot
plt.figure(figsize=(10,6))
plt.plot(times, qt.expect(Op_tau_grav, result.states), label=r'$\langle O_\tau \rangle$')
plt.xlabel('Time')
plt.ylabel('Torque proxy')
plt.title('Two-Parafermion Model - Torque Expectation')
plt.legend()
plt.grid(True)
plt.show()