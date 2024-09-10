import numpy as np
import concurrent.futures

from fcn.estimator import EmpiricalRiskMinimizer as ERM
from fcn.estimator import OLS as OLS

__author__ = "Nicolas Chatzikiriakos"
__contact__ = "nicolas.chatzikiriakos@ist.uni-stuttgart.de"
__date__ = "24/09/06"


def run_experiment(args) -> np.ndarray:
    """
    Function to run a single experiment and estimate the true system from it

    Parameters:
        - args: dictionary consisting of
            - systems: list of all systems in the discrete and finite system class S
            - T_max: Number of samples
            - sigmaU/sigmaW: Variance of Guassian noise/excitation

    Returns:
        - Estimated system [ERM, OLS]
    """

    systems = args["systems"]
    sys0 = systems[0]
    T_max = args["T_max"]
    sigmaW = args["sigmaW"]
    sigmaU = args["sigmaU"]
    # Compute Estimate

    # Define Data matrices
    u_traj = np.zeros((sys0.n_u, T_max))
    x_traj = np.zeros((sys0.n_x, T_max + 1))

    # Data Collection
    x_traj[:, [0]] = np.zeros((sys0.n_x, 1))
    for t in range(T_max):
        w = np.random.multivariate_normal(np.zeros(sys0.n_x), sigmaW)
        u_traj[:, t] = np.random.multivariate_normal(np.zeros((sys0.n_u)), sigmaU)
        x_traj[:, [t + 1]] = sys0.sim(
            x_traj[:, [t]],
            np.reshape(u_traj[:, t], (sys0.n_u, 1)),
            np.reshape(w, (sys0.n_x, 1)),
        )

    # ERM
    ERM_estimator = ERM(candidate_sys=systems, sigmaW=sigmaW)
    ERM_estimator.fit(x_traj, u_traj)

    # OLS
    OLS_estimator = OLS(candidate_sys=systems, sigmaW=sigmaW)
    OLS_estimator.fit(x_traj, u_traj)

    return np.array([ERM_estimator.best_sys, OLS_estimator.best_sys])


def run_multiple_experiments(args, nRuns) -> np.ndarray:
    """
    Function to run multiple experiments in parallel to safe runtime

    Parameters:
        - args: arguments that are inputs to run_experimentsobseravtion
        - nRuns: number of runs to be run

    Returns:
        - results: list with entry of estimate at the end of each experiment
    """

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(run_experiment, [args] * nRuns))
        results = np.array(results)

    return results
