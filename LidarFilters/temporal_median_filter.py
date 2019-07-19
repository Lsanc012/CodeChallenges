import numpy as np

class TemporalMedianFilter:
    def __init__(self, num_prev_scans):
        if num_prev_scans < 0:
            print("Warning: invalid previous scan quantity - value must me greater than or equal to 0")
        self.num_prev_scans = num_prev_scans

        self.prev_scan_data = []
        self.data_array_len = 0

        self.history_index = 0

    def update(self, scan_data):
        if len(scan_data) != self.data_array_len and self.data_array_len > 0 and len(scan_data) > 0:
            print("Error: unable to update filter - array lengths do NOT match or array is empty")
            return []

        self.data_array_len = len(scan_data)

        filtered_scan_data = []
        for i, data_element in enumerate(scan_data):
            history_vals = []

            if (len(self.prev_scan_data) == self.data_array_len) and len(self.prev_scan_data[-1]) == self.num_prev_scans:
                history_vals = [j for j in self.prev_scan_data[i]]
                self.prev_scan_data[i][self.history_index] = data_element
            else:
                if len(self.prev_scan_data) < self.data_array_len:
                    self.prev_scan_data.append([data_element])
                else:
                    history_vals = [j for j in self.prev_scan_data[i]]
                    self.prev_scan_data[i].append(data_element)

            filtered_scan_data.append(np.median((history_vals + [data_element])))

        self.history_index += 1

        if self.history_index >= self.num_prev_scans:
            self.history_index = 0

        return filtered_scan_data
