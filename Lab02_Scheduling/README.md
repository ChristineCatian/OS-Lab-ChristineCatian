# CPU Scheduling Algorithms (FCFS, SJF, RR)

This laboratory implements three fundamental CPU scheduling algorithms in Python:  
- **FCFS (First-Come, First-Served)**  
- **SJF (Shortest Job First)**  
- **RR (Round Robin)**  

The goal is to simulate how these algorithms schedule processes in an operating system and calculate essential metrics such as **Completion Time (CT)**, **Turnaround Time (TAT)**, and **Waiting Time (WT)**.

---

## First-Come, First-Served (FCFS)

**First-Come, First-Served (FCFS)** is the simplest CPU scheduling algorithm in operating systems, where processes are executed in the exact order they arrive in the ready queue. In this method, the process that arrives first is served first, and once it starts executing, it runs until it is finished without being interrupted. This approach is similar to a queue at a ticket counter, where each customer is served one at a time based on their arrival order. FCFS is easy to implement and considered fair since every process gets its turn in sequence. However, it has some drawbacks, such as the **convoy effect**, where shorter processes have to wait for longer processes to complete, which can increase the average waiting time. Despite its simplicity and fairness, FCFS is not always the most efficient scheduling method, especially in systems where response time and resource utilization are critical.

### Sample Output (FCFS)
![FCFS Output](https://github.com/ChristineCatian/OS-Lab-ChristineCatian/blob/ebb24532a4649a90fb7c45ebab935b0bc8a004e7/Lab02_Scheduling/Output/FCFS.png)

---

## Shortest Job First (SJF)

**Shortest Job First (SJF)** is a CPU scheduling algorithm that selects the process with the shortest burst time or execution time to run next. It operates on the principle that shorter jobs should be executed before longer ones, which helps minimize the average waiting time and improve overall system efficiency. SJF can be either **non-preemptive**, where a process runs to completion once it starts, or **preemptive** (also known as *Shortest Remaining Time First*), where a newly arrived process with a shorter burst time can interrupt the current one.

### Sample Output (SJF)
![SJF Output](https://github.com/ChristineCatian/OS-Lab-ChristineCatian/blob/ebb24532a4649a90fb7c45ebab935b0bc8a004e7/Lab02_Scheduling/Output/SJF%20(non-preemptive).png)

---

## Round Robin (RR)

**Round Robin (RR)** is a preemptive CPU scheduling algorithm that assigns each process a fixed time slice, called a **time quantum**, and executes them in a cyclic order. When a process’s time quantum expires before it finishes execution, it is placed at the end of the ready queue, and the next process is given CPU time. This cycle continues until all processes are completed. Round Robin is designed to provide **fairness** and **responsive multitasking**, making it one of the most widely used scheduling methods in time-sharing systems.

### Sample Output (RR)
![Round Robin Output](https://github.com/ChristineCatian/OS-Lab-ChristineCatian/blob/ebb24532a4649a90fb7c45ebab935b0bc8a004e7/Lab02_Scheduling/Output/Round%20Robin%20(quantum%3D2).png)

---

This laboratory demonstrates how different CPU scheduling algorithms work and how they affect process execution order, turnaround time, and waiting time. Each algorithm has unique strengths and trade-offs, and understanding them is essential for designing efficient and fair operating systems.




