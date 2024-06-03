import minizinc
import csv
import time

def splitter(result):
    right = str(result)
    space = right.find(" ")
    costPart= right[:space].strip()
    equation = right[space+1:].strip()
    cost = int(costPart)
    return cost, equation

model = minizinc.Model("Playground_py.mzn")
chuffed = minizinc.Solver.lookup("chuffed")
Cs = list(range(1, 10))
results = []

for C in Cs:
    instance = minizinc.Instance(chuffed, model)
    instance["C"] = C
    start = time.time() 
    result = instance.solve()
    end = time.time() 
    if result:
        cost, equation = splitter(result)
        results.append({"C": C, "Bits": C.bit_length(), "Cost": cost, "Equation": equation, "Runtime": end - start})
        print(C, " tested")

with open("results.csv", "w", newline="") as csvfile:
    fieldnames = ["C", "Bits", "Equation", "Cost", "Runtime"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print("Complete in results.csv")
