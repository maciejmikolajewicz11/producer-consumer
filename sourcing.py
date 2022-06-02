import numpy as np


class Source:
    """_summary_
    """    

    def __init__(self, source_shape: tuple):
        self._source_shape: tuple = source_shape

    def get_data(self) -> np.ndarray:
        """_summary_

        Returns:
            np.ndarray: _description_
        """        
        rows, columns, channels = self._source_shape
        return np.random.randint(
            256,
            size=rows * columns * channels,
            dtype=np.uint8,
        ).reshape(self._source_shape)
