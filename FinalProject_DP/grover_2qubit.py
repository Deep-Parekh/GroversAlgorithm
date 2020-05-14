import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline
%config InlineBackend.figure_format = 'svg' # Makes the images look nice

# importing Qiskit
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

# import basic plot tools
from qiskit.visualization import plot_histogram

n = 2
grover_circuit = QuantumCircuit(n,n)

for qubit in range(n):
    grover_circuit.h(qubit)
grover_circuit.draw('mpl')

# Apply oracle for w = |00>
for qubit in range(n):
    grover_circuit.x(qubit)
    
grover_circuit.cz(0,1)

for qubit in range(n):
    grover_circuit.x(qubit)
    
grover_circuit.draw('mpl')

# Hadamard on both qubits
for qubit in range(n):
    grover_circuit.h(qubit)
    
grover_circuit.draw('mpl')

# reflection Us
for qubit in range(n):
    grover_circuit.z(qubit)
    
grover_circuit.cz(0,1)
grover_circuit.draw('mpl')

# Final Hadamard
for qubit in range(n):
    grover_circuit.h(qubit)
    
grover_circuit.draw('mpl')

# Simulation
grover_circuit.measure_all()
back = Aer.get_backend('qasm_simulator')
result = execute(grover_circuit, back, shots=1024).result()
counts = result.get_counts()
plot_histogram(counts)

# Running on actual Quantum Computer
IBMQ.load_account()
provider = IBMQ.get_provider('ibm-q')
qc = least_busy(provider.backends(simulator=False))
print("Running on current least busy device: ", qc)

job = execute(grover_circuit, backend = qc, shots = 1024)

from qiskit.tools.monitor import job_monitor
job_monitor(job)

result = job.result()
counts = result.get_counts()
plot_histogram(counts)