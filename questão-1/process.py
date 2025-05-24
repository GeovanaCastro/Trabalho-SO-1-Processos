# process.py
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.finish_time = None
        self.waiting_time = 0
        self.execution_sequence = []  # Para registrar sequência de execução

    def __lt__(self, other):
        # Pode escolher o critério, por exemplo, burst_time
        return self.burst_time < other.burst_time
