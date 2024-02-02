import matplotlib.pyplot as plt
import random
from typing import Dict, Tuple, List

import tasks


def generate_random_color():
    # Generate random RGB values between 0 and 1
    forbidden_colors = [
        (0, 0, 0),
        (255, 0, 0)
    ]
    # colors should be between 50 and 255
    color = (
        random.randint(50, 255) / 255,
        random.randint(50, 255) / 255,
        random.randint(50, 255) / 255
    )

    return color


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
    # fig, ax = plt.subplots(figsize=(600, 25))
    fig, ax = plt.subplots()
    ax.set_xlabel('Time')
    ax.set_ylabel('Core')

    # Set y-ticks for the cores
    ax.set_yticks(list(core_number_dict.values()))
    ax.invert_yaxis()

    for core in cores:
        # Plot the overrun and failure times
        core_number = core_number_dict[core]
        if core in core_overruns:
            overrun_time = core_overruns[core]
            ax.annotate('OVR', xy=(overrun_time, core_number),
                        xytext=(overrun_time + 1, core_number - 0.6),
                        arrowprops=dict(arrowstyle='-', color='red'), color='red', va='baseline')
        if core in core_failures:
            overrun_time = core_failures[core]
            ax.annotate('FAIL', xy=(overrun_time, core_number),
                        xytext=(overrun_time + 1, core_number - 0.6),
                        arrowprops=dict(arrowstyle='-', color='red'), color='red', va='baseline')

    # Plot the tasks as horizontal bars
    for job in jobs:

        if job.task not in task_colors:
            task_colors[job.task] = generate_random_color()
        color = task_colors[job.task]
        if job.is_failed:
            color = (0.2, 0.2, 0.2)
        core = job.task.core
        core_number = core_number_dict[core]
        if job.start_time is not None:
            start_time = job.start_time
            end_time = job.end_time
            ax.barh(core_number, end_time - start_time, left=start_time, height=0.5, align='center', color=color)

            duration = end_time - start_time
            label = f"{job} ({duration})"
            label_x = start_time + duration / 2
            label_y = core_number
            ax.text(label_x, label_y - 0.1, label, ha='center', va='center', color=get_appropriate_text_color(*color))

        # Add release time arrow
        release_time = job.release_time
        ax.annotate('', xy=(release_time, core_number - 0.6), xytext=(release_time, core_number),
                    arrowprops=dict(arrowstyle='->', color=color), va='center_baseline')

        # Add deadline arrow
        deadline = job.deadline
        ax.annotate('', xy=(deadline, core_number - 0.6), xytext=(deadline, core_number),
                    arrowprops=dict(arrowstyle='<-', color=color), va='baseline')

        if job.deadline_missed_time:
            ax.annotate('X', xy=(job.deadline_missed_time, core_number),
                        xytext=(job.deadline_missed_time + 1, core_number - 0.6),
                        arrowprops=dict(arrowstyle='-', color='red', linewidth=2), color='red', va='baseline')

    # Set x-ticks and limits
    ax.set_xticks(range(0, total_time + 1, 10))
    ax.set_xlim(0, total_time)

    # Show the grid
    ax.grid(True)

    # Show the plot
    plt.show()
