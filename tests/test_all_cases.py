'''
Just a quick script to run the simulator against all 10 test cases
that were given in the assignment, and check that the total number of
packages delivered matches the number of packages in the input
(this was mentioned in the notes section of the assignment).

Not a proper test framework, just a sanity check script.
'''

import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from delivery_system import get_warehouses, get_agents, get_packages, assign_packages, simulate_delivery


for i in range(1, 11):
    filename = "test_case_" + str(i) + ".json"
    f = open(filename, "r")
    data = json.load(f)
    f.close()

    warehouses = get_warehouses(data)
    agents = get_agents(data)
    packages = get_packages(data)

    assignment = assign_packages(warehouses, agents, packages)
    report = simulate_delivery(warehouses, agents, assignment)

    total_delivered = 0
    for agent_id in report:
        if agent_id == "best_agent":
            continue
        total_delivered += report[agent_id]["packages_delivered"]

    status = "OK" if total_delivered == len(packages) else "MISMATCH"
    print(filename, "-> delivered", total_delivered, "/", len(packages), "packages -", status, "  best agent:", report["best_agent"])
