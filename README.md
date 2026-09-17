# Trabalho de Desenvolvimento — Sistemas Operacionais

Simulador de algoritmos de escalonamento de processos.

**IFRS — Campus Restinga** | ADS 3N — 2026/2
Prof. Jean Carlo Hamerski
Aluno: Paulo (Paulosvv)

## Sobre

Programa que simula seis políticas de escalonamento de processos sobre a mesma
lista de entrada, permitindo comparar o tempo médio de espera de cada uma.

| # | Algoritmo | Preempção |
|---|-----------|-----------|
| 1 | FCFS (First Come, First Served) | não |
| 2 | SJF (Shortest Job First) | sim |
| 3 | SJF (Shortest Job First) | não |
| 4 | Prioridade | sim |
| 5 | Prioridade | não |
| 6 | Round-Robin | sim (por quantum) |

## Como executar

Requisito: Python 3.

```
python base.py
```

O programa começa pedindo como popular a lista de processos:

- `1` — atributos sorteados aleatoriamente
- `0` (ou qualquer outro número) — atributos digitados pelo teclado

Em seguida aparece o menu, que permite executar qualquer algoritmo sobre a mesma
lista, reimprimir a lista, repopular a lista sem reiniciar o programa (opção 8)
ou sair (opção 9).

Para cada execução o programa imprime:

- o histórico de execução (qual processo ocupou a CPU em cada instante de tempo);
- o tempo de espera de cada processo;
- o tempo médio de espera.

## Configuração

Constantes no topo do arquivo `base.py`:

| Constante | Padrão | Significado |
|-----------|--------|-------------|
| `n_processos` | 3 | quantidade de processos da lista |
| `QUANTUM` | 2 | fatia de tempo do Round-Robin |
| `MAXIMO_TEMPO_EXECUCAO` | 65535 | trava de segurança do laço de simulação |

## Convenções adotadas

- **Prioridade:** menor número = prioridade mais alta.
- **Tempo de chegada:** usado por SJF e Prioridade. O FCFS e o Round-Robin o
  ignoram, conforme o enunciado do trabalho.
- **Tempo de espera:** soma dos instantes em que o processo já chegou, ainda não
  terminou e não está ocupando a CPU.

## Estrutura do código

Os processos são representados por listas paralelas indexadas pelo número do
processo (`tempo_execucao`, `tempo_chegada`, `prioridade`, `tempo_restante`,
`tempo_espera`).

Cada função de algoritmo copia as listas com `list()` antes de simular, de modo
que a lista de entrada não é destruída e a mesma entrada pode ser reutilizada por
todos os algoritmos.

Todos os algoritmos compartilham o mesmo laço de tempo: a cada instante verifica-se
o término, decide-se qual processo ocupa a CPU, registra-se o histórico e a espera,
e decrementa-se uma unidade do tempo restante. O que muda entre eles é apenas o
critério de escolha e o momento em que a escolha é refeita.

## Uso de Inteligência Artificial Generativa

Ver o arquivo `ENTREGA.txt` e os comentários marcados com `[IA]` em `base.py`.
