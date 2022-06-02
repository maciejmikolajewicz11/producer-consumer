import datetime
import logging
import os
from queue import Queue

import cv2
import numpy as np

from sourcing import Source


class Processing:

    def __init__(self, source_shape: tuple):
        self.new_shape = self.get_new_shape(source_shape)
        self.Source = Source(source_shape)
        self.finish = False

    @staticmethod
    def get_new_shape(source_shape: tuple) -> tuple:
        """Provide new image size reduced by 2
        Args:
            source_shape (tuple): current image size
        Returns:
            tuple: new image size
        """
        rows, columns, channels = source_shape
        return int(rows / 2), int(columns / 2), channels

    def transform_image(self, image: np.ndarray) -> np.ndarray:
        """Takes an image, returns the image reduced by 2 with removed noise
        Args:
            image (np.ndarray):
        Returns:
            np.ndarray:
        """
        resized = cv2.resize(image, dsize=(self.new_shape[:2]))
        filtered = cv2.medianBlur(resized, ksize=5)
        return filtered

    @staticmethod
    def save_images(output: str, output_queue: Queue, iterations: int):
        """ Save images from queue to provided directory
        Args:
            output (str): name of output folder
            output_queue (Queue): queue with processed images
            iterations (int): number of processed images
        """

        for _ in range(iterations):
            img = output_queue.get()
            cv2.imwrite(
                os.path.join(
                    os.getcwd(),
                    output,
                    f"processed_{datetime.datetime.now().time()}.png",
                ),
                img,
            )
        logging.info(f"Main    : saved {iterations} images to '{output}/' ")
