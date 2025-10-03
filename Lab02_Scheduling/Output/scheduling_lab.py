# scheduling_lab.py
from collections import deque
import copy

class Process:
    def __init__(self, pid, at, bt):
        self.pid = pid
        self.at = int(at)
        self.bt = int(bt)
        self.rem = int(bt)
        self.ct = None
        self.tat = None
        self.wt = None

def compute_metrics(processes):
    for p in processes:
        p.tat = p.ct - p.at
        p.wt = p.tat - p.bt
    avg_tat = sum(p.tat for p in processes) / len(processes)
    avg_wt = sum(p.wt for p in processes) / len(processes)
    return avg_tat, avg_wt

def print_table(processes):
    print("\nOutput Table:")
    print(f"{'Process':^8}{'AT':^8}{'BT':^8}{'CT':^8}{'TAT':^8}{'WT':^8}")
    # keep original PID order (P1,P2,...). Sort by pid numeric part:
    procs_sorted = sorted(processes, key=lambda x: int(x.pid[1:]))
    for p in procs_sorted:
        print(f"{p.pid:^8}{p.at:^8}{p.bt:^8}{p.ct:^8}{p.tat:^8}{p.wt:^8}")

def print_gantt(schedule):
    # schedule: list of tuples (pid|'idle', start, end)
    labels = [seg[0] for seg in schedule]
    times = []
    if schedule:
        times.append(schedule[0][1])
        for seg in schedule:
            times.append(seg[2])
    # Gantt top row
    row = "| " + " | ".join(labels) + " |"
    print("\nGantt Chart:")
    print(row)
    # times row (simple)
    print(" ".join(str(t) for t in times))

def reset_processes_from_input(process_list):
    # process_list is list of tuples (pid, at, bt)
    return [Process(pid, at, bt) for pid, at, bt in process_list]

# --- FCFS ---
def fcfs(process_list):
    procs = reset_processes_from_input(process_list)
    procs_sorted = sorted(procs, key=lambda p: (p.at, int(p.pid[1:])))
    schedule = []
    current = 0
    for p in procs_sorted:
        if current < p.at:
            schedule.append(("idle", current, p.at))
            current = p.at
        start = current
        current += p.bt
        p.ct = current
        schedule.append((p.pid, start, current))
    avg_tat, avg_wt = compute_metrics(procs_sorted)
    return procs_sorted, schedule, avg_tat, avg_wt

# --- SJF Non-preemptive ---
def sjf_nonpreemptive(process_list):
    procs = reset_processes_from_input(process_list)
    n = len(procs)
    procs_sorted = sorted(procs, key=lambda p: (p.at, int(p.pid[1:])))
    schedule = []
    current = 0
    completed = 0
    # mark ct None as unfinished
    while completed < n:
        ready = [p for p in procs_sorted if p.ct is None and p.at <= current]
        if not ready:
            # jump to next arrival
            next_at = min(p.at for p in procs_sorted if p.ct is None)
            if current < next_at:
                schedule.append(("idle", current, next_at))
                current = next_at
            ready = [p for p in procs_sorted if p.ct is None and p.at <= current]
        # pick shortest BT among ready
        p = min(ready, key=lambda x: (x.bt, x.at, int(x.pid[1:])))
        start = current
        current += p.bt
        p.ct = current
        schedule.append((p.pid, start, current))
        completed += 1
    avg_tat, avg_wt = compute_metrics(procs_sorted)
    return procs_sorted, schedule, avg_tat, avg_wt

# --- Round Robin ---
def round_robin(process_list, quantum):
    procs = reset_processes_from_input(process_list)
    procs_sorted = sorted(procs, key=lambda p: (p.at, int(p.pid[1:])))
    n = len(procs_sorted)
    schedule = []
    current = 0
    q = deque()
    i = 0  # next index to enqueue based on arrival
    # enqueue any that arrive at time 0
    while i < n and procs_sorted[i].at <= current:
        q.append(procs_sorted[i]); i += 1
    if not q and i < n:
        # jump to first arrival
        current = procs_sorted[0].at
        q.append(procs_sorted[0]); i = 1
    while q:
        p = q.popleft()
        start = current
        run = min(quantum, p.rem)
        current += run
        p.rem -= run
        schedule.append((p.pid, start, current))
        # enqueue newly arrived processes during this time slice
        while i < n and procs_sorted[i].at <= current:
            q.append(procs_sorted[i]); i += 1
        if p.rem > 0:
            q.append(p)
        else:
            p.ct = current
        # if queue empty but not all finished, fast forward
        if not q and any(x.ct is None for x in procs_sorted):
            # jump to next arrival
            next_at = min(x.at for x in procs_sorted if x.ct is None)
            if current < next_at:
                schedule.append(("idle", current, next_at))
                current = next_at
            while i < n and procs_sorted[i].at <= current:
                q.append(procs_sorted[i]); i += 1
    avg_tat, avg_wt = compute_metrics(procs_sorted)
    return procs_sorted, schedule, avg_tat, avg_wt

# Example driver (sample input from screenshots)
if __name__ == "__main__":
    # define processes: list of (pid, AT, BT)
    process_input = [("P1",0,5), ("P2",1,3), ("P3",2,8)]

    print("=== FCFS ===")
    procs, schedule, avg_tat, avg_wt = fcfs(process_input)
    print_table(procs)
    print(f"\nAverage TAT = {avg_tat:.2f}")
    print(f"Average WT  = {avg_wt:.2f}")
    print_gantt(schedule)

    print("\n=== SJF (non-preemptive) ===")
    procs, schedule, avg_tat, avg_wt = sjf_nonpreemptive(process_input)
    print_table(procs)
    print(f"\nAverage TAT = {avg_tat:.2f}")
    print(f"Average WT  = {avg_wt:.2f}")
    print_gantt(schedule)

    print("\n=== Round Robin (quantum=2) ===")
    procs, schedule, avg_tat, avg_wt = round_robin(process_input, quantum=2)
    print_table(procs)
    print(f"\nAverage TAT = {avg_tat:.2f}")
    print(f"Average WT  = {avg_wt:.2f}")
    print_gantt(schedule)
