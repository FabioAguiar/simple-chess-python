# Vision Spec — Simple Chess Python

## Status do Documento

| Campo | Valor |
|---|---|
| Projeto | Simple Chess Python |
| Natureza | Jogo simples de xadrez em Python |
| Status | Visão inicial |
| Metodologia | SIC — Structured Intent Control |
| Documento | `docs/vision.md` |

---

## 1. Identidade do projeto

Simple Chess Python é um projeto greenfield para implementação de um jogo simples de xadrez em Python.

O projeto será usado tanto como aplicação de aprendizado quanto como projeto controlado para testar um pipeline de workflows do `n8n-local-stack`, em conjunto com a documentação SIC.

A intenção inicial é manter o projeto pequeno, claro, versionável e adequado para execução incremental assistida por IA. Após a definição dos documentos fundacionais (`vision.md`, `architecture.md` e `milestones.md`), o projeto deve poder ser conduzido pelo pipeline do `n8n-local-stack` desde a primeira milestone de implementação.

---

## 2. Propósito

O projeto existe para entregar uma implementação simples e funcional de xadrez em Python, preservando clareza técnica e documentação suficiente para orientar futuras execuções pelo SIC.

Além do jogo em si, o projeto deve servir como caso prático para observar como a documentação SIC ajuda a organizar decisões, reduzir ambiguidade e conduzir a evolução de um sistema desde o início.

---

## 3. Problema que resolve

O projeto resolve duas necessidades concretas:

1. criar um jogo simples de xadrez que possa ser entendido, executado e evoluído de forma incremental;
2. fornecer um repositório pequeno e controlável para testar workflows do `n8n-local-stack` desde as primeiras etapas de implementação, sem a complexidade de um sistema grande.

Como as regras do xadrez são conhecidas e estáveis, o projeto é adequado para testar processo, documentação, validação e continuidade, sem exigir longa descoberta de domínio.

---

## 4. Direção do produto

A direção atual é construir um jogo local de xadrez em Python, com escopo controlado e implementação simples.

A prioridade é:

- clareza antes de sofisticação;
- regras essenciais antes de recursos avançados;
- documentação útil antes de formalismo excessivo;
- arquitetura proporcional ao tamanho real do projeto;
- suporte ao pipeline SIC/n8n sem transformar o jogo em um projeto de automação.

A interface gráfica e a estrutura arquitetural inicial foram consolidadas no `docs/architecture.md`. Mudanças relevantes nessas decisões devem ser registradas antes de afetarem a implementação.

---

## 5. Modelo conceitual inicial

Conceitos principais do projeto:

- **Jogo**: coordena o fluxo geral da partida.
- **Tabuleiro**: representa as casas e a posição das peças.
- **Peça**: representa cada peça de xadrez e suas regras de movimentação.
- **Jogador**: representa o lado branco ou preto.
- **Turno**: controla qual jogador pode mover.
- **Movimento**: representa uma tentativa de deslocamento de peça.
- **Validação de movimento**: verifica se um movimento é permitido.
- **Estado da partida**: registra posição atual, turno, capturas e condições relevantes de continuidade ou encerramento.

Este modelo conceitual não define ainda a arquitetura final.

---

## 6. Drivers arquiteturais iniciais

A futura arquitetura deve considerar os seguintes fatores:

- projeto local e versionável;
- implementação em Python;
- escopo pequeno e adequado para aprendizado;
- regras de xadrez estáveis e conhecidas;
- necessidade de separar lógica de jogo e interface;
- necessidade de testes mínimos para regras essenciais;
- uso do projeto como caso de teste para workflows do `n8n-local-stack` desde a primeira milestone de implementação;
- documentação SIC como referência de direção e continuidade;
- preferência por simplicidade e baixo custo de contexto para IA;
- rejeição de overengineering nesta fase inicial.

Esses drivers não fecham a arquitetura. Eles apenas orientam a próxima etapa de descoberta e decisão arquitetural.

---

## 7. Escopo núcleo

A visão central depende dos seguintes itens:

- jogo implementado em Python;
- representação funcional do tabuleiro;
- representação das peças principais do xadrez;
- controle de turnos entre brancas e pretas;
- validação de movimentos essenciais;
- impedimento de movimentos claramente inválidos;
- captura de peças;
- identificação mínima de xeque e fim de partida, conforme decisão arquitetural futura;
- interface simples para interação local;
- documentação fundacional composta, no mínimo, por:
  - `README.md`;
  - `docs/vision.md`;
  - `docs/architecture.md`;
  - documento de milestones ou planejamento equivalente, se adotado no fluxo SIC;
