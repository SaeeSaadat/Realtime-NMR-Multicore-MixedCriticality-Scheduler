import csv
from typing import List

from tasks import *


def report(config: ProjectConfig, cores: List[Processor], generated_tasks: List[Task]):
    with open(f'reports/{config.config_name}-tasks-report.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Task Name', 'Period', 'Criticality', 'WCET-HI', 'WCET-LO', 'Utilization'])
        for t in generated_tasks:
            if isinstance(t, LowCriticalityTask):
                writer.writerow([t.name, t.period, 'LC', t.wcet, None, t.utilization])
            elif isinstance(t, HighCriticalityTask):
                writer.writerow([t.name, t.period, 'HC', t.wcet, t.wcet_lo, t.utilization])
    with open(f'reports/{config.config_name}-assignment-report.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Core Name', 'Task Name', 'Period', 'WCET', 'Utilization'])
        for c in cores:
            for t in c.tasks:
                writer.writerow([c.name, t.name, t.period, t.wcet, t.utilization])
            writer.writerow([c.name, None, None, None, c.utilization()])