# Grover circuit solving 3-sat problem

import numpy as np
from qiskit import BasicAer
from qiskit.visualization import plot_histogram
%config InlineBackend.figure_format = 'svg' # Makes the images look nice
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import Grover
from qiskit.aqua.components.oracles import LogicalExpressionOracle, TruthTableOracle

input_sat = '''
c example DIMACS-CNF 3-SAT
p cnf 3 6
-1 -2 -3 0
1 -2 3 0
1 2 -3 0
1 -2 -3 0
-1 2 3 0
1 2 3 0
'''

oracle = LogicalExpressionOracle(input_sat)
grover = Grover(oracle)
backend = BasicAer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, shots=1024)
result = grover.run(quantum_instance)
print(result['result'])

plot_histogram(result['measurement'])

# Load our saved IBMQ accounts and get the ibmq_16_melbourne backend
from qiskit import IBMQ
from qiskit.compiler import transpile

IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
backend = provider.get_backend('ibmq_16_melbourne')

grover_compiled = transpile(result['circuit'], backend = backend, optimization_level = 3)