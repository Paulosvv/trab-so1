# Trabalho de Desenvolvimento — Sistemas Operacionais

Simulador de algoritmos de escalonamento de processos.

**IFRS — Campus Restinga** | ADS 3N — 2026/2
Prof. Jean Carlo Hamerski
Aluno: Paulo (Paulosvv)

## Entregas

| # | Algoritmo | Tag | Situação |
|---|---|---|---|
| 1 | FCFS | `v1.0` | entregue |
| 2 | SJF preemptivo e não preemptivo | `v2.0` | a implementar |
| 3 | Prioridade preemptivo e não preemptivo | `v3.0` | a implementar |
| 4 | Round-Robin e integração final | `v4.0` | a implementar |

As opções 2 a 6 do menu já existem porque fazem parte do código-base, mas suas
funções seguem como os esqueletos originais, a serem preenchidos nas próximas
entregas.

## Como executar

Requisito: Python 3.

```
python base.py
```

O programa começa perguntando como popular a lista de processos:

- `1` — atributos sorteados aleatoriamente
- `0` — atributos digitados pelo teclado (tempo de execução, tempo de chegada
  e prioridade, nesta ordem, para cada processo)

Em seguida aparece o menu, de onde se executa o algoritmo (opção 1), reimprime
a lista (7), repopula a lista sem reiniciar o programa (8) ou sai (9).

Para cada execução o programa imprime o histórico (qual processo ocupou a CPU
em cada instante de tempo), o tempo de espera de cada processo e o tempo médio
de espera.

Instruções detalhadas, com exemplo de saída, em [ENTREGA.txt](ENTREGA.txt).

## Configuração

| Constante | Padrão | Significado |
|---|---|---|
| `n_processos` | 3 | quantidade de processos da lista |
| `MAXIMO_TEMPO_EXECUCAO` | 65535 | limite do laço de simulação |

## Estrutura do código

Os processos são representados por **listas paralelas** indexadas pelo número do
processo: `tempo_execucao`, `tempo_chegada`, `prioridade`, `tempo_restante` e
`tempo_espera`.

Cada função de algoritmo copia as listas com `list()` antes de simular, de modo
que a entrada não é destruída e o mesmo conjunto de processos pode alimentar
todos os algoritmos — é o que permitirá comparar o tempo médio de espera entre
as políticas quando as demais entregas estiverem prontas.

O laço de simulação percorre o tempo instante a instante: imprime o histórico,
registra a espera e desconta uma unidade do tempo restante do processo que está
na CPU. O que muda de um algoritmo para outro é apenas **o critério de escolha
do processo** e o momento em que essa escolha é refeita.

### Onde fica a decisão de escalonamento do FCFS

Na função `FCFS()`, dentro do laço: quando o processo em execução chega ao seu
último instante (`tempo_restante == 1`), a CPU passa para
`processo_em_execucao + 1` — o próximo da ordem de chegada da lista. Não há
preempção: um processo só deixa a CPU quando termina. O tempo de chegada não é
usado, conforme o enunciado.

A espera é registrada no instante em que o processo começa a executar
(`tempo_execucao == tempo_restante`), e vale `i - 1`: tudo o que passou antes
dele. Por isso, no FCFS, a espera de cada processo é a soma dos tempos de
execução dos processos anteriores.

## Uso de Inteligência Artificial Generativa

Nesta versão não há trecho de código gerado por IA — o FCFS é o código-base da
disciplina. A declaração completa, exigida pela seção 6 do enunciado, está em
[ENTREGA.txt](ENTREGA.txt).
