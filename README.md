# FastBox Delivery System

This is my submission for the Nexgensis Technologies Python Developer
internship assignment (Mystery Delivery System).

## What it does

Reads warehouse, agent and package data from `data.json`, finds the nearest
agent for every package, simulates the deliveries for the day, and prints
+ saves a report (`report.json`) showing packages delivered, total distance
travelled and efficiency for each agent, plus who the best performing agent
was.

## Files

- `delivery_system.py` - main program, everything is here
- `data.json` - sample input (the example given in the assignment doc)
- `report.json` - gets created after you run the program
- `tests/` - the 10 test cases given in the assignment, and a small script
  to run all of them at once

## How to run

Needs Python 3, no extra libraries required (only used `json` and `math`
which come built in).

```
python delivery_system.py
```

This will use `data.json` in the same folder by default. If you want to
try a different input file, just rename it to `data.json` or edit the
filename in the `main()` function at the bottom of `delivery_system.py`.

To run it against all 10 test cases at once:

```
cd tests
python test_all_cases.py
```

This prints how many packages were delivered for each test case and
confirms it matches the total number of packages (checking this was
mentioned in the assignment notes).

## Assumptions I made

The assignment doc wasn't 100% clear on a couple of things, so here is
what I assumed (also mentioned as comments in the code):

- **Nearest agent** = the agent whose current position is closest
  (straight line / Euclidean distance) to the package's warehouse.
- If an agent gets more than one package, I made them deliver the
  packages one after another, starting the next trip from where the last
  delivery ended (instead of going back to their starting point every
  time) - this made more sense to me since it's more realistic and more
  efficient.
- **Efficiency** = total distance / number of packages delivered
  (basically average distance per delivery, lower is better). I got this
  formula by checking the numbers in the example given in the assignment
  PDF.
- If an agent doesn't get any packages, their efficiency is just shown as
  0 instead of crashing the program with a divide by zero error.
- The two example files given (`base_case.json` and the 10 `test_case_*`
  files) actually use slightly different formats for warehouses/agents
  (one is a dictionary, the other is a list of objects) so I wrote the
  loading functions to handle both.

## Bonus feature

Added a simple ASCII map at the end of the output that shows roughly
where the warehouses (W), agents (A) and package destinations (.) are,
just as a visual extra since it was mentioned as a bonus idea in the
assignment.

## Author

Akshata kandgule

