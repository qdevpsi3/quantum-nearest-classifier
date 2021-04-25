import cirq
import numpy as np

from quantum_ncs.gates import MatrixLoader, VectorLoader
from quantum_ncs.noise import GateNoise, MeasurementNoise


def quantum_inner(x,
                  y,
                  repetitions=1000,
                  error_rate=0.,
                  error_mitigation=True):
    if error_rate == 0.:
        error_mitigation = False
    qubits = cirq.LineQubit.range(len(x))
    gates_x = cirq.decompose(VectorLoader(x)(*qubits))
    gates_y = cirq.decompose(VectorLoader(y, x_flip=False)(*qubits)**-1)
    if error_mitigation:
        gates_m = cirq.measure(*qubits)
    else:
        gates_m = cirq.measure(qubits[0])
    circuit = cirq.Circuit(gates_x, gates_y, gates_m)
    if error_rate > 0.:
        GateNoise(error_rate).apply(circuit)
        MeasurementNoise(error_rate).apply(circuit)
    simulator = cirq.Simulator()
    measure = simulator.run(circuit, repetitions=repetitions)
    if error_mitigation:
        key = ','.join(map(str, range(len(x))))
        total = measure.histogram(key=key)[2**(len(x) - 1)]
        num = sum(measure.histogram(key=key)[2**i] for i in range(len(x)))
    else:
        key = '0'
        total = measure.histogram(key='0')[1]
        num = repetitions
    inner = np.sqrt(total / num)
    return inner


def quantum_distance(x,
                     y,
                     repetitions=1000,
                     error_rate=0.,
                     error_mitigation=True):

    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    inner = quantum_inner(x, y, repetitions, error_rate, error_mitigation)
    dist = np.sqrt(norm_x**2 + norm_y**2 - 2 * norm_x * norm_y * inner)
    return dist


def _quantum_inner(x, y, repetitions=1000):
    qubits = cirq.LineQubit.range(len(x))
    gates_x = cirq.decompose(VectorLoader(x)(*qubits))
    gates_y = cirq.decompose(VectorLoader(y, x_flip=False)(*qubits)**-1)
    circuit = cirq.Circuit(gates_x + gates_y, cirq.measure(qubits[0]))
    simulator = cirq.Simulator()
    measurements = simulator.run(circuit, repetitions=repetitions)
    total = measurements.histogram(key='0')[1]
    inner = np.sqrt(total / repetitions)
    return inner


def _quantum_distance(x, y, repetitions=1000):
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    dist = np.sqrt(norm_x**2 + norm_y**2 -
                   2 * norm_x * norm_y * quantum_inner(x, y))
    return dist
