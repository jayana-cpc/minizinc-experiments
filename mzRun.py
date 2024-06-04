import minizinc
import csv
import time
import matplotlib.pyplot as plt

def splitter(result):
    right = str(result)
    space = right.find(" ")
    costPart = right[:space].strip()
    equation = right[space+1:].strip()
    cost = costPart
    return cost, equation

# Regular Model
model = minizinc.Model("costModel1.mzn")
# Model Weighted k + 1
model2 = minizinc.Model("costModel2.mzn")
# Model Weighted Subtraction by 1.5
model3 = minizinc.Model("costModel3.mzn")
# Model Including Powers of 3
model4 = minizinc.Model("costModel4.mzn")

coinbc = minizinc.Solver.lookup("coinbc")
Cs = list(range(1, 1001))
results = []

saveInt = 10  

for C in Cs:
    try:
        instance = minizinc.Instance(coinbc, model)
        instance2 = minizinc.Instance(coinbc, model2)
        instance3 = minizinc.Instance(coinbc, model3)
        instance4 = minizinc.Instance(coinbc, model4)

        instance["C"] = C
        instance2["C"] = C
        instance3["C"] = C
        instance4["C"] = C

        start = time.time()
        result = instance.solve()
        result2 = instance2.solve()
        result3 = instance3.solve()
        result4 = instance4.solve()
        end = time.time()
        
        if result:
            cost, equation = splitter(result)
            cost2, equation2 = splitter(result2)
            cost3, equation3 = splitter(result3)
            cost4, equation4 = splitter(result4)
            results.append({"C": C, "Bits": C.bit_count(), "Cost": cost, "Cost (k+1)": cost2, "Cost Subtraction 1.5": cost3, "Cost Powers of 3": cost4, "Equation": equation, "Runtime": end - start})
            print(C, "tested")

        if C % saveInt == 0:
            with open("results.csv", "w", newline="") as csvfile:
                fieldnames = ["C", "Bits", "Equation", "Cost", "Cost (k+1)", "Cost Subtraction 1.5", "Cost Powers of 3", "Runtime"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
            print("Progress at C =", C)

    except Exception as e:
        print(f"Error at C = {C}: {e}")
        with open("results.csv", "w", newline="") as csvfile:
            fieldnames = ["C", "Bits", "Equation", "Cost", "Cost (k+1)", "Cost Subtraction 1.5", "Cost Powers of 3", "Runtime"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print("Results Error at C =", C)
        break

with open("results.csv", "w", newline="") as csvfile:
    fieldnames = ["C", "Bits", "Equation", "Cost", "Cost (k+1)", "Cost Subtraction 1.5", "Cost Powers of 3", "Runtime"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)
print("Complete in results.csv")

C_Val = [row["C"] for row in results]
Cost_Val = [row["Cost"] for row in results]
Cost_k1_Vals = [row["Cost (k+1)"] for row in results]
Cost_Subtraction_Val = [row["Cost Subtraction 1.5"] for row in results]
Cost_Power_3 = [row["Cost Powers of 3"] for row in results]

plt.figure(figsize=(10, 6))
plt.plot(C_Val, Cost_Val, label='Cost', marker='o')
plt.plot(C_Val, Cost_k1_Vals, label='Cost (k+1)', marker='x')
plt.plot(C_Val, Cost_Subtraction_Val, label='Cost Subtraction 1.5', marker='s')
plt.plot(C_Val, Cost_Power_3, label='Cost Powers of 3', marker='p')

plt.xlabel('C')
plt.ylabel('Cost')
plt.title('Comparison of Costs for Different Models')
plt.legend()
plt.grid(True)
plt.show()