- estrutura suficiente para que o pipeline do `n8n-local-stack` leia os documentos fundacionais, identifique a milestone vigente, apoie a geração de issues, conduza implementações e registre validações externas.

---

## 8. Escopo não-bloqueante

Os itens abaixo podem melhorar o projeto, mas não devem bloquear a conclusão da visão central:

- interface gráfica mais refinada;
- destaque visual de movimentos possíveis;
- histórico de movimentos;
- desfazer jogada;
- salvar e carregar partidas;
- testes mais abrangentes de regras especiais;
- empacotamento da aplicação;
- publicação de release;
- documentação visual com imagens ou GIFs;
- suporte futuro a IA simples para jogar contra o computador.

---

## 9. Fora do escopo

Não fazem parte desta visão inicial:

- motor de xadrez competitivo;
- análise avançada de posições;
- integração com Stockfish ou engines externas;
- multiplayer online;
- autenticação de usuários;
- ranking, matchmaking ou sistema de contas;
- servidor web obrigatório;
- persistência complexa;
- suporte formal a torneios;
- relógio de xadrez obrigatório;
- automação do gameplay pelo n8n;
- transformar o projeto em framework genérico de jogos.

---

## 10. Restrições e princípios

A evolução do projeto deve respeitar as seguintes restrições:

- manter separação entre visão, arquitetura, milestones, issues, State, Intent e Control;
- não transformar este documento em plano de implementação detalhado;
- não alterar a stack gráfica consolidada no `docs/architecture.md` sem decisão explícita;
- não introduzir arquitetura complexa sem necessidade real;
- preservar legibilidade para humanos e para IA;
- priorizar decisões explícitas e registradas;
- evitar requisitos implícitos não declarados pelo usuário;
- manter o projeto pequeno o suficiente para testar o pipeline de workflows;
- tratar o `n8n-local-stack` como orquestrador externo do processo de implementação e validação, não como parte interna do jogo;
- manter artefatos locais, caches e saídas de runtime fora do versionamento.

---

## 11. Relação com State, Intent e Control

### State

Este documento pode informar States futuros, mas não é memória operacional detalhada.

Ele não deve registrar histórico de execução, patches aplicados ou decisões locais de issues específicas.

### Intent

Este documento orienta intenções futuras, mas não substitui o tipo de tarefa de cada execução.

Cada etapa futura ainda deve declarar sua intenção de forma explícita.

### Control

Este documento limita e orienta execuções futuras, mas não define como executar a implementação.

A execução deve ocorrer por prompts, templates, issues, patches ou workflows apropriados.

---

## 12. Relação com Architecture

O `docs/architecture.md` consolida as decisões técnicas iniciais derivadas desta visão.

As decisões já consolidadas incluem:

- aplicação local, não web;
- interface gráfica com Pygame;
- arquitetura modular simples em camadas leves;
- separação entre interface, aplicação e domínio;
- uso de `python-chess` encapsulado na camada de domínio;
- uso de `pytest` para testes;
- uso de Ruff para lint e formatação;
- manutenção do `n8n-local-stack` fora do runtime do jogo.

Este documento de visão continua definindo o propósito e os limites macro do projeto. O documento de arquitetura define as decisões técnicas iniciais para orientar a implementação.

---

## 13. Definition of Done macro

A visão central poderá ser considerada concluída quando:

- o jogo puder ser executado localmente;
- dois jogadores puderem jogar uma partida simples no mesmo ambiente;
- o tabuleiro e as peças forem representados de forma compreensível;
- turnos forem controlados corretamente;
- movimentos inválidos básicos forem rejeitados;
- capturas forem aplicadas corretamente;
- regras essenciais de xeque ou encerramento forem tratadas conforme escopo definido na arquitetura;
- houver testes ou validações mínimas para regras centrais;
- a documentação fundacional estiver presente e coerente;
- o projeto puder ser usado como alvo de implementação, validação e revisão pelo pipeline de workflows do `n8n-local-stack`.

---

## 14. Pontos em aberto

As seguintes decisões ainda podem ser refinadas em etapas futuras:

- nível exato de refinamento visual da interface;
- nível de suporte inicial a recursos opcionais, como histórico, desfazer jogada ou salvamento;
- formato final das issues derivadas das milestones;
- critérios operacionais específicos usados pelo pipeline do `n8n-local-stack` para conduzir cada implementação;
- licença do projeto.

Esses pontos não bloqueiam a criação do `docs/milestones.md`, mas devem ser tratados por decisões explícitas quando passarem a afetar implementação, validação ou distribuição.
