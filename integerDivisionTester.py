"""
This program tests the accuracy of a Minizinc replication of integer division for a round to zero scheme 
defined in a paper by Drane and Cheung (https://cas.ee.ic.ac.uk/people/gac1/pubs/TheoISCAS12.pdf).


The workflow is as follows:
1. Initialize parameters `d` and `n`. `d` being the divisor. `n` being the bit length.
2. Define a `test_accuracy` function to test the accuracy of the solution by comparing the left-hand side (lhs) and right-hand side (rhs) values for all possible `x` values.
3. Solve Minizinc model.
4. Test the accuracy of the model and save the comparison results to a CSV file.
5. Print a message indicating whether the model's accuracy is satisfactory.

"""

import minizinc
import numpy as np
import pandas as pd 

d = np.uint8(7)
n = np.uint8(6)

def splitter(input_string):
    numbers = input_string.split()
    
    a_BF = np.uint8(int(numbers[0]))
    b_BF = np.uint8(int(numbers[1]))
    k_BF = np.uint8(int(numbers[2]))
    
    return a_BF, b_BF, k_BF

def test_accuracy(a_BF, b_BF, k_BF, d, n):
    max_val = (1 << n) - 1
    x_vals = [i for i in range(max_val + 1)]
    
    lhs = []
    rhs = []
    
    for x in x_vals:
        lhs_value = x // d
        rhs_value = ((a_BF * x) + b_BF) // (1 << k_BF)
        
        lhs.append(lhs_value)
        rhs.append(rhs_value)
    
    accuracy = all(l == r for l, r in zip(lhs, rhs))
    
    df = pd.DataFrame({
        'x_vals': x_vals,
        'lhs': lhs,
        'rhs': rhs
    })
    
    df.to_csv('lhs_rhs_values.csv', index=False)
    
    return accuracy

model = minizinc.Model("integerDivision.mzn")
solver = minizinc.Solver.lookup("highs")
instance = minizinc.Instance(solver, model)
instance["d"] = d
instance["n"] = n
result = instance.solve()
a_BF, b_BF, k_BF = splitter(str(result))

print("Start Accuracy testing")

result = test_accuracy(a_BF, b_BF, k_BF, d, n)
if result:
    print("The test accuracy is satisfactory. Model was accurate.")
else:
    print("Model was inaccurate")
