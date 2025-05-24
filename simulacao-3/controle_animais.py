import threading
import time
import random
import matplotlib.pyplot as plt

# Classe SalaRepouso com alternância para evitar starvation
class SalaRepouso:
    def __init__(self):
        self.lock = threading.Lock()
        self.condicao = threading.Condition(self.lock)
        self.cachorros_na_sala = 0
        self.gatos_na_sala = 0
        self.proximo_grupo = 'cachorro'  # Grupo que tem prioridade para entrar

    def dogWantsToEnter(self, id):
        with self.condicao:
            while self.gatos_na_sala > 0 or self.proximo_grupo != 'cachorro':
                self.condicao.wait()
            self.cachorros_na_sala += 1
            print(f"Cachorro {id} entrou. Cachorros na sala: {self.cachorros_na_sala}")

    def dogLeaves(self, id):
        with self.condicao:
            self.cachorros_na_sala -= 1
            print(f"Cachorro {id} saiu. Cachorros na sala: {self.cachorros_na_sala}")
            if self.cachorros_na_sala == 0:
                # Passa a vez para os gatos quando cachorros saem todos
                self.proximo_grupo = 'gato'
                self.condicao.notify_all()

    def catWantsToEnter(self, id):
        with self.condicao:
            while self.cachorros_na_sala > 0 or self.proximo_grupo != 'gato':
                self.condicao.wait()
            self.gatos_na_sala += 1
            print(f"Gato {id} entrou. Gatos na sala: {self.gatos_na_sala}")

    def catLeaves(self, id):
        with self.condicao:
            self.gatos_na_sala -= 1
            print(f"Gato {id} saiu. Gatos na sala: {self.gatos_na_sala}")
            if self.gatos_na_sala == 0:
                # Passa a vez para os cachorros quando gatos saem todos
                self.proximo_grupo = 'cachorro'
                self.condicao.notify_all()


def cachorro(sala, id, eventos, start_time):
    time.sleep(random.uniform(0.5, 2.0))
    sala.dogWantsToEnter(id)
    entrada = time.time() - start_time
    eventos.append(('cachorro', id, 'entra', entrada))
    time.sleep(random.uniform(2, 4))
    saida = time.time() - start_time
    eventos.append(('cachorro', id, 'sai', saida))
    sala.dogLeaves(id)


def gato(sala, id, eventos, start_time):
    time.sleep(random.uniform(0.5, 2.0))
    sala.catWantsToEnter(id)
    entrada = time.time() - start_time
    eventos.append(('gato', id, 'entra', entrada))
    time.sleep(random.uniform(1, 5))
    saida = time.time() - start_time
    eventos.append(('gato', id, 'sai', saida))
    sala.catLeaves(id)


if __name__ == "__main__":
    sala = SalaRepouso()
    threads = []
    eventos = []
    num_cachorros = 10
    num_gatos = 10
    start_time = time.time()

    for i in range(num_cachorros):
        t = threading.Thread(target=cachorro, args=(sala, i, eventos, start_time))
        threads.append(t)
    for i in range(num_gatos):
        t = threading.Thread(target=gato, args=(sala, i, eventos, start_time))
        threads.append(t)

    random.shuffle(threads)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("\nSimulação concluída.")

    eventos.sort(key=lambda x: x[3])  # Ordena os eventos pelo tempo

    tempo = []
    ocupacao_cachorros = []
    ocupacao_gatos = []

    current_cachorros = 0
    current_gatos = 0

    for evento in eventos:
        especie, id, acao, t = evento
        tempo.append(t)

        if especie == 'cachorro':
            if acao == 'entra':
                current_cachorros += 1
            else:
                current_cachorros -= 1
        elif especie == 'gato':
            if acao == 'entra':
                current_gatos += 1
            else:
                current_gatos -= 1

        ocupacao_cachorros.append(current_cachorros)
        ocupacao_gatos.append(current_gatos)

    plt.figure(figsize=(10, 6))
    plt.step(tempo, ocupacao_cachorros, where='post', label='Cachorros na sala', color='blue')
    plt.step(tempo, ocupacao_gatos, where='post', label='Gatos na sala', color='red')
    plt.title('Ocupação da sala de repouso ao longo do tempo')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Número de animais na sala')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
