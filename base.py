# ==============================================================
# Simulador de Escalonamento de Processos
# Sistemas Operacionais - IFRS Campus Restinga - ADS 3N - 2026/2
# Prof. Jean Carlo Hamerski
#
# Entrega 1 (tag v1.0): FCFS
# Entrega 2 (tag v2.0): SJF preemptivo e nao preemptivo
# Aluno: Paulo (Paulosvv)
#
# DECLARACAO DE USO DE IA GENERATIVA (secao 6 do enunciado):
# IA utilizada: Claude (Anthropic).
# Onde: na funcao SJF() e nas funcoes auxiliares soma_restante(),
#       contabiliza_espera() e menor_tempo_restante(), marcadas com "[IA]",
#       e nos comentarios explicativos dos blocos do arquivo.
# Para que fim: escrever a logica de escolha do processo a cada instante
#       de tempo, seguindo o mesmo modelo de laco do FCFS do codigo-base.
# O FCFS, main, popular_processos, imprime_processos e imprime_stats sao o
# codigo-base da disciplina (apenas receberam comentarios).
# PRIORIDADE() e Round_Robin() seguem como esqueletos (entregas 3 e 4).
# O detalhamento esta em ENTREGA.txt.
# ==============================================================

import random

# Limite do laco de simulacao: cada volta do laco e' um instante de tempo.
MAXIMO_TEMPO_EXECUCAO = 65535

# Quantidade de processos da lista.
n_processos = 3


def main():
    # --- Criacao das listas paralelas ---
    # Cada processo e' um indice (0, 1, 2...) e cada lista guarda um atributo
    # dele. Ex.: tempo_execucao[1] e' o tempo de execucao do processo 1.
    tempo_execucao = [0] * n_processos
    tempo_chegada = [0] * n_processos
    prioridade = [0] * n_processos
    tempo_espera = [0] * n_processos
    tempo_restante = [0] * n_processos

    # --- Preenche e mostra a lista de processos ---
    popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

    imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

    # --- Menu principal ---
    # Repete ate o usuario escolher 9. A mesma lista de processos alimenta
    # todos os algoritmos, o que permite comparar os tempos medios de espera.
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
    # Pergunta se os atributos serao sorteados (1) ou digitados (0).
    aleatorio = int(input("Sera aleatorio?:  "))

    for i in range(n_processos):
        # --- Modo aleatorio: sorteia os atributos do processo i ---
        if aleatorio == 1:
            tempo_execucao[i] = random.randint(1, 10)
            tempo_chegada[i] = random.randint(1, 10)
            prioridade[i] = random.randint(1, 15)
        # --- Modo manual: le os atributos do teclado ---
        else:
            tempo_execucao[i] = int(input("Digite o tempo de execucao do processo[" + str(i) + "]:  "))
            tempo_chegada[i] = int(input("Digite o tempo de chegada do processo[" + str(i) + "]:  "))
            prioridade[i] = int(input("Digite a prioridade do processo[" + str(i) + "]:  "))

        # --- Estado inicial ---
        # Nada foi executado ainda: falta executar o tempo todo e a espera e' zero.
        tempo_restante[i] = tempo_execucao[i]
        tempo_espera[i] = 0


def imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
    # Mostra uma linha por processo com todos os seus atributos.
    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_execucao=" + str(tempo_execucao[i]) +
              " tempo_restante=" + str(tempo_restante[i]) +
              " tempo_chegada=" + str(tempo_chegada[i]) +
              " prioridade =" + str(prioridade[i]))


def imprime_stats(espera):
    tempo_espera = list(espera)

    # --- Soma as esperas e imprime a de cada processo ---
    tempo_espera_total = 0.0

    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_espera=" + str(tempo_espera[i]))
        tempo_espera_total = tempo_espera_total + tempo_espera[i]

    # --- Media: soma das esperas dividida pela quantidade de processos ---
    print("Tempo medio de espera: " + str(tempo_espera_total / n_processos))


def FCFS(execucao, espera, restante, chegada):
    # --- Copia das listas ---
    # list() cria copias: a simulacao altera as copias e a lista original
    # continua intacta para ser usada pelos outros algoritmos.
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    # tempo_chegada = list(chegada)   # o FCFS nao usa o tempo de chegada

    processo_em_execucao = 0  # processo inicial no FIFO e o zero

    # --- Laco de simulacao: cada volta e' um instante de tempo i ---
    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        # Historico: qual processo ocupa a CPU neste instante.
        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]))

        # --- Registro da espera ---
        # Se o restante ainda e' igual ao tempo total, o processo esta
        # comecando agora: ele esperou tudo o que passou antes (i - 1).
        if tempo_execucao[processo_em_execucao] == tempo_restante[processo_em_execucao]:
            tempo_espera[processo_em_execucao] = i - 1

        # --- Decisao de escalonamento (sem preempcao) ---
        # O processo so sai da CPU quando chega ao ultimo instante; entao a CPU
        # passa para o proximo da fila (indice + 1). Se era o ultimo, acabou.
        if tempo_restante[processo_em_execucao] == 1:
            if processo_em_execucao == (n_processos - 1):
                break
            else:
                processo_em_execucao = processo_em_execucao + 1
        # --- Execucao: o processo consome 1 unidade de tempo ---
        else:
            tempo_restante[processo_em_execucao] = tempo_restante[processo_em_execucao] - 1

    imprime_stats(tempo_espera)


