import random
from process import Process
from schedulers import fcfs, sjf_nonpreemptive, round_robin
from metrics import calculate_metrics
import matplotlib.pyplot as plt


def generate_processes(n):
    arrival_times = sorted(random.sample(range(0, n * 3), n))
    burst_times = [random.randint(5, 800) for _ in range(n)]
    return [Process(i + 1, arrival_times[i], burst_times[i]) for i in range(n)]

def print_metrics(metrics):
    print(f"Tempo médio de espera: {metrics['avg_waiting']:.2f} ± {metrics['std_waiting']:.2f}")
    print(f"Tempo médio de retorno: {metrics['avg_turnaround']:.2f} ± {metrics['std_turnaround']:.2f}")
    print(f"Vazão: {metrics['throughput']:.2f}")

# Função para plotar os gráficos

def plot_metrics(metric_name, labels, values, errors=None):
    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, values, yerr=errors, capsize=5)
    plt.ylabel(metric_name)
    plt.title(f"Comparação de {metric_name}")
    plt.grid(axis='y')

    # Adiciona o valor de cada barra acima dela
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + (max(values) * 0.01),  # posiciona um pouco acima do topo da barra
            f'{values[i]:.2f}',
            ha='center',
            va='bottom'
        )
    plt.show()

def main():
    N = 10000
    process_list = generate_processes(N)
    print("Processos gerados:")
    for p in process_list:
        print(f"Processo {p.pid}: Chegada={p.arrival_time}, Burst={p.burst_time}")

    print("\n--- Executando FCFS ---")
    fcfs_result = fcfs([Process(p.pid, p.arrival_time, p.burst_time) for p in process_list])
    fcfs_metrics = calculate_metrics(fcfs_result)

    print("\n--- Executando SJF não preemptivo ---")
    sjf_result = sjf_nonpreemptive([Process(p.pid, p.arrival_time, p.burst_time) for p in process_list])
    sjf_metrics = calculate_metrics(sjf_result)

    print("\n--- Executando Round Robin ---")
    quantums = [5, 200, 800]
    rr_metrics_list = []
    for q in quantums:
        rr_result = round_robin([Process(p.pid, p.arrival_time, p.burst_time) for p in process_list], q)
        rr_metrics = calculate_metrics(rr_result)
        rr_metrics_list.append(rr_metrics)

    # Preparar para os gráficos
    labels = ['FCFS', 'SJF', 'RR q=5', 'RR q=200', 'RR q=800']

    # Gráfico de Tempo Médio de Espera
    avg_waitings = [
        fcfs_metrics['avg_waiting'],
        sjf_metrics['avg_waiting'],
        rr_metrics_list[0]['avg_waiting'],
        rr_metrics_list[1]['avg_waiting'],
        rr_metrics_list[2]['avg_waiting']
    ]
    errors_waiting = [
        fcfs_metrics['std_waiting'],
        sjf_metrics['std_waiting'],
        rr_metrics_list[0]['std_waiting'],
        rr_metrics_list[1]['std_waiting'],
        rr_metrics_list[2]['std_waiting']
    ]
    plot_metrics("Tempo Médio de Espera", labels, avg_waitings, errors_waiting)

    # Gráfico de Tempo Médio de Retorno
    avg_turnarounds = [
        fcfs_metrics['avg_turnaround'],
        sjf_metrics['avg_turnaround'],
        rr_metrics_list[0]['avg_turnaround'],
        rr_metrics_list[1]['avg_turnaround'],
        rr_metrics_list[2]['avg_turnaround']
    ]
    errors_turnaround = [
        fcfs_metrics['std_turnaround'],
        sjf_metrics['std_turnaround'],
        rr_metrics_list[0]['std_turnaround'],
        rr_metrics_list[1]['std_turnaround'],
        rr_metrics_list[2]['std_turnaround']
    ]
    plot_metrics("Tempo Médio de Retorno", labels, avg_turnarounds, errors_turnaround)

    # Gráfico de Vazão
    throughputs = [
        fcfs_metrics['throughput'],
        sjf_metrics['throughput'],
        rr_metrics_list[0]['throughput'],
        rr_metrics_list[1]['throughput'],
        rr_metrics_list[2]['throughput']
    ]
    errors_throughput = [0, 0, 0, 0, 0]  # Sem desvio padrão para vazão
    plot_metrics("Vazão", labels, throughputs, errors_throughput)

if __name__ == "__main__":
    main()