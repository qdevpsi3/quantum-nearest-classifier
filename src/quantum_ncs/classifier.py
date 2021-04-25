from sklearn.neighbors import NearestCentroid

from quantum_ncs.functions import quantum_distance


class QuantumNearestCentroid(NearestCentroid):
    def __init__(self, repetitions=500, error_rate=0., error_mitigation=True):
        self.repetitions = repetitions
        self.error_rate = error_rate
        self.error_mitigation = error_mitigation
        super().__init__(metric=self.get_metric)

    def get_metric(self, x, y):
        return quantum_distance(x,
                                y,
                                repetitions=self.repetitions,
                                error_rate=self.error_rate,
                                error_mitigation=self.error_mitigation)

    def fit(self, X, y):
        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings(action='ignore',
                                    message="Averaging for metrics other than "
                                    "euclidean and manhattan not supported. "
                                    "The average is set to be the mean.")
            return super().fit(X, y)
