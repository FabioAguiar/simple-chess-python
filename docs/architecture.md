# Architecture — Python Chess Game

## 1. Status

Status: **Inicial / Aprovado para implementação**

Este documento consolida as decisões arquiteturais iniciais do projeto `simple-chess-python`.

O objetivo é orientar a implementação de um jogo simples de xadrez em Python, mantendo o projeto pequeno, compreensível, testável e adequado para uso como projeto-piloto em workflows do `n8n-local-stack` e na aplicação prática da metodologia SIC.

---

## 2. Contexto

O projeto `simple-chess-python` será uma aplicação local de xadrez simples, desenvolvida em Python.

O projeto não será uma aplicação web e não terá, inicialmente, foco em multiplayer online, persistência em banco de dados, engine própria de inteligência artificial ou implementação manual completa das regras do xadrez.

Além do objetivo funcional de criar um jogo jogável, este projeto também servirá como experimento controlado para avaliar como a documentação SIC pode apoiar a construção incremental de software com auxílio de IA e automações externas via n8n.

---

## 3. Objetivos arquiteturais

A arquitetura deve favorecer:

- simplicidade;
- clareza estrutural;
- separação mínima de responsabilidades;
- facilidade de entendimento por IA;
- facilidade de teste;
- evolução incremental;
- baixo acoplamento entre interface gráfica e regras do jogo;
- compatibilidade com execução local;
- uso futuro em pipelines de validação do `n8n-local-stack`.

A arquitetura não deve introduzir complexidade desnecessária para um projeto pequeno.

---

## 4. Decisão arquitetural principal

O projeto adotará uma **arquitetura modular simples em camadas leves**.

A separação principal será:

```text
Interface gráfica
  ↓
Camada de aplicação
  ↓
Domínio / regras do jogo
  ↓
Biblioteca python-chess
```

Essa estrutura permite que a interface gráfica seja mantida separada das regras do jogo e do controle de estado da partida.

A arquitetura não seguirá uma Clean Architecture rígida, pois isso adicionaria formalismo excessivo para o tamanho e o propósito atual do projeto.

---

## 5. Tecnologias escolhidas

### 5.1 Linguagem

**Python** será a linguagem principal do projeto.

Justificativa:

- já está definida como requisito do projeto;
- é adequada para prototipação rápida;
- possui bibliotecas maduras para jogos simples, testes e automação;
- combina bem com o objetivo de aprendizado e portfólio.

---

### 5.2 Interface gráfica

A interface gráfica será implementada com **Pygame**.

Justificativa:

- é adequada para jogos 2D simples;
- permite desenhar tabuleiro, peças e elementos visuais com baixo custo de implementação;
- possui modelo natural de loop de eventos;
- é suficiente para capturar cliques, atualizar a tela e renderizar o estado do jogo.

Alternativas consideradas:

- `Tkinter`: viável, mas menos natural para um jogo com renderização de tabuleiro e interação visual contínua;
- `Arcade`: viável, mas adicionaria uma escolha menos necessária para o escopo inicial;
- aplicação web: rejeitada por decisão explícita do projeto.

---

### 5.3 Motor de regras do xadrez

As regras do xadrez serão inicialmente apoiadas pela biblioteca **python-chess**.

Justificativa:

- reduz o risco de erros em regras específicas como xeque, xeque-mate, roque, promoção e en passant;
- permite focar o projeto na arquitetura, interface, fluxo de implementação e validação;
- evita transformar o projeto inicial em uma implementação completa de regras de xadrez do zero;
- mantém o projeto mais adequado como caso de teste para o pipeline SIC + n8n.

Decisão importante:

> A biblioteca `python-chess` deve ser encapsulada pela camada de domínio. Ela não deve aparecer espalhada por toda a aplicação.

Isso preserva a possibilidade de, no futuro, substituir ou complementar o motor de regras sem reescrever a interface gráfica inteira.

---

### 5.4 Testes

O projeto utilizará **pytest** para testes automatizados.

Prioridades iniciais de teste:

- estado inicial da partida;
- validação de movimento permitido;
- rejeição de movimento inválido;
- alternância de turno;
- detecção de fim de jogo, quando suportada;
- comportamento da camada de aplicação sem depender da interface gráfica.

A interface Pygame não será o foco inicial dos testes automatizados.

---

### 5.5 Qualidade de código

O projeto utilizará **Ruff** para lint e formatação.

Justificativa:

- reduz a quantidade de ferramentas necessárias;
- mantém o projeto simples;
- favorece consistência de estilo;
- é adequado para validações automatizadas futuras.

---

### 5.6 Gerenciamento do projeto

O projeto deverá usar um `pyproject.toml` simples.

O ambiente de desenvolvimento poderá ser criado com Conda, mas a configuração do projeto deve permanecer compreensível e portável.

