# Realtime-NMR-Multicore-MixedCriticality-Scheduler
Sharif University of Technology - Real Time Systems project

## Usage
```shell
python main.py <config_number>
```

## UUniFast task generation
Task generation based on the UUniFast algorithm is done based on [This Paper](https://sharif.edu/~ansari/pdfs/LETR-MC.pdf)

## Config
The config file is a YML file that contains the following fields:
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
