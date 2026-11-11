import numpy as np

class Buffer:
    @staticmethod
    def make(list_of_values: list[float | int]) -> "Buffer":
        array = np.array(list_of_values, dtype=np.float32)
        return Buffer(array)

    @staticmethod
    def make_copy_repeating(list_of_values: list[float|int], buffer:"Buffer") -> "Buffer":
        return np.tile(np.array(list_of_values, dtype=np.float32), (buffer.data.shape[0], 1))
    
    def __init__(self, array : np.ndarray | None, ctype = np.float32) -> None:
        self.ctype = ctype
        self.data: np.ndarray = array if array is not None else np.array([], dtype=self.ctype)


    def add_element(self, value: int|float) -> None:
        if isinstance(value, int) and self.ctype != np.int32:
            raise TypeError("Value type does not match buffer type.")
        if isinstance(value, float) and self.ctype != np.float32:
            raise TypeError("Value type does not match buffer type.")
        self.data = np.append(self.data, np.array([value], dtype=self.ctype))

    def add_array(self, array: "Buffer") -> None:
        self.data = np.append(self.data, array.data.astype(self.ctype))

    def attach_data_to_index(self, index, data: Buffer):
        """Attach data to a specific index in the buffer"""
        element = self.data[index]
        self.data[index] = np.hstack((element, data.data)).reshape(-1).astype(self.ctype)

    def attach_data(self, data: Buffer):
        """Attach data to the entire buffer"""
        self.data = np.hstack((self.data, data.data)).reshape(-1).astype(self.ctype)

    def attach_data_per_section(self, data: Buffer, start: int, end: int):
        if self.in_buffer(start) or self.in_buffer(end):
            raise ValueError("End index exceeds the number of vertices.")
        self.data[start:end] = np.hstack((self.data[start:end], data.data)).reshape(-1).astype(self.ctype)

    def in_buffer(self, index) -> bool:
        return index >= self.data.shape[0] or index < 0 

    def length(self) -> int:
        return self.data.shape[0]

    def is_same_length(self, other: "Buffer") -> bool:
        return self.length() == other.length()
