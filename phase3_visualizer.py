import matplotlib.pyplot as plt
from phase1_baselines import Task, EnergyState
from phase2_voltsync import voltsync_scheduler, edf_scheduler

def run_visualization():
    # 1. Setup Data
    tasks_edf = [Task("T1", 0, 4, 10), Task("T2", 1, 2, 5), Task("T3", 2, 1, 12)]
    tasks_vs  = [Task("T1", 0, 4, 10), Task("T2", 1, 2, 5), Task("T3", 2, 1, 12)]
    
    # Run Baseline
    edf_results = edf_scheduler(tasks_edf)
    edf_total_time = max([t.completion_time for t in edf_results])
    edf_active_time = sum([t.execution_time for t in tasks_edf])
    edf_energy = edf_total_time * EnergyState.MAX_FREQ
    edf_cpu_util = (edf_active_time / edf_total_time) * 100
    edf_tat = sum([t.completion_time - t.arrival_time for t in edf_results]) / len(edf_results)

    # Run VoltSync
    vs_results, power_log, vs_energy = voltsync_scheduler(tasks_vs)
    vs_total_time = len(power_log)
    vs_sleep_time = power_log.count(EnergyState.SLEEP)
    vs_cpu_util = ((vs_total_time - vs_sleep_time) / vs_total_time) * 100
    vs_tat = sum([t.completion_time - t.arrival_time for t in vs_results]) / len(vs_results)
    
    energy_saved_pct = ((edf_energy - vs_energy) / edf_energy) * 100
    time_steps = list(range(len(power_log)))
    
    # --- BUILD PLOTS ---
    fig = plt.figure(figsize=(14, 8))
    
    # Plot 1: Power vs Time Graph (Top Row, spanning all columns)
    ax1 = plt.subplot(2, 1, 1)
    ax1.step(time_steps, power_log, where='post', color='teal', linewidth=2)
    ax1.fill_between(time_steps, power_log, step='post', color='teal', alpha=0.2)
    ax1.set_title('VoltSync Scheduler: Dynamic Power State vs Time', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Time (Seconds)', fontsize=12)
    ax1.set_ylabel('Power Draw (Watts)', fontsize=12)
    ax1.set_yticks([1, 5, 15])
    ax1.set_yticklabels(['Sleep (1W)', 'Low Freq (5W)', 'Max Freq (15W)'])
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Plot 2: Energy Comparison (Bottom Left)
    ax2 = plt.subplot(2, 3, 4)
    labels = ['Baseline EDF', 'VoltSync']
    bars = ax2.bar(labels, [edf_energy, vs_energy], color=['#e74c3c', '#2ecc71'])
    ax2.set_title('Total Energy (Joules)', fontsize=12)
    # Add floating text for % saved!
    ax2.text(1, vs_energy + 2, f"-{energy_saved_pct:.1f}%!", ha='center', color='green', fontweight='bold')

    # Plot 3: Turnaround Time Comparison (Bottom Middle)
    ax3 = plt.subplot(2, 3, 5)
    ax3.bar(labels, [edf_tat, vs_tat], color=['#3498db', '#f1c40f'])
    ax3.set_title('Avg Turnaround Time (Sec)', fontsize=12)

    # Plot 4: CPU Utilization Comparison (Bottom Right)
    ax4 = plt.subplot(2, 3, 6)
    ax4.bar(labels, [edf_cpu_util, vs_cpu_util], color=['#9b59b6', '#34495e'])
    ax4.set_title('CPU Utilization (%)', fontsize=12)
    ax4.set_ylim(0, 110) # Set axis a bit higher than 100 for visual padding

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_visualization()