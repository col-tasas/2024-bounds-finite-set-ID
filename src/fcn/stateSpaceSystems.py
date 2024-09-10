__author__ = "Nicolas Chatzikiriakos"
__contact__ = "nicolas.chatzikiriakos@ist.uni-stuttgart.de"
__date__ = "2024/08/13"


import numpy as np

__author__ = "Nicolas Chatzikiriakos"
__contact__ = "nicolas.chatzikiriakos@ist.uni-stuttgart.de"
__date__ = "2024/09/06"


# Metasclass for systems
class system:
    def __init__(self) -> None:
        pass

    def sim(self, x: np.ndarray, u: np.ndarray, w: np.ndarray) -> np.ndarray:
        pass


# Class of discrete-time LTI Systems
class LTI_discrete(system):
    def __init__(self, A: np.ndarray, B: np.ndarray) -> None:
        """
        Requires
            A: np.ndarray, A matrix of the System
            B: np.ndarray, Input matrix of the System
            stdNoise: Std of the process noise affecting the system
        """
        self.A = A
        self.B = B
        self.n_x, self.n_u = B.shape

    def sim(self, x: np.ndarray, u: np.ndarray, w: np.ndarray) -> np.ndarray:
        """
        Simulates one timestep, requires:
        x: np.ndarray, dimension (n_x, 1), state vector
        u: np.ndarray, dimension (n_u, 1), input vector
        w: np.ndarray, dimension (n_x, 1), noise vecotr
        """
        x_p = self.A @ x + self.B @ u + w
        return x_p
