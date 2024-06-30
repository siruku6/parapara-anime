import os
from typing import Iterable
import matplotlib.pyplot as plt
import pytest
import numpy as np

from parapara.generator import play_anim, save_as_gif, to_numpy


class TestToNumpy:
    @pytest.fixture(name="dummy_figure")
    def fixture_dummy_figure(self) -> plt.figure:
        """
        Generte a small Figure which is used in tests
        """
        size: int = 10
        x: np.ndarray = np.arange(0, size + 1)
        y: np.ndarray = np.arange(0, size + 1)

        fig = plt.figure(figsize=(4, 4), dpi=10)
        ax = fig.add_subplot(111)
        ax.plot(x, y)

        yield fig

        plt.clf()
        plt.close()

    def test_format(self, dummy_figure: plt.figure) -> None:
        """
        Test the format of the numpy array is correct.
        """
        np_image: np.ndarray = to_numpy(dummy_figure)

        assert isinstance(np_image, np.ndarray)
        assert np_image.shape[2] in [3, 4]

    @pytest.fixture(name="expected_nparray")
    def fixture_expected_nparray(self, request) -> Iterable:
        """
        Load the expected numpy array from the file

        Refernce
        ------
        The way to get the path of directory derives from the following article:
            https://medium.com/opsops/how-to-get-directory-with-test-from-fixture-in-conftest-py-275b566fcc00
        """
        f_name: str = "expected_nparray.npy"
        test_dir: str = os.path.dirname(request.module.__file__)
        data_filename = os.path.join(test_dir, "fixtures", "test_generator", f_name)
        np_array = np.load(data_filename)

        yield np_array

        del np_array

    def test_each_values(
        self, dummy_figure: plt.figure, expected_nparray: np.ndarray
    ) -> None:
        """
        Test the values of the numpy array are correct.
        """
        np_image: np.ndarray = to_numpy(dummy_figure)
        np.testing.assert_array_equal(np_image, expected_nparray)
