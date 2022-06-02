import argparse
import os
import shutil
import unittest
from os.path import dirname, abspath
from unittest import mock

import run
from processing import Processing
from sourcing import Source

shape = (112, 112, 3)
iterations = 10
rows = 768
width = 1024
path = os.path.join(dirname(dirname(abspath(__file__))), 'tmp')


class ProducedConsumerTestCase(unittest.TestCase):

    def test_case_even_numbers(self):
        new_shape = Processing(shape).get_new_shape(shape)
        self.assertEqual((56, 56, 3), new_shape)

    def test_case_odd_numbers(self):
        new_shape = Processing(shape).get_new_shape(shape)
        self.assertEqual((56, 56, 3), new_shape)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    rows=10,
                    columns=10,
                    channels=3,
                    iterations=iterations,
                    output=path))
    def test_case_10_iter_main(self, mock_args):
        run.main()
        lista_jpg = [x for x in os.listdir(path) if x.endswith('.png')]
        shutil.rmtree(path)
        self.assertEqual(iterations, len(lista_jpg))

    def test_case_shape_source(self):
        data = Source(shape).get_data()
        self.assertEqual(shape, data.shape)


if __name__ == '__main__':
    unittest.main()
