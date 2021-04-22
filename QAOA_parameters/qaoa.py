# QAOA circuit for MAXCUT

from qiskit import QuantumCircuit, Aer, execute
from qiskit.compiler import transpile

def append_zz_term(qc, q1, q2, gamma):
    qc.cx(q1,q2)
    qc.rz(2*gamma, q2)
    qc.cx(q1,q2)

def get_maxcut_cost_operator_circuit(G, gamma):
    N = G.number_of_nodes()
    qc = QuantumCircuit(N)
    for i, j in G.edges():
        append_zz_term(qc, i, j, gamma)
    return qc

def append_x_term(qc, q1, beta):
    qc.h(q1)
    qc.rz(2*beta, q1)
    qc.h(q1)

def get_mixer_operator_circuit(G, beta):
    N = G.number_of_nodes()
    qc = QuantumCircuit(N)
    for n in G.nodes():
        append_x_term(qc, n, beta)
    return qc

def get_maxcut_qaoa_circuit(G, beta, gamma, transpile_to_basis=True):
    assert(len(beta) == len(gamma))
    p = len(beta) # infering number of QAOA steps from the parameters passed
    N = G.number_of_nodes()
    qc = QuantumCircuit(N)
    # first, apply a layer of Hadamards
    qc.h(range(N))
    # second, apply p alternating operators
    for i in range(p):
        qc += get_maxcut_cost_operator_circuit(G,gamma[i])
        qc += get_mixer_operator_circuit(G,beta[i])
    if transpile_to_basis:
        qc = transpile(qc, optimization_level=0,basis_gates=['u1', 'u2', 'u3', 'cx'])
    return qc