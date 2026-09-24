# Trabalho de Desenvolvimento — Sistemas Operacionais

Simulador de algoritmos de escalonamento de processos.

**IFRS — Campus Restinga** | ADS 3N — 2026/2
Prof. Jean Carlo Hamerski
Aluno: Paulo (Paulosvv)

## Entregas

| # | Algoritmo | Tag | Situação |
|---|---|---|---|
| 1 | FCFS | `v1.0` | entregue |
| 2 | SJF preemptivo e não preemptivo | `v2.0` | entregue |
| 3 | Prioridade preemptivo e não preemptivo | `v3.0` | a implementar |
| 4 | Round-Robin e integração final | `v4.0` | a implementar |

As opções 4 a 6 do menu já existem porque fazem parte do código-base, mas suas
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

### Onde fica a decisão de escalonamento do SJF

Na função `SJF()`, dentro do laço, a CPU é (re)atribuída pela função
`menor_tempo_restante()`: entre os processos que já chegaram
(`tempo_chegada <= i`) e ainda não terminaram, vence o de menor tempo restante
(empate: quem chegou primeiro). O parâmetro `preemptivo` decide **quando** essa
escolha é refeita:

- **Não preemptivo** (opção 3): só quando a CPU fica livre — quem começou roda
  até o fim.
- **Preemptivo / SRTF** (opção 2): a cada instante — um processo mais curto que
  chega toma a CPU do atual.

A espera é somada instante a instante por `contabiliza_espera()`: cada processo
que já chegou, não terminou e não está na CPU ganha 1 de espera. Se ninguém
chegou ainda, o instante aparece como `CPU ociosa`.

Exemplo (execução 8, 4, 2; chegada 1, 2, 3) — tempo médio de espera:
FCFS 6,67 · SJF não preemptivo 5,0 · SJF preemptivo 2,67. Passo a passo em
[ENTREGA.txt](ENTREGA.txt).

## Uso de Inteligência Artificial Generativa

O FCFS é o código-base da disciplina (recebeu apenas comentários). A função
`SJF()` e suas auxiliares, marcadas com `[IA]`, e os comentários dos blocos
foram escritos com auxílio do Claude (Anthropic). A declaração completa,
exigida pela seção 6 do enunciado, está em [ENTREGA.txt](ENTREGA.txt).
