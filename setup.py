from setuptools import find_packages, setup

setup(name='quantum_ncs',
      version='0.0.1',
      install_requires=['cirq', 'scikit-learn'],
      packages=find_packages('src'),
      package_dir={'': 'src'})
