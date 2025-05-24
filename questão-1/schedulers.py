# schedulers.py
import heapq

def fcfs(processes):
    processes = sorted(processes, key=lambda p: p.arrival_time)
    current_time = 0
    for p in processes:
        if p.arrival_time > current_time:
            current_time = p.arrival_time
        p.start_time = current_time
        p.finish_time = current_time + p.burst_time
        p.waiting_time = p.start_time - p.arrival_time
        p.execution_sequence.append(('exec', p.pid, p.start_time, p.finish_time))
        current_time = p.finish_time
    return processes

def sjf_nonpreemptive(processes):
    processes = sorted(processes, key=lambda p: p.arrival_time)
    current_time = 0
    ready_queue = []
    completed = []

    i = 0
    n = len(processes)
    while i < n or ready_queue:
        while i < n and processes[i].arrival_time <= current_time:
            heapq.heappush(ready_queue, (processes[i].burst_time, processes[i]))
            i += 1
        if ready_queue:
            burst, p = heapq.heappop(ready_queue)
            p.start_time = current_time
            p.finish_time = current_time + burst
            p.waiting_time = p.start_time - p.arrival_time
            p.execution_sequence.append(('exec', p.pid, p.start_time, p.finish_time))
            current_time = p.finish_time
            completed.append(p)
        else:
            # Se não há processos prontos, avança no tempo
            current_time = processes[i].arrival_time
    return completed

def round_robin(processes, quantum):
    processes = sorted(processes, key=lambda p: p.arrival_time)
    current_time = 0
    ready_queue = []
    completed = []

    i = 0
    n = len(processes)

    while i < n or ready_queue:
        # Adiciona processos que chegaram ao pronto
        while i < n and processes[i].arrival_time <= current_time:
            ready_queue.append(processes[i])
            i += 1

        if not ready_queue:
            # Se a fila estiver vazia, pula no tempo até o próximo processo chegar
            current_time = processes[i].arrival_time
            continue

        current_process = ready_queue.pop(0)
        if current_process.start_time is None:
            current_process.start_time = current_time

        run_time = min(current_process.remaining_time, quantum)
        start_exec = current_time
        current_process.remaining_time -= run_time
        end_exec = current_time + run_time
        current_process.execution_sequence.append(('exec', current_process.pid, start_exec, end_exec))
        current_time = end_exec

        # Incrementa a espera dos processos na fila
        for p in ready_queue:
            p.waiting_time += run_time

        if current_process.remaining_time == 0:
            current_process.finish_time = current_time
            completed.append(current_process)
        else:
            # Ainda não finalizado, volta para fila
            ready_queue.append(current_process)

        # Tempo de troca de contexto
        current_time += 1
        # Incrementa espera para processos na fila por mudança de contexto
        for p in ready_queue:
            p.waiting_time += 1

    return completed