def SJF(preemptivo, execucao, espera, restante, chegada):
    # --- Copia das listas (mesmo motivo do FCFS) ---
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)  # o SJF usa o tempo de chegada

    # [IA] SJF preemptivo e nao preemptivo.
    # Regra: entre os processos que JA CHEGARAM e ainda nao terminaram,
    # a CPU vai para o que tem o MENOR tempo restante.
    #  - Nao preemptivo: a escolha so e' feita quando a CPU fica livre;
    #    quem comecou roda ate o fim.
    #  - Preemptivo (SRTF): a escolha e' refeita a cada instante; se chegar
    #    um processo mais curto, ele toma a CPU do atual.
    processo_em_execucao = -1  # -1 significa CPU ociosa (ninguem escolhido)

    # --- Laco de simulacao: cada volta e' um instante de tempo i ---
    for i in range(1, MAXIMO_TEMPO_EXECUCAO):

        # --- Condicao de parada ---
        # Se a soma do que falta executar e' zero, todos terminaram.
        if soma_restante(tempo_restante) == 0:
            break

        # --- Decisao de escalonamento ---
        # Escolhe um (novo) processo quando:
        #  - a CPU esta ociosa (-1);
        #  - o processo atual terminou (restante == 0);
        #  - o algoritmo e' preemptivo (reavalia em todo instante).
        # No nao preemptivo, fora esses casos, o processo atual continua.
        if (processo_em_execucao == -1 or preemptivo or
                tempo_restante[processo_em_execucao] == 0):
            processo_em_execucao = menor_tempo_restante(tempo_restante, tempo_chegada, i)

        # --- CPU ociosa ---
        # Nenhum processo chegou ainda neste instante: pula para o proximo.
        if processo_em_execucao == -1:
            print("tempo[" + str(i) + "]: CPU ociosa")
            continue

        # --- Historico: qual processo ocupa a CPU neste instante ---
        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]))

        # --- Registro da espera ---
        # Todo processo que ja chegou, nao terminou e nao esta na CPU
        # esperou 1 unidade de tempo neste instante.
        contabiliza_espera(tempo_espera, tempo_restante, tempo_chegada, processo_em_execucao, i)

        # --- Execucao: o processo escolhido consome 1 unidade de tempo ---
        tempo_restante[processo_em_execucao] = tempo_restante[processo_em_execucao] - 1

    imprime_stats(tempo_espera)


def PRIORIDADE(preemptivo, execucao, espera, restante, chegada, prioridade):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)
    prioridade_temp = list(prioridade)

    # implementar codigo do Prioridade preemptivo e nao preemptivo (entrega 3)
    #

    imprime_stats(tempo_espera)


def Round_Robin(execucao, espera, restante):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)

    # implementar codigo do Round-Robin (entrega 4)
    #

    imprime_stats(tempo_espera)


# ---------- funcoes auxiliares do SJF [IA] ----------

def soma_restante(tempo_restante):
    # Soma o que falta executar de todos os processos.
    # Quando da zero, a simulacao acabou.
    total = 0
    for i in range(n_processos):
        total = total + tempo_restante[i]
    return total


def contabiliza_espera(tempo_espera, tempo_restante, tempo_chegada, em_execucao, instante):
    # Soma 1 na espera de cada processo que esta na fila de prontos:
    # ja chegou (chegada <= instante), ainda nao terminou (restante > 0)
    # e nao e' o que esta ocupando a CPU.
    for j in range(n_processos):
        if j != em_execucao and tempo_chegada[j] <= instante and tempo_restante[j] > 0:
            tempo_espera[j] = tempo_espera[j] + 1


def menor_tempo_restante(tempo_restante, tempo_chegada, instante):
    # Percorre a fila de prontos e devolve o indice do processo com o
    # MENOR tempo restante. Devolve -1 se nenhum processo chegou ainda.
    # Desempate: quem chegou primeiro; persistindo, o de menor indice.
    escolhido = -1
    for j in range(n_processos):
        # So concorre quem ja chegou e ainda tem o que executar.
        if tempo_chegada[j] <= instante and tempo_restante[j] > 0:
            if (escolhido == -1 or
                    tempo_restante[j] < tempo_restante[escolhido] or
                    (tempo_restante[j] == tempo_restante[escolhido] and
                     tempo_chegada[j] < tempo_chegada[escolhido])):
                escolhido = j
    return escolhido


main()
