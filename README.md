# Realtime-NMR-Multicore-MixedCriticality-Scheduler
Sharif University of Technology - Real Time Systems project

## Usage
```shell
python main.py <config_number> <mode>
```
the mode argument is optional and can be either `debug` or `report`.
If the mode is `debug`, the program will print the results to the console.
If the mode is `report`, the program will generate two csv reports in the `reports` folder. One for the tasks and one for the core assignments.
the name of the report will correspond to the config file and the assignment method used for the tasks.

## Config
The config file is a YML file that contains the following fields:
- `random_seed`: The seed used for generating random numbers. (Optional for consistent results)
- `num_of_tasks`: Number of tasks to be generated
- `ratio`: Ratio of the number of high criticality tasks to the number of low criticality tasks
- `num_of_cores`: Number of cores in the system
- `core_utilization`: Utilization of each core
- `periods`: A list of periods for the tasks (chosen uniformly at random)
- `mu_range`: the minimum and maximum values for the mu parameter in the UUniFast algorithm
- `overrun_percentage`: The percentage of cores that are in overrun state
- `error_rate`: The error rate of the system (what percentage of cores might fail their tasks)
- `reliability`: The required reliability of the system 
- `assignment_policy`: The policy used for assigning tasks to cores. (`WFD` or `FFD`)
- `scheduling_policy`: The policy used for scheduling the tasks. (Only `EDF-VD` has been implemented)


## UUniFast task generation
Task generation based on the UUniFast algorithm is done based on [This Paper](https://sharif.edu/~ansari/pdfs/LETR-MC.pdf)
Since we are using NMR, the utilization generated for HC tasks is divided by the number of copies needed to achieve the required reliability.


## Calculating the number of copies needed to ensure reliability
using this formula:
```
N = ceil(-log(1 - R) / log(P)) if P ≠ 0, else 0
```
The number of copies we need for a task with failure rate of P to achieve reliability of R is calculated.

## Task Assignment
The tasks are assigned to cores based on the chosen policy. The policies implemented are `WFD` and `FFD`.