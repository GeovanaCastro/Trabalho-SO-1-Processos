import threading
import time
import random
import matplotlib.pyplot as plt
from collections import deque

compilador_lock = threading.Lock()
compilador_cond = threading.Condition(compilador_lock)
fila_compilador = deque()

banco_de_dados = threading.Semaphore(2)

cont_compilacoes = [0] * 5
simulando = True

tempo_monitor = []
uso_compilador = []
uso_banco_de_dados = []

contador_lock = threading.Lock()
no_compilador = 0
no_banco = 0

def programador(id):
    global no_banco, no_compilador

    while simulando:
        time.sleep(random.uniform(1, 2)) # a thread pensa por um tempo aleatorio de 1 a 2 segundos

        banco_de_dados.acquire()
        with contador_lock:
            no_banco += 1

        # evita inanicao
        with compilador_cond:
            fila_compilador.append(id)
            while fila_compilador[0] != id:
                compilador_cond.wait()
            no_compilador += 1

        # compilando
        time.sleep(random.uniform(0.5, 1.5))
        cont_compilacoes[id] += 1

        # libera compilador
        with compilador_cond:
            fila_compilador.popleft()
            no_compilador -= 1
            compilador_cond.notify_all()

        # libara banco de dados
        banco_de_dados.release()
        with contador_lock:
            no_banco -= 1

def monitorar_uso():
    inicio = time.time()
    while simulando:
        tempo_atual = time.time() - inicio
        with contador_lock:
            uso_compilador.append(no_compilador)
            uso_banco_de_dados.append(no_banco)
        tempo_monitor.append(tempo_atual)
        time.sleep(0.1)

threads = [threading.Thread(target=programador, args=(i,)) for i in range(5)]
monitor = threading.Thread(target=monitorar_uso)

for t in threads:
    t.start()
monitor.start()

# tempo de simulação
time.sleep(60)
simulando = False

for t in threads:
    t.join(timeout=2)
monitor.join(timeout=2)

# grafico 1
programadores = [f"P{i}" for i in range(5)]
plt.figure(figsize=(8, 5))
barras = plt.bar(programadores, cont_compilacoes, color='skyblue')
plt.title("Compilações por Programador")
plt.xlabel("Programador")
plt.ylabel("Compilações")
plt.tight_layout()

for bar in barras:
    altura = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, altura + 0.1, f'{int(altura)}',
             ha='center', va='bottom', fontsize=10)
plt.savefig("compilacoes_por_programador.png")
plt.show()

# grafico 2
plt.figure(figsize=(10, 4))
plt.plot(tempo_monitor, uso_compilador, color='red', label='Compilador (máx 1)')
plt.title("Uso do Compilador ao Longo do Tempo")
plt.xlabel("Tempo (s)")
plt.ylabel("Uso")
plt.yticks([0, 1])
plt.legend()
plt.tight_layout()
plt.savefig("uso_compilador.png")
plt.show()

# grafico 3
plt.figure(figsize=(10, 4))
plt.plot(tempo_monitor, uso_banco_de_dados, color='green', label='Banco de Dados (máx 2)')
plt.title("Uso do Banco de Dados ao Longo do Tempo")
plt.xlabel("Tempo (s)")
plt.ylabel("Uso")
plt.yticks([0, 1, 2])
plt.legend()
plt.tight_layout()
plt.savefig("uso_banco_de_dados.png")
plt.show()
