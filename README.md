# Simple Chess Python

Projeto inicial de um jogo simples de xadrez desenvolvido em Python.

Este repositório nasce com dois objetivos principais:

1. implementar um jogo de xadrez simples, funcional e compreensível;
2. servir como projeto de teste para um pipeline de workflows do `n8n-local-stack`, usando a documentação SIC como método de orientação, continuidade e validação.

O foco inicial não é criar um motor de xadrez avançado, uma IA competitiva ou uma aplicação complexa. O foco é construir um projeto pequeno, rastreável e adequado para testar o fluxo documental e operacional do SIC.

---

## Status atual

Projeto em fase inicial.

Neste momento, o repositório contém apenas a documentação fundacional mínima:

```text
README.md
.gitignore
docs/
  vision.md
```

A implementação do jogo ainda não foi iniciada.

---

## Objetivos do projeto

O projeto deve permitir, ao final da visão central:

- jogar uma partida simples de xadrez em Python;
- representar tabuleiro, peças, turnos e movimentos legais essenciais;
- impedir movimentos inválidos básicos;
- reconhecer condições fundamentais de encerramento ou continuidade da partida;
- manter documentação suficiente para orientar próximas etapas via SIC;
- funcionar como projeto de validação para workflows do `n8n-local-stack`.

---

## Relação com SIC

Este projeto será conduzido com apoio do SIC — Structured Intent Control.

A documentação do projeto deve preservar a separação entre:

- **State**: memória operacional e contexto acumulado;
- **Intent**: intenção explícita de cada tarefa;
- **Control**: execução controlada, validação e geração de artefatos.

O projeto também deve respeitar o fluxo fundacional recomendado:

```text
Vision Spec
→ Architecture Discovery
→ Architecture Decision
→ Architecture Documentation
→ Milestones
→ Issues
```

Por isso, este repositório começa pelo documento `docs/vision.md`. O próximo pilar previsto é o documento `docs/architecture.md`.

---

## Escopo inicial

O núcleo do projeto é um jogo de xadrez simples.

Faz parte do escopo inicial:

- implementação em Python;
- regras essenciais do xadrez;
- fluxo de partida local;
- interface simples, ainda não definida;
- código legível e adequado para aprendizado;
- documentação mínima para continuidade com IA e workflows.

Não faz parte do escopo inicial:

- motor de IA competitivo;
- multiplayer online;
- ranking;
- autenticação de usuários;
- persistência complexa;
- integração obrigatória com serviços externos;
- suporte completo a torneios ou relógio de xadrez.

---

## Estrutura planejada

A estrutura ainda será definida no documento de arquitetura.

Estrutura mínima atual:

```text
simple-chess-python/
  README.md
  .gitignore
  docs/
    vision.md
```

Possíveis diretórios futuros, ainda não consolidados:

```text
src/
tests/
docs/
```

Esses diretórios só devem ser tratados como definitivos após a criação do `docs/architecture.md`.

---

## Execução local

Ainda não há aplicação executável.

A criação do ambiente Python e a escolha das dependências serão definidas em etapa posterior, após a consolidação arquitetural inicial.

---

## Próximo passo previsto

O próximo documento fundacional do projeto será:

```text
docs/architecture.md
```

Esse documento deve decidir, de forma proporcional ao tamanho do projeto:

- biblioteca gráfica ou abordagem inicial de interface;
- organização dos módulos;
- fronteiras entre regra de jogo, estado da partida e apresentação;
- estratégia mínima de testes;
- critérios para evitar overengineering.

---

## Licença

Licença ainda não definida.
