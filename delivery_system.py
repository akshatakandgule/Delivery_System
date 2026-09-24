'''
Delivery System Simulator - FastBox
Internship Assignment - Python Developer

This program reads warehouse, agent and package data from a json file,
assigns every package to the nearest agent, simulates the delivery and
then makes a report showing how each agent performed.

How it works (short version):
1. Load data.json
2. For every package -> find the closest agent to its warehouse (using distance formula)
3. Let each agent "deliver" its packages one by one and add up the distance travelled
4. Print the report and also save it in report.json

Some things were not 100% clear in the problem statement so I made my own
assumption for those and wrote it in the comments below wherever it applies.
'''

import json
import math


def load_data(filename="data.json"):
    # just read the json file, nothing fancy
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    return data


def get_warehouses(data):
    # the test files give warehouses as a dictionary {"W1":[x,y]}
    # but the base_case.json file has it as a list of dicts instead,
    # so this handles both cases
    warehouses = {}
    w = data["warehouses"]
    if type(w) == dict:
        for wid in w:
            warehouses[wid] = w[wid]
    else:
        for item in w:
            warehouses[item["id"]] = item["location"]
    return warehouses


def get_agents(data):
    agents = {}
    a = data["agents"]
    if type(a) == dict:
        for aid in a:
            agents[aid] = a[aid]
    else:
        for item in a:
            agents[item["id"]] = item["location"]
    return agents


def get_packages(data):
    # some files use "warehouse" key, some use "warehouse_id", so check both
    packages = []
    for p in data["packages"]:
        wid = p.get("warehouse")
        if wid is None:
            wid = p.get("warehouse_id")
        packages.append({"id": p["id"], "warehouse": wid, "destination": p["destination"]})
    return packages


def distance(point1, point2):
    # simple distance formula (pythagoras theorem)
    x1, y1 = point1
    x2, y2 = point2
    d = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return d


def assign_packages(warehouses, agents, packages):
    # for each package, check every agent and find which one is closest
    # to the package's warehouse. that agent gets the package.
    assignment = {}
    for agent_id in agents:
        assignment[agent_id] = []

    for pkg in packages:
        w_loc = warehouses[pkg["warehouse"]]
        closest_agent = None
        closest_dist = 999999999  # just a big number to start with

        for agent_id in agents:
            a_loc = agents[agent_id]
            d = distance(a_loc, w_loc)
            if d < closest_dist:
                closest_dist = d
                closest_agent = agent_id

        assignment[closest_agent].append(pkg)

    return assignment


def simulate_delivery(warehouses, agents, assignment):
    # go through each agent's list of packages and "deliver" them
    # agent moves: current position -> warehouse -> destination
    # and this repeats for every package assigned to that agent
    report = {}

    for agent_id in assignment:
        current_pos = agents[agent_id]
        total_distance = 0
        delivered_count = 0

        for pkg in assignment[agent_id]:
            w_loc = warehouses[pkg["warehouse"]]
            dest = pkg["destination"]

            total_distance += distance(current_pos, w_loc)
            total_distance += distance(w_loc, dest)

            current_pos = dest  # agent is now here, ready for next package
            delivered_count += 1

        if delivered_count > 0:
            efficiency = round(total_distance / delivered_count, 2)
        else:
            # agent got no packages at all, so avoid divide by zero
            efficiency = 0

        report[agent_id] = {
            "packages_delivered": delivered_count,
            "total_distance": round(total_distance, 2),
            "efficiency": efficiency
        }

    # find the best agent (lowest efficiency = less distance per package = better)
    # only consider agents who actually delivered something
    best_agent = None
    best_efficiency = None
    for agent_id in report:
        if report[agent_id]["packages_delivered"] == 0:
            continue
        if best_efficiency is None or report[agent_id]["efficiency"] < best_efficiency:
            best_efficiency = report[agent_id]["efficiency"]
            best_agent = agent_id

    report["best_agent"] = best_agent
    return report


def print_ascii_map(warehouses, agents, packages):
    # bonus feature - quick and dirty ascii visualization of the map
    # W = warehouse, A = agent, . = package destination
    print("\nRoute Map (rough, not to scale):")

    all_points = list(warehouses.values()) + list(agents.values())
    for p in packages:
        all_points.append(p["destination"])

    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    if max_x == min_x:
        max_x += 1
    if max_y == min_y:
        max_y += 1

    width = 40
    height = 15
    grid = []
    for row in range(height):
        grid.append([" "] * width)

    def place(point, symbol):
        col = int((point[0] - min_x) / (max_x - min_x) * (width - 1))
        row = int((point[1] - min_y) / (max_y - min_y) * (height - 1))
        row = height - 1 - row
        grid[row][col] = symbol

    for p in packages:
        place(p["destination"], ".")
    for loc in warehouses.values():
        place(loc, "W")
    for loc in agents.values():
        place(loc, "A")

    for row in grid:
        print("".join(row))
    print("(W = warehouse, A = agent, . = package destination)")


def main():
    data = load_data("data.json")

    warehouses = get_warehouses(data)
    agents = get_agents(data)
    packages = get_packages(data)

    print("Loaded", len(warehouses), "warehouses,", len(agents), "agents,", len(packages), "packages")

    assignment = assign_packages(warehouses, agents, packages)

    print("\nPackage assignment:")
    for agent_id in assignment:
        pkg_ids = [p["id"] for p in assignment[agent_id]]
        print(agent_id, "->", pkg_ids)

    report = simulate_delivery(warehouses, agents, assignment)

    print("\nFinal Report:")
    print(json.dumps(report, indent=4))

    # save the report
    out = open("report.json", "w")
    json.dump(report, out, indent=4)
    out.close()
    print("\nReport saved to report.json")

    # check that all packages got delivered (as mentioned in the notes)
    total_delivered = 0
    for agent_id in report:
        if agent_id == "best_agent":
            continue
        total_delivered += report[agent_id]["packages_delivered"]
    print("Total packages delivered:", total_delivered, "/", len(packages))

    # bonus - show the ascii map
    print_ascii_map(warehouses, agents, packages)


if __name__ == "__main__":
    main()
