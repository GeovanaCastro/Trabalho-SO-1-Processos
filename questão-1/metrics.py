import statistics

def calculate_metrics(processes):
    if not processes:
        return {}
    turnaround_times = [p.finish_time - p.arrival_time for p in processes]
    waiting_times = [p.waiting_time for p in processes]
    total_time = max(p.finish_time for p in processes) - min(p.arrival_time for p in processes)
    throughput = len(processes) / total_time if total_time > 0 else 0

    return {
        'avg_waiting': sum(waiting_times) / len(waiting_times),
        'std_waiting': statistics.stdev(waiting_times) if len(waiting_times) > 1 else 0,
        'avg_turnaround': sum(turnaround_times) / len(turnaround_times),
        'std_turnaround': statistics.stdev(turnaround_times) if len(turnaround_times) > 1 else 0,
        'throughput': throughput
    }