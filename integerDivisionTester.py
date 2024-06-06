import minizinc
import math

d = 7
n = 6

def minh(a, b):
    p = max(a.bit_length(), b.bit_length())  
    c = 0
    for i in range(p - 1, -1, -1):  
        bit_a = (a >> i) & 1  
        bit_b = (b >> i) & 1  
        if bit_a == bit_b:
            c |= (bit_a << i) 
            a &= ~(1 << i) 
        else:
            c += 2**(i + 1)  
            break
    return c

model = minizinc.Model("findK.mzn")
coinbc = minizinc.Solver.lookup("coinbc")
findK = minizinc.Instance(coinbc, model)
findK["d"] = d
findK["n"] = n
result = findK.solve()
k = int(str(result))
a = math.floor(pow(2, k) // d)

if a*d - pow(2, k) > 0:
    b = 0
else:
    b = minh(((pow(2, k) - (a * d)) * math.floor(pow(2, n) // d)), (pow(2, k) - ((a * (d - 1)) - 1)))

print(f"a = {a}, b = {b}, k = {k}")

