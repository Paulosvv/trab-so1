# ==============================================================
# Simulador de Escalonamento de Processos
# Sistemas Operacionais - IFRS Campus Restinga - ADS 3N - 2026/2
# Autor: Paulo
#
# DECLARACAO DE USO DE IA GENERATIVA (exigencia da secao 6 do enunciado):
# IA utilizada: Claude (Anthropic).
# Onde: nas funcoes SJF(), PRIORIDADE(), Round_Robin() e proximo_processo(),
#       marcadas com o comentario "[IA]".
# Para que fim: escrever a logica de escolha do processo em cada instante
#       de tempo, seguindo o modelo do FCFS ja' fornecido no codigo-base.
# O restante do arquivo e' o codigo-base do professor.
# ==============================================================

import random

MAXIMO_TEMPO_EXECUCAO = 65535

n_processos = 3

QUANTUM = 2  # [IA] fatia de tempo usada pelo Round-Robin


def main():
    tempo_execucao = [0] * n_processos
    tempo_chegada = [0] * n_processos
    prioridade = [0] * n_processos
    tempo_espera = [0] * n_processos
    tempo_restante = [0] * n_processos

    popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

    imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

    # Escolher algoritmo
    while True:
        alg = int(input(
            "Escolha o algoritmo?: [1=FCFS 2=SJF Preemptivo 3=SJF Nao Preemptivo  "
            "4=Prioridade Preemptivo 5=Prioridade Nao Preemptivo  6=Round_Robin  "
            "7=Imprime lista de processos 8=Popular processos novamente 9=Sair]: "))

        if alg == 1:  # FCFS
            FCFS(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        elif alg == 2:  # SJF PREEMPTIVO
            SJF(True, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        elif alg == 3:  # SJF NAO PREEMPTIVO
            SJF(False, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        elif alg == 4:  # PRIORIDADE PREEMPTIVO
            PRIORIDADE(True, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

        elif alg == 5:  # PRIORIDADE NAO PREEMPTIVO
            PRIORIDADE(False, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

        elif alg == 6:  # Round_Robin
            Round_Robin(tempo_execucao, tempo_espera, tempo_restante)

        elif alg == 7:  # IMPRIME CONTEUDO INICIAL DOS PROCESSOS
            imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

        elif alg == 8:  # REATRIBUI VALORES INICIAIS
            popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)
            imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

        elif alg == 9:
            break


def popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
    aleatorio = int(input("Sera aleatorio?:  "))

    for i in range(n_processos):
        # Popular Processos Aleatorio
        if aleatorio == 1:
            tempo_execucao[i] = random.randint(1, 10)
            tempo_chegada[i] = random.randint(1, 10)
            prioridade[i] = random.randint(1, 15)
        # Popular Processos Manual
        else:
            tempo_execucao[i] = int(input("Digite o tempo de execucao do processo[" + str(i) + "]:  "))
            tempo_chegada[i] = int(input("Digite o tempo de chegada do processo[" + str(i) + "]:  "))
            prioridade[i] = int(input("Digite a prioridade do processo[" + str(i) + "]:  "))

        tempo_restante[i] = tempo_execucao[i]
        tempo_espera[i] = 0


def imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
    # Imprime lista de processos
    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_execucao=" + str(tempo_execucao[i]) +
              " tempo_restante=" + str(tempo_restante[i]) +
              " tempo_chegada=" + str(tempo_chegada[i]) +
              " prioridade =" + str(prioridade[i]))


def imprime_stats(espera):
    tempo_espera = list(espera)
    # Implementar o calculo e impressao de estatisticas

    tempo_espera_total = 0.0

    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_espera=" + str(tempo_espera[i]))
        tempo_espera_total = tempo_espera_total + tempo_espera[i]

    print("Tempo medio de espera: " + str(tempo_espera_total / n_processos))


def FCFS(execucao, espera, restante, chegada):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    # tempo_chegada = list(chegada)

    processo_em_execucao = 0  # processo inicial no FIFO e o zero

    # implementar codigo do FCFS
    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]))

        if tempo_execucao[processo_em_execucao] == tempo_restante[processo_em_execucao]:
            tempo_espera[processo_em_execucao] = i - 1

        if tempo_restante[processo_em_execucao] == 1:
            if processo_em_execucao == (n_processos - 1):
                break
            else:
                processo_em_execucao = processo_em_execucao + 1
        else:
            tempo_restante[processo_em_execucao] = tempo_restante[processo_em_execucao] - 1
    #

    imprime_stats(tempo_espera)


