import numpy as np
from fcn.stateSpaceSystems import system

__author__ = "Nicolas Chatzikiriakos"
__contact__ = "nicolas.chatzikiriakos@ist.uni-stuttgart.de"
__date__ = "24/09/06"


# Base class for estimators
class Estimator:
    def __init__(self, candidate_sys, sigmaW) -> None:
        """
        Initializes the Estimator with candidate systems and noise covariance

        Parameters:
        - candidate_sys: list of candidate systems to evaluate
        - sigmaW: noise covariance matrix
        """

        self.candidate_sys = candidate_sys
        self.sigmaW = sigmaW
        self.best_sys = None
        pass

    def fit(self, x_traj: np.array, u_traj: np.array) -> None:
        """
        Abstract method to find the best fit out of the candidate systems.

        Parameters:
        - x_traj: state trajectory
        - u_traj: input trajectory
        """

        pass

    def get_best_model(self):
        """
        Return the best model after fitting.

        Returns:
        - best_model: the model with the lowest empirical risk.
        """

        return self.best_sys


# Estimator Subclass to claculate Empirical Risk Minimizer
class EmpiricalRiskMinimizer(Estimator):
    def __init__(self, candidate_sys, sigmaW) -> None:
        """
        Initializes the ERM with a list of candidate models

        Parameters:
        - candidateSys: list of candidate systems
        - sigmaW: noise covariance matrix
        """

        super().__init__(candidate_sys, sigmaW)
        self.best_risk = float("inf")

    def fit(self, x_traj: np.ndarray, u_traj: np.ndarray) -> None:
        """
        Fit each candidate model to the data and select the one with the lowest ER

        Parameters:
        - x_traj: np.ndarray, state trajectory
        - u_traj: np.ndarray, input trajectory

        """

        for index, sys in enumerate(self.candidate_sys):
            risk = self.empirical_risk(sys, x_traj, u_traj)
            if risk < self.best_risk:
                self.best_risk = risk
                self.best_sys = index

    def empirical_risk(
        self, sys: system, x_traj: np.ndarray, u_traj: np.ndarray
    ) -> float:
        """
        Calculate the empirical risk (mean squared error) for a given model

        Parameters:
        - sys: the candidate system being evaluated
        - x_traj: np.ndarray, state trajectory
        - u_traj: np.ndarray, input trajectory

        Returns:
        - risk: float, the empirical risk
        """

        x_p = sys.sim(x_traj[:, :-1], u_traj, 0)
        risk = np.mean(
            np.diag(
                (x_p - x_traj[:, 1:]).transpose()
                @ np.linalg.inv(self.sigmaW)
                @ (x_p - x_traj[:, 1:])
            )
        )

        return risk


# Estimator Subclass to calculate ordinary least squares estimate
class OLS(Estimator):
    def __init__(self, candidate_sys, sigmaW) -> None:
        """
        Initializes the OLS estimator with a list of candidate models

        Parameters:
        - candidateSys: list of candidate systems
        - sigmaW: noise covariance matrix
        """
        super().__init__(candidate_sys, sigmaW)
        self.dist = float("inf")

    def fit(self, x_traj: np.array, u_traj: np.array) -> None:
        """
        compute OLS and select candidate system closest to OLS

        Parameters:
        - x_traj: np.ndarray, state trajectory
        - u_traj: np.ndarray, input trajectory

        """

        theta_hat = self.leastSquares(x_traj, u_traj)
        for index, sys in enumerate(self.candidate_sys):
            theta_i = np.concatenate([sys.A.transpose(), sys.B.transpose()])
            dist = np.linalg.norm(theta_hat - theta_i, 2)
            if dist < self.dist:
                self.dist = dist
                self.best_sys = index

    def leastSquares(self, x_traj: np.array, u_traj: np.array) -> np.ndarray:
        """
        Least squares estimation of the system parameters

        Parameters:
        - x_traj: state trajectory
        - u_traj: input trajectory

        Returns:
        - theta_hat: estimated parameter matrix
        """

        X = np.concatenate([x_traj[:, :-1], u_traj]).transpose()
        Xp = x_traj[:, 1:].transpose()

        theta_hat = np.linalg.inv((X.transpose() @ X)) @ (X.transpose() @ Xp)

        return theta_hat
