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

latestModel2 = minizinc.Model("SCM_Expression_Reuse2.mzn")
latestModel = minizinc.Model("SCM_Expression_Reuse.mzn")

highs = minizinc.Solver.lookup("highs")
Cs = [
    38, 39, 1084, 2052, 2060, 2064, 2065, 2066, 2067, 2068, 2070, 2072, 2073, 2074, 2075, 2076, 2077,
    2081, 2082, 2083, 2085, 2088, 2089, 2094, 2095, 2096, 2097, 2098, 2100, 2101, 2102, 2103, 2104,
    2108, 2109, 2110, 2112, 2115, 2116, 2118, 2120, 2121, 2122, 2124, 2126, 2128, 2129, 2131, 2132,
    2135, 2136, 2140, 2144, 2148, 2152, 2158, 2160, 2162, 2164, 2166, 2168, 2169, 2171, 2172, 2173,
    2174, 2178, 2179, 2180, 2181, 2182, 2183, 2184, 2185, 2186, 2187, 2188, 2189, 2190, 2192, 2194,
    2196, 2200, 2204, 2205, 2206, 2212, 2216, 2224, 2236, 2238, 2239, 2240, 2255, 2256, 2262, 2264,
    2269, 2270, 2271, 2272, 2280, 2284, 2288, 2289, 2292, 2294, 2296, 2298, 2300, 2301, 2303, 2304,
    2305, 2307, 2310, 2312, 2314, 2316, 2318, 2320, 2321, 2325, 2328, 2332, 2333, 2335, 2336, 2337,
    2352, 2353, 2360, 2362, 2364, 2365, 2367, 2369, 2370, 2372, 2382, 2383, 2384, 2399, 2416, 2424,
    2428, 2430, 2433, 2434, 2436, 2440, 2486, 2488, 2489, 2494, 2495, 2496, 2497, 2498, 2502, 2504,
    2524, 2526, 2527, 2528, 2529, 2530, 2532, 2542, 2543, 2544, 2545, 2546, 2551, 2552, 2556, 2558,
    2559, 2560, 2561, 2564, 2567, 2568, 2569, 2575, 2577, 2578, 2588, 2590, 2591, 2592, 2593, 2594,
    2596, 2616, 2620, 2622, 2623, 2624, 2625, 2626, 2628, 2631, 2672, 2680, 2681, 2684, 2686, 2688,
    2689, 2690, 2696, 2702, 2704, 3996, 4544, 4574, 4576, 5088, 6654, 6902, 7230, 7236, 7896, 8112,
    8302, 8478, 9183, 9246, 9285, 9471, 9489, 9967, 9980
]
results = []

saveInt = 1
timeout_duration = 600 

with ThreadPoolExecutor(max_workers=5) as executor:
    for C in Cs:
        try:
            # instance = minizinc.Instance(gecode, baseModel)
            instance = minizinc.Instance(highs, latestModel)
            instance2 = minizinc.Instance(highs, latestModel2)

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
                    "Latest Model Cost HiGHS": cost, "Latest Model Equation HiGHS": equation,
                    "Latest Model2 Cost HiGHS": cost2, "Latest Model2 Equation HiGHS": equation2,
                })
                print(C, "tested")

            if C % saveInt == 0:
                with open("results.csv", "w", newline="") as csvfile:
                    fieldnames = [
                        "C", "Bits", 
                        "Latest Model Cost HiGHS", "Latest Model Equation HiGHS",
                        "Latest Model2 Cost HiGHS", "Latest Model2 Equation HiGHS",
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
                "Latest Model Cost HiGHS", "Latest Model Equation HiGHS",
                "Latest Model2 Cost HiGHS", "Latest Model2 Equation HiGHS",
            ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)
print("Complete in results.csv")
