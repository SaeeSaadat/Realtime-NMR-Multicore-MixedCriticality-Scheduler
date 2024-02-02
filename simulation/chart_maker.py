import matplotlib.pyplot as plt
import random
from typing import Dict, Tuple, List

import tasks


def generate_random_color():
    # Generate random RGB values between 0 and 1
    return (
        random.random(),
        random.random(),
        random.random()
    )


def get_appropriate_text_color(r, g, b):
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return 'black' if brightness > 0.5 else 'white'


def plot_gantt_chart(
        total_time: int,
        jobs: List[tasks.TaskInstance],
        cores: List[tasks.Processor],
        core_overruns: dict,
        core_failures: dict
):
    task_colors: Dict[tasks.Task, Tuple[float, float, float]] = {}
    core_number_dict = {core: i for i, core in enumerate(cores)}

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(100, 25))
    ax.set_xlabel('Time')
    ax.set_ylabel('Core')

    # Set y-ticks for the cores
    ax.set_yticks(list(core_number_dict.values()))
    ax.invert_yaxis()

    # Plot the tasks as horizontal bars
    for job in jobs:
        if job.start_time is None:
            continue

        if job.task not in task_colors:
            task_colors[job.task] = generate_random_color()
        color = task_colors[job.task]
        core = job.task.core
        core_number = core_number_dict[core]
        start_time = job.start_time
        end_time = job.end_time
        ax.barh(core_number, end_time - start_time, left=start_time, height=0.5, align='center', color=color)

        duration = end_time - start_time
        label = f"{job} ({duration})"
        label_x = start_time + duration / 2
        label_y = core_number
        ax.text(label_x, label_y, label, ha='center', va='center', color=get_appropriate_text_color(*color))

        # Add release time arrow
        release_time = job.release_time
        ax.annotate('', xy=(release_time, core_number - 0.4), xytext=(release_time, core_number),
                    arrowprops=dict(arrowstyle='->', color=color), va='center_baseline')

        # Add deadline arrow
        deadline = job.deadline
        ax.annotate('', xy=(deadline, core_number - 0.4), xytext=(deadline, core_number),
                    arrowprops=dict(arrowstyle='<-', color=color), va='baseline')

    # Set x-ticks and limits
    ax.set_xticks(range(0, total_time + 1, 10))
    ax.set_xlim(0, total_time)

    # Show the grid
    ax.grid(True)

    # Show the plot
    plt.show()
