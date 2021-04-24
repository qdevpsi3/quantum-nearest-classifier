<h1 align="center" style="margin-top: 0px;"> <b>Nearest Centroid Classiﬁcation on a Trapped Ion Quantum Computer</b></h1>
<div align="center" >

[![paper](https://img.shields.io/static/v1.svg?label=Paper&message=arXiv:2012.04145&color=b31b1b)](https://arxiv.org/abs/2012.04145)
[![packages](https://img.shields.io/static/v1.svg?label=Made%20with&message=Cirq&color=fbc43b)](https://quantumai.google/cirq)
[![license](https://img.shields.io/static/v1.svg?label=License&message=GPL%20v3.0&color=green)](https://www.gnu.org/licenses/gpl-3.0.html)
</div>

## **Description**
This repository contains an <ins>unofficial</ins> implementation of the <ins>Quantum Vector and Matrix loaders</ins> and its application to the <ins>Nearest Centroid Classification problem</ins> as in :

- Paper : **Nearest Centroid Classiﬁcation on a Trapped Ion Quantum Computer**
- Authors : **S. Johri, S. Debnath, A.Mocherla, A. Singh, A. Prakash, J. Kim, and I. Kerenidis**
- Date : **2021**

## **Installation**
To <ins>install</ins>, clone this repository and execute the following commands :

```
$ cd quantum-nearest-classifier
$ pip install -r requirements.txt
$ pip install -e .
```

## **Usage**

### *Data Loaders*
The vector and matrix loaders are built using the `cirq.Gate` base class. They can load data of size 2^n which is given as an input. 

```python
from quantum_ncs.gates import VectorLoader

dim = 8
vector = np.random.uniform(size=dim)
loader = VectorLoader(vector=vector)

qubits = cirq.LineQubit.range(dim)
circuit = cirq.Circuit(loader(*qubits))
```
You can also decompose the loader into *X* and *RBS* gates using : 
```python
circuit = cirq.Circuit(cirq.decompose(loader(*qubits)))

print(circuit)
```
```
0: ───X───B───B───B───
          │   │   │
1: ───────┼───┼───S───
          │   │
2: ───────┼───S───B───
          │       │
3: ───────┼───────S───
          │
4: ───────S───B───B───
              │   │
5: ───────────┼───S───
              │
6: ───────────S───B───
                  │
7: ───────────────S───
```

You can use the matrix loader in a similar way. For example :
```python
from quantum_ncs.gates import MatrixLoader

dim = 4
matrix = np.random.uniform(size=(dim,dim))
loader = MatrixLoader(matrix=matrix)

qubits = cirq.LineQubit.range(2*dim)
circuit = cirq.Circuit(cirq.decompose(loader(*qubits)))

print(circuit)
```
```
0: ───X───B───B───@───@───@───────────────────────────────────────
          │   │   │   │   │
1: ───────┼───S───┼───┼───┼───@───@───@───────────────────────────
          │       │   │   │   │   │   │
2: ───────S───B───┼───┼───┼───┼───┼───┼───@───@───@───────────────
              │   │   │   │   │   │   │   │   │   │
3: ───────────S───┼───┼───┼───┼───┼───┼───┼───┼───┼───@───@───@───
                  │   │   │   │   │   │   │   │   │   │   │   │
4: ───X───────────B───B───┼───B───B───┼───B───B───┼───B───B───┼───
                  │   │   │   │   │   │   │   │   │   │   │   │
5: ───────────────┼───S───┼───┼───S───┼───┼───S───┼───┼───S───┼───
                  │       │   │       │   │       │   │       │
6: ───────────────S───────B───S───────B───S───────B───S───────B───
                          │           │           │           │
7: ───────────────────────S───────────S───────────S───────────S───
```

### *Functions*
These gates are used to simulate the functions for the quantum inner product and distance estimation. For now, it requires that the inner product is positive. The argument `repetitions` specify the number of shots to perform. For example :
```python
from quantum_ncs.functions import quantum_inner, quantum_distance

dim = 4
x = np.random.uniform(size=dim)
y = np.random.uniform(size=dim)

inner = quantum_inner(x,y, repetitions=500)
dist = quantum_distance(x,y, repetitions=500)
```

### *Classifier*
The quantum nearest centroid classifier is built using the `sklearn` base class. It behaves similarly to the classical one.


```python
from quantum_ncs.classifier import QuantumNearestCentroid

clf = QuantumNearestCentroid(repetitions=500)

# train
clf.fit(X, y)

# test
y_pred = clf.predict(X)
```