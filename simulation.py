import CHSH
import numpy as np
import scipy.optimize as opt
import os
import sys

os.makedirs('data', exist_ok=True)

PI = np.pi

repeatNForOptimalAngles = 100000
PerfermeComparisons = True
PerfermeNoiseSimulation = True

if repeatNForOptimalAngles:
    def Strategy(err, n):
        def Outcome(diff_a, diff_0, diff_b):
            games = CHSH.PlayQuantum(n, err, diff_a, diff_0, diff_b)
            result = CHSH.Analyze(games)
            return result.WinRate
        objective = lambda x: -Outcome(x[0], x[1], x[2])
        bounds = [(-0.5*PI, 0.5*PI), (-0.5*PI, 0.5*PI), (-0.5*PI, 0.5*PI)]
        result = opt.differential_evolution(objective, bounds=bounds)
        return result.x

    f = open('data/optimalAngles.txt', 'w')
    original_stdout = sys.stdout
    sys.stdout = f
    n = repeatNForOptimalAngles
    for err in [0.0, 0.01,0.02, 0.05, 0.1, 0.2, 0.5, 0.99]:
        diff_a, diff_0, diff_b = Strategy(err, n)
        games = CHSH.PlayQuantum(n, err, diff_a, diff_0, diff_b)
        result = CHSH.Analyze(games)
        print("Error rate: ", err)
        print("Diff_a: ", diff_a * 180 / PI, " Diff_0: ", diff_0 * 180 / PI, " Diff_b: ", diff_b * 180 / PI)
        print(result)
        print()
    sys.stdout = original_stdout
    f.close()

if PerfermeComparisons:
    f = open('data/classicalComparison.txt', 'w')
    original_stdout = sys.stdout
    sys.stdout = f
    print("Classical Strategy")
    games = CHSH.PlayClassical(500000)
    result = CHSH.Analyze(games)
    print(result)
    print()
    print("Pure Random")
    games = CHSH.PlayRandom(500000)
    result = CHSH.Analyze(games)
    print(result)
    print()
    print("Perfect Quantum Strategy with 0/1 Basis")
    games = CHSH.PlayQuantum(500000, 0.0, 0.0, 0.0, 0.0)
    result = CHSH.Analyze(games)
    print(result)
    print()
    print("Perfect Quantum Strategy with Optimal Basis")
    games = CHSH.PlayQuantum(500000, 0.0, PI/4, PI/8, -PI/4)
    result = CHSH.Analyze(games)
    print(result)
    print()
    sys.stdout = original_stdout
    f.close()

if PerfermeNoiseSimulation:
    f = open('data/imperfectPreparation.txt', 'w')
    original_stdout = sys.stdout
    sys.stdout = f
    for err in [i*0.01 for i in range(101)]:
        print("Error Rate: ", err)
        games = CHSH.PlayQuantum(500000, err, PI/4, PI/8, -PI/4)
        result = CHSH.Analyze(games)
        print(result)
        print()
    sys.stdout = original_stdout
    f.close()