O ambiente Conda não deve substituir a documentação do projeto, nem deve armazenar decisões arquiteturais.

---

## 6. Estrutura inicial recomendada

A estrutura inicial recomendada é:

```text
simple-chess-python/
  README.md
  pyproject.toml
  .gitignore

  docs/
    vision.md
    architecture.md
    milestones.md

  src/
    simple_chess/
      __init__.py
      main.py

      app/
        __init__.py
        game_controller.py
        game_state.py

      domain/
        __init__.py
        board.py
        rules.py
        move.py

      ui/
        __init__.py
        pygame_app.py
        board_renderer.py
        input_handler.py

  tests/
    test_game_state.py
    test_rules.py
```

Essa estrutura pode ser simplificada durante a implementação se algum arquivo se mostrar prematuro.

A regra principal é evitar que `ui/` concentre regras de xadrez ou controle completo da partida.

---

## 7. Responsabilidades por camada

## 7.1 Camada de domínio

Diretório sugerido:

```text
src/simple_chess/domain/
```

Responsável por representar e proteger os conceitos centrais do jogo.

Responsabilidades:

- tabuleiro;
- posição das peças;
- movimentos;
- validação de regras;
- integração encapsulada com `python-chess`;
- consulta de estados como xeque, xeque-mate, empate ou partida em andamento.

A camada de domínio não deve depender de Pygame.

---

## 7.2 Camada de aplicação

Diretório sugerido:

```text
src/simple_chess/app/
```

Responsável por coordenar o fluxo da partida.

Responsabilidades:

- controlar seleção de peças;
- solicitar validação de movimentos;
- atualizar o estado da partida;
- controlar turno atual;
- expor mensagens ou estados para a interface;
- servir como ponte entre interface e domínio.

A camada de aplicação não deve desenhar tela.

---

## 7.3 Camada de interface gráfica

Diretório sugerido:

```text
src/simple_chess/ui/
```

Responsável por interação visual com o usuário.

Responsabilidades:

- abrir a janela do jogo;
- desenhar o tabuleiro;
- desenhar peças;
- capturar eventos de mouse;
- converter cliques em coordenadas do tabuleiro;
- solicitar ações à camada de aplicação;
- redesenhar a tela conforme o estado atual.

A interface gráfica não deve decidir se um movimento é válido.

---

## 8. Fluxo básico de execução

O fluxo inicial esperado é:

```text
1. Usuário abre o jogo.
2. A aplicação inicializa o estado da partida.
3. A interface renderiza o tabuleiro inicial.
4. O usuário seleciona uma peça.
5. O usuário seleciona uma casa de destino.
6. A interface envia a intenção de movimento para a camada de aplicação.
7. A camada de aplicação consulta o domínio.
8. O domínio valida o movimento com apoio do python-chess.
9. Se o movimento for válido, o estado da partida é atualizado.
10. Se o movimento for inválido, o estado é preservado e uma mensagem pode ser exibida.
11. A interface redesenha o tabuleiro.
```

---

## 9. Regras de dependência

As dependências devem seguir esta direção:

```text
ui → app → domain → python-chess
```

Regras:

- `domain/` não deve importar `ui/`;
- `domain/` não deve depender de Pygame;
- `app/` não deve depender de detalhes de renderização;
- `ui/` pode depender de `app/`, mas não deve manipular diretamente estruturas internas do motor de regras;
- `python-chess` deve ficar encapsulado no domínio.

---

## 10. Estado da aplicação

O estado mínimo da aplicação deve incluir:

- posição atual do tabuleiro;
- turno atual;
- peça ou casa selecionada, quando aplicável;
- histórico de movimentos, se necessário;
- estado da partida: em andamento, xeque, xeque-mate, empate ou finalizada;
- mensagem de feedback para o usuário, quando aplicável.

O estado não precisa ser persistido em banco de dados no escopo inicial.

---

## 11. Persistência

Não haverá banco de dados na arquitetura inicial.

Persistência de partidas, histórico em arquivo, PGN ou salvamento local podem ser considerados futuramente, mas não fazem parte da fundação inicial.

---

## 12. Escopo fora da arquitetura inicial

Ficam fora do escopo arquitetural inicial:

- aplicação web;
- API HTTP;
- banco de dados;
- multiplayer online;
- autenticação;
- ranking de jogadores;
- engine própria de IA adversária;
- implementação manual completa das regras do xadrez;
- Clean Architecture rígida;
- arquitetura orientada a eventos;
- integração direta do jogo com n8n em tempo de execução.

---

## 13. Relação com SIC

Este projeto deve ser desenvolvido de forma compatível com a metodologia SIC.

A separação esperada é:

```text
State   → memória operacional do projeto
Intent  → objetivo específico de cada próxima implementação
Control → execução controlada da alteração
```

