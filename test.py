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


def plot_gantt_chart(jobs: List[tasks.TaskInstance], core_overruns: dict, core_failures: dict):
    task_colors: Dict[tasks.Task, Tuple[float, float, float]] = {}

    # Set up the figure and axis
    fig, ax = plt.subplots()
    ax.set_xlabel('Time')
    ax.set_ylabel('Core')

    # Set y-ticks for the cores
    ax.set_yticks(range(1, num_cores + 1))
    ax.invert_yaxis()

    # Plot the tasks as horizontal bars
    for job in jobs:
        if job.task not in task_colors:
            task_colors[job.task] = generate_random_color()
        color = task_colors[job.task]
        core = job.task.core
        start_time = job.start_time
        end_time = job.end_time
        ax.barh(core, end_time - start_time, left=start_time, height=0.5, align='center', color=color)

        duration = end_time - start_time
        label = f"{job} ({duration})"
        label_x = start_time + duration / 2
        label_y = core
        ax.text(label_x, label_y, label, ha='center', va='center', color=get_appropriate_text_color(*color))

        # Add release time arrow
        release_time = job.release_time
        ax.annotate('', xy=(release_time, core - 0.4), xytext=(release_time, core),
                    arrowprops=dict(arrowstyle='->', color=color), va='center_baseline')

        # Add deadline arrow
        deadline = job.deadline
        ax.annotate('', xy=(deadline, core - 0.4), xytext=(deadline, core),
                    arrowprops=dict(arrowstyle='<-', color=color), va='baseline')

    # Set x-ticks and limits
    ax.set_xticks(range(0, total_time + 1, 10))
    ax.set_xlim(0, total_time)

    # Show the grid
    ax.grid(True)

    # Show the plot
    plt.show()


if __name__ == '__main__':
    # Example usage
    tasks = [
        {'core': 1, 'start_time': 0, 'end_time': 20, 'label': 'task1', 'release_time': 0, 'deadline': 10},
        {'core': 2, 'start_time': 5, 'end_time': 25, 'label': 'task2', 'release_time': 0, 'deadline': 35},
        {'core': 1, 'start_time': 15, 'end_time': 30, 'label': 'task3', 'release_time': 13, 'deadline': 40},
        {'core': 3, 'start_time': 25, 'end_time': 35, 'label': 'task4', 'release_time': 10, 'deadline': 30},
    ]
    num_cores = 3
    total_time = 40
    plot_gantt_chart(tasks, num_cores, total_time)
