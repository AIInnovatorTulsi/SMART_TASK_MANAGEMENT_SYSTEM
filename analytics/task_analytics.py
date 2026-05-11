import pandas as pd
import numpy as np
from models.models import Task

def generate_task_analytics():

    tasks = Task.query.all()

    data = []

    for task in tasks:
        data.append({
            "status": task.status
        })

    df = pd.DataFrame(data)

    total_tasks = len(df)

    completed_tasks = len(df[df['status'] == 'Completed'])

    pending_tasks = len(df[df['status'] == 'Pending'])

    completion_percentage = np.round(
        (completed_tasks / total_tasks) * 100,
        2
    ) if total_tasks > 0 else 0

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "completion_percentage": completion_percentage
    }