Este documento pertence ao eixo de arquitetura do projeto e não deve ser tratado como plano de implementação detalhado.

Ele define limites, decisões e estrutura esperada, mas não substitui issues, milestones ou controles de execução.

---

## 14. Relação com n8n-local-stack

O projeto `simple-chess-python` poderá ser usado como projeto-alvo para validar workflows do `n8n-local-stack`.

No entanto:

- o jogo não deve depender do n8n para funcionar;
- o n8n não deve ser parte da arquitetura runtime do jogo;
- workflows externos podem validar documentação, estrutura, testes e convenções;
- o repositório do jogo deve continuar independente e executável localmente.

Essa separação preserva o limite entre projeto-alvo e plataforma de automação.

---

## 15. Estratégia incremental sugerida

A evolução recomendada é:

```text
1. Criar estrutura base do projeto.
2. Configurar pyproject.toml.
3. Criar camada de domínio com integração mínima ao python-chess.
4. Criar camada de aplicação para coordenar movimentos.
5. Criar interface Pygame mínima com tabuleiro renderizado.
6. Permitir movimentação básica por clique.
7. Adicionar feedback visual de seleção e movimento inválido.
8. Adicionar testes automatizados de domínio e aplicação.
9. Adicionar validações automatizáveis para uso no pipeline n8n.
```

Essa estratégia deve ser futuramente detalhada em `docs/milestones.md`.

---

## 16. Riscos arquiteturais

### 16.1 Acoplamento excessivo da interface com regras

Risco:

A interface Pygame pode acabar concentrando regras do jogo, estado da partida e renderização ao mesmo tempo.

Mitigação:

Manter validação e estado nas camadas `app/` e `domain/`.

---

### 16.2 Overengineering

Risco:

O projeto pode crescer em formalismo antes de ter uma versão jogável simples.

Mitigação:

Evitar padrões arquiteturais pesados e priorizar uma implementação incremental.

---

### 16.3 Dependência espalhada de python-chess

Risco:

A biblioteca `python-chess` pode ser usada diretamente em várias partes do projeto, dificultando futuras alterações.

Mitigação:

Encapsular o uso da biblioteca dentro da camada de domínio.

---

### 16.4 Desvio de propósito

Risco:

O projeto pode deixar de ser um caso simples para teste SIC + n8n e virar um projeto grande de engine de xadrez.

Mitigação:

Manter o escopo inicial limitado a jogo local simples, com interface gráfica e regras apoiadas por biblioteca externa.

---

## 17. Decisões registradas

### ADR-001 — Arquitetura modular simples

Decisão:

Adotar arquitetura modular simples em camadas leves.

Motivo:

O projeto é pequeno e precisa ser compreensível, testável e adequado para evolução incremental.

Consequência:

O projeto terá separação entre domínio, aplicação e interface, mas sem formalismo excessivo.

---

### ADR-002 — Uso de Pygame para interface

Decisão:

Usar Pygame como biblioteca gráfica inicial.

Motivo:

Pygame é adequado para jogos 2D simples e permite implementar tabuleiro, peças e interação por clique de forma direta.

Consequência:

A aplicação será local e desktop, sem necessidade de navegador ou servidor web.

---

### ADR-003 — Uso de python-chess para regras

Decisão:

Usar `python-chess` como motor inicial de regras.

Motivo:

Evita bugs complexos nas regras do xadrez e mantém o foco do projeto na estrutura, interface e validação pelo pipeline.

Consequência:

A implementação inicial não será uma engine própria de xadrez.

---

### ADR-004 — Encapsulamento do motor de regras

Decisão:

Encapsular `python-chess` dentro da camada de domínio.

Motivo:

Evitar acoplamento espalhado com uma dependência externa.

Consequência:

A interface e a camada de aplicação devem conversar com abstrações internas do projeto, não diretamente com a biblioteca externa.

---

### ADR-005 — n8n fora do runtime do jogo

Decisão:

Manter o n8n fora da arquitetura runtime do jogo.

Motivo:

O n8n será usado como plataforma externa de automação, validação e workflow, não como dependência funcional do jogo.

Consequência:

O jogo deve funcionar localmente sem depender do `n8n-local-stack`.

---

## 18. Critério de aderência arquitetural

Uma implementação estará aderente a este documento se:

- o jogo executar localmente;
- a interface estiver separada das regras;
- `python-chess` estiver encapsulado no domínio;
- testes automatizados cobrirem ao menos domínio e aplicação;
- o projeto não depender de n8n para funcionar;
- a estrutura permanecer simples e compreensível;
- novas decisões relevantes forem registradas antes de alterar significativamente a arquitetura.

---

## 19. Próximo documento recomendado

Após este documento, o próximo pilar recomendado é:

```text
docs/milestones.md
```

Esse documento deve transformar a visão e a arquitetura em etapas incrementais de implementação.
