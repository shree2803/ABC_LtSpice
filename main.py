import numpy as np
import subprocess
import re
import os

# Function to modify the .param line in the SPICE netlist file
def modify_param_in_netfile(net_file_path, new_values_list):
    with open(net_file_path, 'r') as file:
        lines = file.readlines()

    param_dict = {}
    for line in lines:
        if ".param N1" in line:
            param_parts = line.strip().split(" ")[1:]
            for part in param_parts:
                key, value = part.split("=")
                param_dict[key] = value

    param_keys = list(param_dict.keys())

    if len(new_values_list) != len(param_keys):
        print("Error: The number of new values doesn't match the number of parameters.")
        return

    for i, key in enumerate(param_keys):
        param_dict[key] = new_values_list[i]

    new_param_line = ".param " + " ".join([f"{key}={param_dict[key]}" for key in param_keys]) + "\n"

    for i, line in enumerate(lines):
        if ".param N1" in line:
            lines[i] = new_param_line
            break

    with open(net_file_path, 'w') as file:
        file.writelines(lines)

    print(f"Modified the .net file: {net_file_path}")

# Function to run LTspice simulation
def run_ltspice_simulation(ltspice_path, netlist_path, log_path):
    command = [
        ltspice_path,
        '-b',
        netlist_path
    ]
    with open(log_path, 'w') as log_file:
        subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)
    print("Simulation complete. Log saved to", log_path)

# Function to parse the LTspice log for power and delay
def parse_ltspice_log(log_path):
    with open(log_path, 'r') as file:
        log_content = file.read()

    power_match = re.search(r"sum:\s*AVG\(v\(s\)\*i\(r2\)\)=([\d\.e+-]+)", log_content)
    delay_match = re.search(r"delay_sum_cin:\s*\(tphl_sum_cin \+ tplh_sum_cin\) / 2=([\d\.e+-]+)", log_content)

    power = float(power_match.group(1)) if power_match else None
    delay = float(delay_match.group(1)) if delay_match else None

    return power, delay

# Function to calculate the Power-Delay Product (PDP)
def pdp_cost_function(params):
    netlist_path = "delay_pr.net"
    log_path = "delay_pr.log"
    ltspice_path = r"C:\Users\shree\AppData\Local\Programs\ADI\LTspice\LTspice.exe"  # Adjust as needed

    modify_param_in_netfile(netlist_path, params)
    run_ltspice_simulation(ltspice_path, netlist_path, log_path)
    power, delay = parse_ltspice_log(log_path)

    if power is None or delay is None:
        print("Failed to extract power or delay. Returning high cost.")
        return float('inf')  # Return a high cost if extraction fails

    pdp = power * delay
    return pdp

# ABC algorithm for optimization
def abc_algorithm(cost_func, num_bees=30, max_iter=10, dim=10, bounds=(67e-9, 350e-9)):
    best_solution = None
    best_cost = float('inf')

    # Initialize population
    population = np.random.uniform(bounds[0], bounds[1], (num_bees, dim))
    costs = np.array([cost_func(ind) for ind in population])

    for iteration in range(max_iter):
        print(iteration)
        for i in range(num_bees):
            phi = np.random.uniform(-1, 1)
            k = np.random.choice([j for j in range(num_bees) if j != i])
            new_solution = population[i] + phi * (population[i] - population[k])
            new_solution = np.clip(new_solution, bounds[0], bounds[1])
            new_cost = cost_func(new_solution)

            if new_cost < costs[i]:
                population[i] = new_solution
                costs[i] = new_cost

                if new_cost < best_cost:
                    best_solution = new_solution
                    best_cost = new_cost

        print(f"Iteration {iteration + 1}/{max_iter}, Best PDP: {best_cost}")

    return best_solution, best_cost

# Run the ABC algorithm to optimize transistor parameters
# min_cost=18e-15
best_params, best_pdp = abc_algorithm(pdp_cost_function)
print("Optimized Transistor Parameters:", best_params)
print("Optimized PDP:", best_pdp*2)
