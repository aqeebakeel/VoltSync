# phase2_voltsync.py
from phase1_baselines import Task, EnergyState, edf_scheduler, calculate_metrics

def voltsync_scheduler(tasks):
    """Energy-Aware OS Scheduler (VoltSync)"""
    time = 0
    completed_tasks = []
    power_log = [] # Stores wattage at each second for our final graph
    total_energy = 0.0
    n = len(tasks)
    
    # Reset tasks for a fresh simulation run
    for t in tasks:
        t.remaining_time = float(t.execution_time)
        t.is_completed = False
        
    while len(completed_tasks) < n:
        available_tasks = [t for t in tasks if t.arrival_time <= time and not t.is_completed]
        
        # Requirement 1: Enter low-power sleep states when idle
        if not available_tasks:
            power_log.append(EnergyState.SLEEP)
            total_energy += EnergyState.SLEEP
            time += 1
            continue
            
        # Pick task with the earliest deadline
        current_task = min(available_tasks, key=lambda x: x.deadline)
        
        # Requirement 2 & 3: Dynamically scale CPU frequency & Batch/Throttle
        time_to_deadline = current_task.deadline - time
        
        # If deadline is dangerously close, blast it at MAX_FREQ
        if time_to_deadline <= current_task.remaining_time + 1:
            current_power = EnergyState.MAX_FREQ
            work_done = 1.0 # 100% processing speed
        else:
            # Loose deadline: drop to LOW_FREQ to save massive amounts of energy
            current_power = EnergyState.LOW_FREQ
            work_done = 0.5 # 50% processing speed due to lower clock speed
            
        current_task.remaining_time -= work_done
        power_log.append(current_power)
        total_energy += current_power
        time += 1
        
        if current_task.remaining_time <= 0:
            current_task.is_completed = True
            current_task.completion_time = time
            completed_tasks.append(current_task)
            
    return completed_tasks, power_log, total_energy

# --- Execution & Comparison ---
if __name__ == "__main__":
    # --- 1. Baseline EDF ---
    test_tasks = [
        Task("T1", 0, 4, 10),
        Task("T2", 1, 2, 5),
        Task("T3", 2, 1, 12)
    ]
    print("==================================================")
    print(" BASELINE TEST: Earliest Deadline First (EDF)")
    print("==================================================")
    edf_results = edf_scheduler(test_tasks)
    calculate_metrics(edf_results, "EDF Scheduler")
    
    # Calculate EDF CPU Utilization
    edf_total_time = max([t.completion_time for t in edf_results])
    edf_active_time = sum([t.execution_time for t in test_tasks])
    edf_cpu_util = (edf_active_time / edf_total_time) * 100
    edf_energy = edf_total_time * EnergyState.MAX_FREQ
    
    print(f"Total Energy Consumed: {edf_energy} Joules")
    print(f"CPU Utilization:       {edf_cpu_util:.2f}%\n")

    # --- 2. Energy-Aware VoltSync ---
    print("==================================================")
    print(" ENERGY-AWARE TEST: VoltSync Scheduler")
    print("==================================================")
    voltsync_tasks = [
        Task("T1", 0, 4, 10),
        Task("T2", 1, 2, 5),
        Task("T3", 2, 1, 12)
    ]
    voltsync_results, voltsync_power_log, voltsync_total_energy = voltsync_scheduler(voltsync_tasks)
    calculate_metrics(voltsync_results, "VoltSync Scheduler")
    
    # Calculate VoltSync CPU Utilization & Savings
    voltsync_total_time = len(voltsync_power_log)
    voltsync_sleep_time = voltsync_power_log.count(EnergyState.SLEEP)
    voltsync_cpu_util = ((voltsync_total_time - voltsync_sleep_time) / voltsync_total_time) * 100
    energy_saved_pct = ((edf_energy - voltsync_total_energy) / edf_energy) * 100
    
    print(f"\nTotal Energy Consumed: {voltsync_total_energy} Joules")
    print(f"Energy Savings:        {energy_saved_pct:.2f}% (Compared to Baseline)")
    print(f"CPU Utilization:       {voltsync_cpu_util:.2f}%")