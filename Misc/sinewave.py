from typing import Callable

import numpy as np


def create_sine_func(
    frequency: float, ampitude: int = 1, sample_freq: int = 44100
) -> Callable[[float], float]:
    angular_frq = 2 * np.pi * frequency
    opp = angular_frq / sample_freq
    return lambda t: ampitude * np.sin(opp * t)
