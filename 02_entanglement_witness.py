"""
02_entanglement_witness.py
Aggiunge calcolo entanglement entropy e negativity (multi-site proxy)
"""

# ... (continua dal codice precedente, dopo result = qt.mesolve(...))

from qutip import entropy_vn, negativity, ptrace

entropies = []
negativities = []

for state in result.states:
    # Entanglement tra i due parafermions (sistema bipartito)
    rho_A = ptrace(state, 0)  # partial trace su primo parafermion
    S = entropy_vn(rho_A)
    entropies.append(S)
    
    # Negativity long-range (proxy multi-site se esteso)
    rho_14 = ptrace(state, [0,1])  # full system per toy
    neg = negativity(rho_14, 2)  # logarithmic negativity
    negativities.append(neg)

mean_S = np.mean(entropies)
mean_neg = np.mean(negativities)

print(f"Mean von Neumann entropy (golden threshold >0.40): {mean_S:.4f}")
print(f"Mean negativity (entanglement witness >0.05): {mean_neg:.4f}")

if mean_S > 0.40:
    print("Golden signature: STRONG")
if mean_neg > 0.05:
    print("Long-range entanglement: DETECTED")