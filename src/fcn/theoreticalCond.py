import numpy as np

__author__ = "Nicolas Chatzikiriakos"
__contact__ = "nicolas.chatzikiriakos@ist.uni-stuttgart.de"
__date__ = "24/09/06"


def checkTheoCondUpper(
    delta: float, T_max: int, candidate_sys, sigmaU: np.ndarray, sigmaW: np.ndarray
) -> bool:
    """
    Check theoretical condition for upper bound

    Parameters:
    - delta: failure probability
    - T_max: number of samples
    - candidate_sys: list of candidate systems, first element is true system
    - sigmaU: input covariance matrix
    - sigmaW: noise covariance matrix

    Returns:
    - bool: True if conditions for upper bound are satisfied, False otherwise
    """

    # Extract true system
    sys0 = candidate_sys[0]
    # Extract N
    N = len(candidate_sys)
    # Compute largest k
    k_max = np.floor(T_max / (320 / 3 * np.log(2 * sys0.n_x * N / delta)))

    condSat = np.array((N, 1), dtype=bool)

    if k_max > 0:
        for index, sys in enumerate(candidate_sys[1:]):
            deltaA = sys0.A - sys.A
            deltaB = sys0.B - sys.B
            trace = (
                sys0.n_x
                + np.linalg.norm(
                    np.sqrt(np.linalg.inv(sigmaW)) @ deltaB @ np.sqrt(sigmaU), "fro"
                )
                ** 2
            )

            for kk in range(int(np.floor(k_max / 2))):
                trace += (
                    np.linalg.norm(
                        np.sqrt(np.linalg.inv(sigmaW))
                        @ deltaA
                        @ np.linalg.matrix_power(sys0.A, kk)
                        @ np.sqrt(sigmaW),
                        "fro",
                    )
                    ** 2
                    + np.linalg.norm(
                        np.sqrt(np.linalg.inv(sigmaW))
                        @ deltaA
                        @ np.linalg.matrix_power(sys0.A, kk)
                        @ sys0.B
                        @ np.sqrt(sigmaU),
                        "fro",
                    )
                    ** 2
                )

            rhs = 9 / 3200 * k_max / T_max * np.floor(T_max / k_max) * trace

            condSat[index] = bool(sys0.n_x + np.sqrt(sys0.n_x) <= rhs)

    else:
        # Set conSat[0] to false if k = 0
        condSat[0] = False

    return all(condSat)


def checkTheoCondLower(
    delta: float, T_max: int, candidate_sys, sigmaU: np.ndarray, sigmaW: np.ndarray
) -> bool:
    """
    Check theoretical condition for lower obund

    Parameters:
    - delta: failure probability
    - T_max: number of samples
    - candidate_sys: list of candidate systems, first element is true system
    - sigmaU: input covariance matrix
    - sigmaW: noise covariance matrix

    Returns:
    - bool: True if conditions for lower bound are satisfied, False otherwise
    """

    # Extract true system
    sys0 = candidate_sys[0]
    # Extract N
    N = len(candidate_sys)
    # Vector to check whether conditions are met for all systems
    condSat = np.array((N, 1), dtype=bool)
    # Init Trace
    trace = 0

    for index, sys in enumerate(candidate_sys[1:]):
        deltaA = sys0.A - sys.A
        deltaB = sys0.B - sys.B
        trace = (
            T_max
            * np.linalg.norm(
                np.sqrt(np.linalg.inv(sigmaW)) @ deltaB @ np.sqrt(sigmaU), "fro"
            )
            ** 2
        )

        for s in range(T_max):
            trace += (T_max - 1 - s) * (
                np.linalg.norm(
                    np.sqrt(np.linalg.inv(sigmaW))
                    @ deltaA
                    @ np.linalg.matrix_power(sys0.A, s)
                    @ np.sqrt(sigmaW),
                    "fro",
                )
                ** 2
                + np.linalg.norm(
                    np.sqrt(np.linalg.inv(sigmaW))
                    @ deltaA
                    @ np.linalg.matrix_power(sys0.A, s)
                    @ sys0.B
                    @ np.sqrt(sigmaU),
                    "fro",
                )
                ** 2
            )

        condSat[index] = trace >= 2 * np.log(1 / (2.4 * delta))

    return all(condSat)
