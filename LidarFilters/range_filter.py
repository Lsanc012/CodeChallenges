import numpy as np

class RangeFilter:
    def __init__(self, min_range, max_range):
        self.min_range = min_range
        self.max_range = max_range

    def update(self, scan_data):
        return [np.minimum(np.maximum([i], [self.min_range]), [self.max_range])[0] for i in scan_data]
