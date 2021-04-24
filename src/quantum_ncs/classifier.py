from sklearn.neighbors import NearestCentroid

from quantum_ncs.functions import quantum_distance


class QuantumNearestCentroid(NearestCentroid):
    def __init__(self, repetitions=1000):
        self.repetitions = repetitions
        super().__init__(metric=self.get_metric)

    def get_metric(self, x, y):
        return quantum_distance(x, y, repetitions=self.repetitions)

    def fit(self, X, y):
        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings(action='ignore',
                                    message="Averaging for metrics other than "
                                    "euclidean and manhattan not supported. "
                                    "The average is set to be the mean.")
            return super().fit(X, y)
