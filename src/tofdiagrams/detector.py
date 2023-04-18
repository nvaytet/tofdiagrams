class Detector:
    def __init__(self, distance: float = 0.0):
        self.distance = distance

    def __repr__(self):
        return f"Detector(distance={self.distance})"
