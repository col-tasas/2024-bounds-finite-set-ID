import numpy as np
import pandas as pd
import os
import argparse

from datetime import datetime

from fcn.stateSpaceSystems import LTI_discrete
from fcn.theoreticalCond import checkTheoCondUpper, checkTheoCondLower
from fcn.runExp import run_multiple_experiments

__author__ = "Nicolas Chatzikiriakos"
__contact__ = "nicolas.chatzikiriakos@ist.uni-stuttgart.de"
__date__ = "24/09/09"


if __name__ == "__main__":

    # Choose experiment
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--exp", required=True, type=int, help="Enter Experiment (1, 2 or 3)"
    )
    args = parser.parse_args()
    exp = args.exp

    # specify T, delta, nRuns
    T_max = np.array([10, 20])  # np.array([250, 500, 750, 1000, 1250])
    delta = 0.05
    nRuns = 1000

    # Name for saving
    name = (
        "dataExp"
        + str(exp)
        + "_"
        + datetime.today().strftime("%Y-%m-%d")
        + "_delta_"
        + str(int(100 * delta))
        + ".csv"
    )

    # Set the seed for reproducibility
    np.random.seed(42)

    # Define Systems
    n_x = 3
    n_u = 2

    A_0 = np.array([[0.2, 0.1, 0], [0, 0.2, 0], [0, 0, 0.5]])
    A_1 = np.array([[0.1, 0.1, 0], [0, 0.2, 0], [0, 0, 0.5]])
    A_2 = np.array([[0.2, 0.1, 0], [0, 0.2, 0], [0, 0, 0.6]])

    B_0 = np.array([[0, 0], [1, 0], [0, 1]])
    B_1 = B_0
    B_2 = B_0

    sys0 = LTI_discrete(A_0, B_0)
    sys1 = LTI_discrete(A_1, B_1)
    sys2 = LTI_discrete(A_2, B_2)

    systems = [sys0, sys1, sys2]

    N = len(systems)

    # Noise and input variance
    if exp == 1:
        sigmaW = 0.1 * np.identity(n_x)
        sigmaU = np.array([[10, 0], [0, 0.1]])
    elif exp == 2:
        sigmaW = 0.1 * np.identity(n_x)
        sigmaU = np.array([[0.1, 0], [0, 10]])
    elif exp == 3:
        sigmaW = np.array([[10, 0, 0], [0, 0.1, 0], [0, 0, 0.001]])
        sigmaU = np.array([[10, 0], [0, 0.1]])

    # Vector with estimation percentage
    estimation_per_ERM = np.zeros((N, T_max.size))
    estimation_per_OLS = np.zeros((N, T_max.size))
    theoCondLower = np.zeros((T_max.size))
    theoCondUpper = np.zeros((T_max.size))

    for ii, T in enumerate(T_max):

        # Check Theoretical Conditions
        theoCondUpper[ii] = checkTheoCondUpper(delta, T, systems, sigmaU, sigmaW)
        theoCondLower[ii] = checkTheoCondLower(delta, T, systems, sigmaU, sigmaW)

        args = {
            "systems": systems,
            "T_max": T,
            "sigmaW": sigmaW,
            "sigmaU": sigmaU,
        }

        results = run_multiple_experiments(args, nRuns)

        for jj in range(N):
            estimation_per_ERM[jj, ii] = np.count_nonzero(results[:, 0] == jj) / nRuns
            estimation_per_OLS[jj, ii] = np.count_nonzero(results[:, 1] == jj) / nRuns

    data = pd.DataFrame(
        {
            "T": T_max,
            "Sys0_per_ERM": estimation_per_ERM[0, :],
            "Sys1_per_ERM": estimation_per_ERM[1, :],
            "Sys2_per_ERM": estimation_per_ERM[2, :],
            "Sys0_per_OLS": estimation_per_OLS[0, :],
            "Sys1_per_OLS": estimation_per_OLS[1, :],
            "Sys2_per_OLS": estimation_per_OLS[2, :],
            "theoCondLower": theoCondLower,
            "theoCondUpper": theoCondUpper,
        }
    )

    # Save to CSV
    if not (os.path.isdir("../data")):
        os.mkdir("../data")

    data.to_csv("../data/" + name, sep=";", encoding="utf-8", index=False, header=True)