def SJF(preemptivo, execucao, espera, restante, chegada):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)

    # [IA] implementar codigo do SJF preemptivo e nao preemptivo
    processo_em_execucao = -1  # -1 significa CPU ociosa

    for i in range(1, MAXIMO_TEMPO_EXECUCAO):

        # todos os processos terminaram
        if soma_restante(tempo_restante) == 0:
            break

        # Quando escolher um novo processo?
        # - se a CPU esta ociosa
        # - se o processo que estava rodando terminou
        # - se o algoritmo e' preemptivo (reavalia a cada instante de tempo)
        if (processo_em_execucao == -1 or preemptivo or
                tempo_restante[processo_em_execucao] == 0):
            processo_em_execucao = menor_tempo_restante(tempo_restante, tempo_chegada, i)

        # nenhum processo chegou ainda
        if processo_em_execucao == -1:
            print("tempo[" + str(i) + "]: CPU ociosa")
            continue

        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]))

        contabiliza_espera(tempo_espera, tempo_restante, tempo_chegada, processo_em_execucao, i)

        tempo_restante[processo_em_execucao] = tempo_restante[processo_em_execucao] - 1
    #

    imprime_stats(tempo_espera)


def PRIORIDADE(preemptivo, execucao, espera, restante, chegada, prioridade):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)
    prioridade_temp = list(prioridade)

    # [IA] implementar codigo do Prioridade preemptivo e nao preemptivo
    # Convencao adotada: MENOR numero = prioridade MAIS ALTA
    processo_em_execucao = -1  # -1 significa CPU ociosa

    for i in range(1, MAXIMO_TEMPO_EXECUCAO):

        if soma_restante(tempo_restante) == 0:
            break

        if (processo_em_execucao == -1 or preemptivo or
                tempo_restante[processo_em_execucao] == 0):
            processo_em_execucao = maior_prioridade(prioridade_temp, tempo_restante, tempo_chegada, i)

        if processo_em_execucao == -1:
            print("tempo[" + str(i) + "]: CPU ociosa")
            continue

        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]) +
              " prioridade=" + str(prioridade_temp[processo_em_execucao]))

        contabiliza_espera(tempo_espera, tempo_restante, tempo_chegada, processo_em_execucao, i)

        tempo_restante[processo_em_execucao] = tempo_restante[processo_em_execucao] - 1
    #

    imprime_stats(tempo_espera)


def Round_Robin(execucao, espera, restante):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)

    # [IA] implementar codigo do Round-Robin
    # O Round-Robin nao usa tempo de chegada: todos os processos ja' estao na fila.
    processo_em_execucao = 0
    quantum_usado = 0

    for i in range(1, MAXIMO_TEMPO_EXECUCAO):

        if soma_restante(tempo_restante) == 0:
            break

        # troca de processo se o atual terminou ou se ja' gastou toda a sua fatia
        if tempo_restante[processo_em_execucao] == 0 or quantum_usado == QUANTUM:
            processo_em_execucao = proximo_processo(processo_em_execucao, tempo_restante)
            quantum_usado = 0

        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]) +
              " quantum=" + str(quantum_usado + 1) + "/" + str(QUANTUM))

        # no Round-Robin todos que ainda nao terminaram estao esperando
        for j in range(n_processos):
            if j != processo_em_execucao and tempo_restante[j] > 0:
                tempo_espera[j] = tempo_espera[j] + 1

        tempo_restante[processo_em_execucao] = tempo_restante[processo_em_execucao] - 1
        quantum_usado = quantum_usado + 1
    #

    imprime_stats(tempo_espera)


# ---------- funcoes auxiliares [IA] ----------

def soma_restante(tempo_restante):
    """Soma o que falta executar de todos os processos.
    Quando da' zero, a simulacao acabou."""
    total = 0
    for i in range(n_processos):
        total = total + tempo_restante[i]
    return total


def contabiliza_espera(tempo_espera, tempo_restante, tempo_chegada, em_execucao, instante):
    """Soma 1 no tempo de espera de todo processo que ja' chegou,
    ainda nao terminou e nao e' o que esta ocupando a CPU."""
    for j in range(n_processos):
        if j != em_execucao and tempo_chegada[j] <= instante and tempo_restante[j] > 0:
            tempo_espera[j] = tempo_espera[j] + 1


def menor_tempo_restante(tempo_restante, tempo_chegada, instante):
    """Devolve o indice do processo pronto com o menor tempo restante.
    Devolve -1 se nenhum processo chegou ainda."""
    escolhido = -1
    for j in range(n_processos):
        if tempo_chegada[j] <= instante and tempo_restante[j] > 0:
            if escolhido == -1 or tempo_restante[j] < tempo_restante[escolhido]:
                escolhido = j
    return escolhido


def maior_prioridade(prioridade, tempo_restante, tempo_chegada, instante):
    """Devolve o indice do processo pronto com a prioridade mais alta
    (menor numero). Devolve -1 se nenhum processo chegou ainda."""
    escolhido = -1
    for j in range(n_processos):
        if tempo_chegada[j] <= instante and tempo_restante[j] > 0:
            if escolhido == -1 or prioridade[j] < prioridade[escolhido]:
                escolhido = j
    return escolhido


def proximo_processo(atual, tempo_restante):
    """Devolve o proximo processo da fila circular que ainda tem tempo restante."""
    for k in range(1, n_processos + 1):
        proximo = (atual + k) % n_processos
        if tempo_restante[proximo] > 0:
            return proximo
    return atual


main()
