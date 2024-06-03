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

model = minizinc.Model("costModel1.mzn")
model2 = minizinc.Model("costModel2.mzn")
chuffed = minizinc.Solver.lookup("chuffed")
Cs = list(range(1, 101))
results = []

for C in Cs:
    instance = minizinc.Instance(chuffed, model)
    instance2 = minizinc.Instance(chuffed, model2)

    instance["C"] = C
    instance2["C"] = C

    start = time.time() 
    result = instance.solve()
    result2 = instance2.solve()
    end = time.time() 
    if result:
        cost, equation = splitter(result)
        cost2, equation2 = splitter(result2)

        results.append({"C": C, "Bits": C.bit_count(), "Cost (k+1)": cost, "Cost": cost2,"Equation": equation, "Runtime": end - start})
        print(C, " tested")

with open("results.csv", "w", newline="") as csvfile:
    fieldnames = ["C", "Bits", "Equation", "Cost (k+1)", "Cost", "Runtime"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print("Complete in results.csv")
