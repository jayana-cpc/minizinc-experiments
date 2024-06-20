"""
This program runs any number of Minizinc models on any set of input parameters.

Functions:
- splitter(result): Splits the result string into cost and equation parts.
- solve_instance(instance, C): Solves the MiniZinc instance with a given constant C.

Process:
1. Initialize MiniZinc models and solver.
2. Define the list of constants (Cs) to be tested.
3. For each constant C:
    a. Create instances for both models.
    b. Solve the instances concurrently with a timeout.
    c. Extract and store the results (cost and equation) for each model.
    d. Periodically save the results to a CSV file to track progress.
4. Save the final results to a CSV file after all constants are processed.

Additional:
- The program includes error handling and timeout management.
- Results are saved to 'results.csv'.
"""

import minizinc
import csv
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def splitter(result):
    right = str(result)
    space = right.find(" ")
    costPart = right[:space].strip()
    equation = right[space+1:].strip()
    cost = costPart
    return cost, equation

def solve_instance(instance, C):
    instance["C"] = C
    return instance.solve()

baseModel = minizinc.Model("baseModel.mzn")
latestModel = minizinc.Model("latestModel.mzn")

solver = minizinc.Solver.lookup("highs")
Cs = list(range(1,10001))
results = []

saveInt = 5
timeout_duration = 600 

with ThreadPoolExecutor(max_workers=5) as executor:
    for C in Cs:
        try:
            instance = minizinc.Instance(solver, baseModel)
            instance2 = minizinc.Instance(solver, latestModel)

            futures = [
                executor.submit(solve_instance, instance, C),
                executor.submit(solve_instance, instance2, C),
            ]

            start = time.time()
            results_list = []
            for future in futures:
                try:
                    result = future.result(timeout=timeout_duration)
                    results_list.append(result)
                except TimeoutError:
                    print(f"Timeout at C = {C}")
                    break

            end = time.time()

            if len(results_list) == 2:
                cost, equation = splitter(results_list[0])
                cost2, equation2 = splitter(results_list[1])

                results.append({
                    "C": C, "Bits": C.bit_count(), 
                    "Base Model Cost": cost, "Base Model Equation": equation,
                    "Latest Model Cost": cost2, "Latest Model Equation": equation2,
                })
                print(C, "tested")

            if C % saveInt == 0:
                with open("results.csv", "w", newline="") as csvfile:
                    fieldnames = [
                        "C", "Bits", 
                        "Base Model Cost", "Base Model Equation",
                        "Latest Model Cost", "Latest Model Equation",
                    ]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(results)
                print("Progress at C =", C)

        except Exception as e:
            print(f"Error at C = {C}: {e}")
            continue

with open("results.csv", "w", newline="") as csvfile:
    fieldnames = [
                        "C", "Bits", 
                        "Base Model Cost", "Base Model Equation",
                        "Latest Model Cost", "Latest Model Equation",
                    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)
print("Complete in results.csv")
