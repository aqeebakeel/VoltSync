from collections import deque

# 1. Define Task Parameters
class Task:
    def __init__(self, task_id, arrival_time, execution_time, deadline):
        self.task_id = task_id
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.deadline = deadline
        self.completion_time = 0
        self.is_completed = False

    def __repr__(self):
        return f"Task({self.task_id}, Arr:{self.arrival_time}, Exec:{self.execution_time}, Dead:{self.deadline})"

# 2. Define Energy Metrics (Wattage)
class EnergyState:
    SLEEP = 1.0       # Idle / Low-power sleep state
    LOW_FREQ = 5.0    # Throttled CPU for low-priority tasks
    MAX_FREQ = 15.0   # Maximum performance for strict deadlines

# 3. Implement Baseline Algorithms

def round_robin_scheduler(tasks, time_quantum):
    """Baseline Round Robin Scheduler for comparison."""
    time = 0
    queue = deque()
    completed_tasks = []
    task_idx = 0
    n = len(tasks)
    
    # Sort tasks by arrival time initially
    tasks.sort(key=lambda x: x.arrival_time)
    
    while len(completed_tasks) < n:
        # Add newly arrived tasks to the queue
        while task_idx < n and tasks[task_idx].arrival_time <= time:
            queue.append(tasks[task_idx])
            task_idx += 1
            
        if not queue:
            time += 1 # CPU is idle
            continue
            
        current_task = queue.popleft()
        
        # Execute for time quantum or remaining time, whichever is smaller
        execution_chunk = min(time_quantum, current_task.remaining_time)
        current_task.remaining_time -= execution_chunk
        time += execution_chunk
        
        # Check for new arrivals while the current task was executing
        while task_idx < n and tasks[task_idx].arrival_time <= time:
            queue.append(tasks[task_idx])
            task_idx += 1
            
        if current_task.remaining_time == 0:
            current_task.is_completed = True
            current_task.completion_time = time
            completed_tasks.append(current_task)
        else:
            queue.append(current_task) # Put back in queue if not finished
            
    return completed_tasks

def edf_scheduler(tasks):
    """Baseline Earliest Deadline First (EDF) Scheduler for comparison."""
    time = 0
    completed_tasks = []
    n = len(tasks)
    
    # Reset tasks in case they were modified by another simulation
    for t in tasks:
        t.remaining_time = t.execution_time
        t.is_completed = False
        
    while len(completed_tasks) < n:
        # Get all tasks that have arrived and are not completed
        available_tasks = [t for t in tasks if t.arrival_time <= time and not t.is_completed]
        
        if not available_tasks:
            time += 1 # CPU is idle
            continue
            
        # Pick the task with the earliest deadline
        current_task = min(available_tasks, key=lambda x: x.deadline)
        
        # Execute for 1 unit of time (preemptive)
        current_task.remaining_time -= 1
        time += 1
        
        if current_task.remaining_time == 0:
            current_task.is_completed = True
            current_task.completion_time = time
            completed_tasks.append(current_task)
            
    return completed_tasks

# --- Quick Test of Phase 1 ---
if __name__ == "__main__":
    # Create some dummy tasks: (ID, Arrival, Execution, Deadline)
    test_tasks = [
        Task("T1", 0, 4, 10),
        Task("T2", 1, 2, 5),
        Task("T3", 2, 1, 12)
    ]
    
    print("Running Baseline EDF Scheduler...")
    edf_results = edf_scheduler(test_tasks)
    for t in edf_results:
        missed = "Missed!" if t.completion_time > t.deadline else "Met"
        print(f"{t.task_id} completed at time {t.completion_time} | Deadline {t.deadline} ({missed})")



def calculate_metrics(completed_tasks, scheduler_name):
    total_tasks = len(completed_tasks)
    if total_tasks == 0:
        print("No tasks completed.")
        return

    total_tat = 0
    total_wt = 0
    missed_deadlines = 0

    print(f"\n--- Metrics for {scheduler_name} ---")
    print(f"{'Task ID':<10} | {'Turnaround Time':<18} | {'Waiting Time':<15} | {'Deadline Status'}")
    print("-" * 65)

    for t in completed_tasks:
        # Calculate Turnaround Time and Waiting Time
        tat = t.completion_time - t.arrival_time
        wt = tat - t.execution_time
        
        total_tat += tat
        total_wt += wt
        
        # Check Deadline Status
        status = "Met"
        if t.completion_time > t.deadline:
            missed_deadlines += 1
            status = "Missed"

        print(f"{t.task_id:<10} | {tat:<18} | {wt:<15} | {status}")

    # Calculate Averages
    avg_tat = total_tat / total_tasks
    avg_wt = total_wt / total_tasks
    miss_rate = (missed_deadlines / total_tasks) * 100

    print("-" * 65)
    print(f"Average Turnaround Time: {avg_tat:.2f} units")
    print(f"Average Waiting Time:    {avg_wt:.2f} units")
    print(f"Deadline Miss Rate:      {miss_rate:.2f}%")
    
    return avg_tat, avg_wt, miss_rate

# --- Updated Quick Test ---
if __name__ == "__main__":
    # Note: Define the Task class and edf_scheduler function from Phase 1 here
    
    test_tasks = [
        Task("T1", 0, 4, 10),
        Task("T2", 1, 2, 5),
        Task("T3", 2, 1, 12)
    ]
    
    # Run and evaluate the EDF Baseline
    edf_results = edf_scheduler(test_tasks)
    calculate_metrics(edf_results, "EDF Scheduler")