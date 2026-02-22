# VoltSync: Energy-Aware OS Scheduler
An intelligent, energy-efficient CPU scheduling algorithm designed for battery-powered embedded devices (IoT, medical wearables, Edge AI diagnostic appliances).

### Features
* **Dynamic Voltage and Frequency Scaling (DVFS):** Scales CPU frequency based on strictness of task deadlines.
* **Task Batching:** Throttles down processing speed (5.0W) for low-priority tasks to conserve battery.
* **Sleep States:** Enters a low-power idle state (1.0W) when the queue is empty.

### Results
Compared to a standard Earliest Deadline First (EDF) scheduler running at maximum frequency, VoltSync achieved a **19.05% reduction in total energy consumption** while maintaining a 0.00% deadline miss rate.

### Tech Stack
* **Language:** Python
* **Visualization:** Matplotlib