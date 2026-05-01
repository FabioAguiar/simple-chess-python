# Milestones — Simple Chess Python

## 1. Propósito do documento

Este documento define o plano inicial de milestones do projeto `simple-chess-python`.

O objetivo é transformar a visão e a arquitetura já consolidadas em uma sequência incremental de capacidades encerráveis, verificáveis e adequadas para execução futura por meio do fluxo SIC e do pipeline de workflows do `n8n-local-stack`.

Este documento não é uma lista de issues detalhadas.

Este documento não implementa código.

Este documento não substitui `docs/vision.md`, `docs/architecture.md`, issues formais, States, Intents ou Controls futuros.

---

## 2. Relação com Vision e Architecture

O `docs/vision.md` define o propósito macro do projeto: criar um jogo simples de xadrez em Python, local, pequeno, versionável, incremental e adequado para testar a aplicação prática do SIC e do pipeline do `n8n-local-stack`.

O `docs/architecture.md` consolida as decisões técnicas iniciais:

- aplicação local, não web;
- arquitetura modular simples em camadas leves;
- separação entre interface gráfica, camada de aplicação e domínio;
- uso de Pygame para interface gráfica;
- uso de `python-chess` como motor inicial de regras, encapsulado no domínio;
- uso de `pytest` para testes;
- uso de Ruff para lint e formatação;
- ausência de banco de dados na arquitetura inicial;
- manutenção do `n8n-local-stack` fora do runtime do jogo.

As milestones deste documento devem preservar essas decisões.

Mudanças relevantes na direção do produto ou na arquitetura devem ser registradas antes de alterarem o escopo das milestones.

---

## 3. Relação operacional com SIC e n8n-local-stack

O projeto `simple-chess-python` deve ser tratado como projeto-alvo do pipeline de workflows do `n8n-local-stack` desde a primeira milestone de implementação.

Isso significa que o pipeline poderá apoiar atividades como:

- leitura dos documentos fundacionais;
- identificação da milestone vigente;
- geração de drafts de issues;
- geração de State, Intent e Control;
- apoio à implementação controlada;
- execução de validações;
- revisão pós-implementação;
- atualização documental quando necessário;
- registro de evidências sanitizadas.

O `n8n-local-stack`, porém, não faz parte do runtime do jogo.

O jogo deve continuar:

- executável localmente;
- independente do n8n;
- sem dependência funcional de workflows externos;
- sem integração runtime obrigatória com automações.

As milestones abaixo representam capacidades do projeto de xadrez. O n8n é o meio externo de orquestração do processo, não uma funcionalidade interna do jogo.

---

## 4. Critérios gerais de planejamento

Cada milestone deve representar uma capacidade encerrável e validável.

Uma milestone será considerada bem definida quando possuir:

- objetivo claro;
- escopo núcleo;
- fora de escopo explícito;
- dependências conhecidas;
- critérios de conclusão;
- evidência mínima esperada;
- utilidade para derivação futura de issues.

As milestones não devem ser pequenas a ponto de representarem apenas uma tarefa mecânica, nem grandes a ponto de misturarem capacidades independentes demais.

---

## 5. Lista de milestones

| Milestone | Nome | Tipo | Resultado esperado |
|---|---|---|---|
| M0 | Fundação documental e entrada no fluxo SIC/n8n | Fundação | Projeto documentado e pronto para derivação controlada de issues |
| M1 | Estrutura base Python e configuração do projeto | Fundação técnica | Projeto Python inicial executável e validável |
| M2 | Domínio de xadrez e encapsulamento do motor de regras | Implementação | Domínio mínimo usando `python-chess` de forma encapsulada |
| M3 | Camada de aplicação e controle do fluxo da partida | Implementação | Fluxo de partida coordenado sem dependência da interface gráfica |
| M4 | Interface gráfica local com Pygame | Implementação | Janela local com tabuleiro renderizado e entrada básica |
| M5 | Jogabilidade local mínima | Implementação | Dois jogadores conseguem realizar uma partida simples no mesmo ambiente |
| M6 | Testes, lint e validação arquitetural | Validação | Projeto validável por testes, Ruff e critérios arquiteturais |
| M7 | Execução local documentada e fechamento da versão inicial | Fechamento | Versão inicial documentada, executável e pronta para revisão de milestone |

---

## M0 — Fundação documental e entrada no fluxo SIC/n8n

### Objetivo

Consolidar os documentos fundacionais mínimos do projeto e permitir que o repositório seja usado como alvo do pipeline do `n8n-local-stack` desde as primeiras execuções controladas.

### Capacidade entregue

Ao final desta milestone, o projeto terá direção macro, decisões arquiteturais e planejamento incremental suficientes para orientar a geração futura de issues e execuções pelo SIC.

### Escopo núcleo

- Criar ou revisar `README.md`.
- Criar ou revisar `docs/vision.md`.
- Criar ou revisar `docs/architecture.md`.
- Criar ou revisar `docs/milestones.md`.
- Garantir coerência entre visão, arquitetura e milestones.
- Registrar que o n8n atua como orquestrador externo do processo, não como runtime do jogo.

### Fora de escopo

- Implementar código do jogo.
- Criar workflows do n8n dentro deste repositório.
- Criar issues detalhadas de implementação sem etapa própria de derivação.
- Automatizar gameplay pelo n8n.

### Dependências

- Definição inicial do propósito do projeto.
- Decisões arquiteturais iniciais aprovadas.
- Documentação SIC disponível como referência metodológica.

### Critérios de conclusão

- `README.md` existe e descreve o projeto de forma mínima.
- `docs/vision.md` existe e define propósito, escopo e limites macro.
- `docs/architecture.md` existe e consolida decisões técnicas iniciais.
- `docs/milestones.md` existe e organiza a evolução incremental do projeto.
- Os documentos não tratam o n8n como dependência runtime do jogo.
- Os documentos permitem derivação futura de issues sem necessidade de redescobrir a direção geral do projeto.

### Evidência mínima esperada

- Arquivos fundacionais versionáveis no repositório.
- Revisão textual de coerência entre visão, arquitetura e milestones.
- Ausência de arquivos sensíveis, caches ou artefatos de runtime versionados.

### Observações para geração futura de issues

Issues derivadas desta milestone devem focar apenas em ajustes documentais, alinhamento SIC e correções de coerência entre documentos fundacionais.

---

## M1 — Estrutura base Python e configuração do projeto

### Objetivo

Criar a fundação técnica mínima do projeto Python, respeitando a estrutura arquitetural definida e permitindo execução, instalação local e validações iniciais.

### Capacidade entregue

Ao final desta milestone, o repositório terá uma estrutura Python organizada, com configuração mínima de dependências, ponto de entrada inicial e ferramentas básicas de qualidade preparadas.

### Escopo núcleo

- Criar `pyproject.toml` simples.
- Definir dependências iniciais do projeto.
- Definir dependências de desenvolvimento.
- Criar estrutura `src/simple_chess/`.
- Criar pacotes `app/`, `domain/` e `ui/` conforme a arquitetura.
- Criar ponto de entrada inicial da aplicação.
- Criar estrutura inicial de testes.
- Configurar Ruff de forma simples.
- Garantir compatibilidade com ambiente Conda sem tornar Conda uma dependência documental rígida.

### Fora de escopo

- Implementar regras completas do xadrez.
- Implementar interface gráfica funcional completa.
- Implementar jogabilidade real.
- Criar empacotamento avançado.
- Criar workflows n8n dentro do projeto.

### Dependências

- M0 concluída ou suficientemente estável.
- `docs/architecture.md` aprovado.

### Critérios de conclusão

- A estrutura base do projeto existe.
- O pacote `simple_chess` pode ser importado.
- O projeto possui configuração inicial em `pyproject.toml`.
- `ruff` pode ser executado sobre o projeto.
- `pytest` pode ser executado, ainda que com testes mínimos.
- A estrutura inicial respeita a separação `ui → app → domain`.

### Evidência mínima esperada

- Estrutura de diretórios versionada.
- `pyproject.toml` versionado.
- Execução bem-sucedida de comandos mínimos de validação disponíveis no momento.
- Registro de limitações caso algum comando ainda seja apenas estrutural.

### Observações para geração futura de issues

Issues futuras podem separar configuração do projeto, estrutura de pacotes, configuração de Ruff, configuração de pytest e documentação de comandos iniciais.

---

## M2 — Domínio de xadrez e encapsulamento do motor de regras

### Objetivo

Implementar a base do domínio do jogo, encapsulando o uso de `python-chess` para representar estado, validar movimentos e consultar condições essenciais da partida.

### Capacidade entregue

Ao final desta milestone, o projeto terá uma camada de domínio mínima capaz de representar uma partida de xadrez e validar movimentos sem expor `python-chess` diretamente para a interface gráfica.

### Escopo núcleo

- Criar abstração interna para o tabuleiro.
- Criar abstração interna para movimentos.
- Encapsular inicialização e estado de `python-chess`.
- Validar movimentos legais.
- Rejeitar movimentos inválidos.
- Consultar turno atual.
- Consultar estado básico da partida.
- Expor API interna simples para a camada de aplicação.
- Criar testes de domínio para casos essenciais.

### Fora de escopo

- Implementar manualmente todas as regras de xadrez do zero.
- Criar engine própria de IA.
- Criar interface gráfica.
- Tratar refinamentos visuais.
- Persistir partidas.

### Dependências

- M1 concluída.
- Dependência `python-chess` definida no projeto.
- Estrutura `domain/` existente.

### Critérios de conclusão

- O domínio inicializa uma partida padrão.
- Movimentos válidos podem ser aplicados.
- Movimentos inválidos são rejeitados.
- O turno atual pode ser consultado.
- A camada de domínio não depende de Pygame.
- O uso de `python-chess` está concentrado no domínio.
- Testes de domínio cobrem casos mínimos.

### Evidência mínima esperada

- Testes automatizados de domínio passando.
- Código do domínio sem importações de `ui/` ou Pygame.
- Evidência de que `python-chess` não foi espalhado pela interface.

### Observações para geração futura de issues

Issues futuras podem separar abstração de tabuleiro, abstração de movimento, integração com `python-chess`, consulta de estado da partida e testes de domínio.

---

## M3 — Camada de aplicação e controle do fluxo da partida

### Objetivo

Implementar a camada de aplicação responsável por coordenar seleção de peças, tentativa de movimento, atualização de estado e feedback para a interface.

### Capacidade entregue

Ao final desta milestone, o jogo terá um controlador de partida utilizável sem interface gráfica, capaz de receber intenções de movimento e responder com estado atualizado ou mensagens de erro.

### Escopo núcleo

- Criar controlador de jogo na camada `app/`.
- Controlar seleção de origem e destino.
- Enviar tentativas de movimento ao domínio.
- Atualizar estado da partida após movimento válido.
- Preservar estado após movimento inválido.
- Expor dados necessários para a interface renderizar o tabuleiro.
- Expor mensagens simples de feedback.
- Criar testes da camada de aplicação sem depender de Pygame.

### Fora de escopo

- Renderizar tabuleiro.
- Capturar eventos de mouse.
- Implementar lógica visual.
- Criar persistência de partidas.
- Criar IA adversária.

### Dependências

- M2 concluída.
- API interna do domínio minimamente estável.

### Critérios de conclusão

- A camada de aplicação coordena movimentos usando o domínio.
- A camada de aplicação não desenha tela.
- A camada de aplicação não depende de Pygame.
- Estados de sucesso e erro são distinguíveis.
- Testes da camada de aplicação cobrem fluxo básico de movimento válido e inválido.

### Evidência mínima esperada

- Testes automatizados da camada de aplicação passando.
- Ausência de dependência direta de renderização na camada `app/`.
- Registro claro de dados expostos para a interface.

### Observações para geração futura de issues

Issues futuras podem separar controlador de partida, estado de aplicação, feedback de movimentos e testes de fluxo.

---

## M4 — Interface gráfica local com Pygame

### Objetivo

Criar a primeira interface gráfica local com Pygame, capaz de abrir uma janela, renderizar o tabuleiro e capturar interações básicas do usuário.

### Capacidade entregue

Ao final desta milestone, o usuário poderá abrir a aplicação localmente e visualizar um tabuleiro de xadrez renderizado em uma janela Pygame.

### Escopo núcleo

- Inicializar janela Pygame.
- Renderizar tabuleiro 8x8.
- Representar peças de forma compreensível.
- Capturar cliques do mouse.
- Converter coordenadas de tela em casas do tabuleiro.
- Integrar a interface à camada de aplicação.
- Redesenhar o tabuleiro conforme o estado atual.

### Fora de escopo

- Refinamento visual avançado.
- Animações complexas.
- Sons.
- Temas gráficos configuráveis.
- Testes automatizados completos da interface gráfica.
- Multiplayer online.

### Dependências

- M3 concluída.
- Dependência Pygame definida no projeto.
- Dados de estado expostos pela camada de aplicação.

### Critérios de conclusão

- A aplicação abre uma janela local.
- O tabuleiro é renderizado de forma compreensível.
- As peças são representadas visualmente ou por símbolos claros.
- Cliques em casas do tabuleiro são capturados.
- A interface não decide diretamente se um movimento é válido.
- A interface delega regras e estado para as camadas `app/` e `domain/`.

### Evidência mínima esperada

- Execução local da interface.
- Registro de comando de execução.
- Verificação estrutural de que `ui/` depende de `app/`, mas não concentra regras do jogo.

### Observações para geração futura de issues

Issues futuras podem separar janela Pygame, renderização do tabuleiro, renderização das peças, conversão de coordenadas e integração com o controlador.

---

## M5 — Jogabilidade local mínima

### Objetivo

Integrar domínio, aplicação e interface para permitir uma partida local simples entre dois jogadores no mesmo ambiente.

### Capacidade entregue

Ao final desta milestone, dois jogadores poderão mover peças alternadamente em uma partida local, com validação de movimentos e atualização visual do tabuleiro.

### Escopo núcleo

- Permitir seleção de peça por clique.
- Permitir seleção de casa de destino por clique.
- Aplicar movimentos válidos.
- Rejeitar movimentos inválidos.
- Alternar turnos corretamente.
- Atualizar o tabuleiro após cada movimento válido.
- Exibir feedback simples para movimento inválido.
- Indicar estado básico da partida quando disponível.

### Fora de escopo

- IA adversária.
- Multiplayer online.
- Relógio de xadrez.
- Salvamento e carregamento de partidas.
- Histórico visual avançado.
- Sistema de ranking.
- Controle do gameplay pelo n8n.

### Dependências

- M4 concluída.
- Integração estável entre `ui/`, `app/` e `domain/`.

### Critérios de conclusão

- Uma partida pode ser iniciada localmente.
- Movimentos válidos alteram o estado e a tela.
- Movimentos inválidos não alteram indevidamente o estado.
- Turnos são respeitados.
- Capturas básicas funcionam conforme regras do motor encapsulado.
- Condições essenciais de xeque ou encerramento são tratadas conforme suporte do domínio.
- A aplicação continua independente do n8n em runtime.

### Evidência mínima esperada

- Execução manual validada localmente.
- Testes de domínio e aplicação passando.
- Comando documentado para iniciar o jogo.
- Registro de limitações conhecidas de jogabilidade, se houver.

### Observações para geração futura de issues

Issues futuras podem separar seleção de peças, aplicação de movimento, feedback visual, alternância de turnos e estado de fim de jogo.

---

## M6 — Testes, lint e validação arquitetural

### Objetivo

Consolidar a validação técnica do projeto por meio de testes automatizados, lint/formatação e verificação de aderência arquitetural.

### Capacidade entregue

Ao final desta milestone, o projeto terá uma base mínima de validação capaz de sustentar revisões futuras e execuções pelo pipeline do `n8n-local-stack`.

### Escopo núcleo

- Ampliar testes de domínio.
- Ampliar testes da camada de aplicação.
- Validar comandos de `pytest`.
- Validar comandos de Ruff.
- Documentar comandos de validação.
- Verificar aderência à separação `ui → app → domain`.
- Registrar lacunas conhecidas de cobertura.
- Garantir que artefatos locais e caches não sejam versionados.

### Fora de escopo

- Testes automatizados completos da interface Pygame, salvo se simples e viáveis.
- Cobertura absoluta de todas as regras possíveis do xadrez.
- Pipeline n8n implementado dentro deste repositório.
- Garantia de distribuição multiplataforma.

### Dependências

- M5 concluída ou suficientemente funcional.
- Testes iniciais já existentes.
- Configuração de Ruff existente.

### Critérios de conclusão

- `pytest` executa com sucesso.
- `ruff check` executa com sucesso ou possui exceções justificadas.
- `ruff format` ou comando equivalente está documentado.
- Testes cobrem domínio e aplicação em cenários essenciais.
- Aderência arquitetural mínima foi revisada.
- Lacunas de validação foram registradas.

### Evidência mínima esperada

- Resultado de execução dos comandos de teste e lint.
- Registro textual de validação.
- Lista de lacunas não bloqueantes, se existirem.

### Observações para geração futura de issues

Issues futuras podem separar cobertura de domínio, cobertura de aplicação, comandos de validação, ajustes de Ruff e revisão de aderência arquitetural.

---

## M7 — Execução local documentada e fechamento da versão inicial

### Objetivo

Consolidar a versão inicial do projeto como aplicação local executável, documentada e revisável.

### Capacidade entregue

Ao final desta milestone, o projeto terá uma versão inicial jogável, com comandos documentados, limitações conhecidas registradas e condições suficientes para revisão de milestone.

### Escopo núcleo

- Revisar `README.md` com instruções de instalação, execução e validação.
- Documentar dependências principais.
- Documentar comandos de execução local.
- Documentar comandos de teste e lint.
- Registrar limitações conhecidas da versão inicial.
- Revisar coerência entre documentação e implementação.
- Preparar evidência mínima de fechamento da versão inicial.

### Fora de escopo

- Publicação de release formal em pacote distribuível.
- Instalador gráfico.
- Distribuição em loja ou plataforma externa.
- Empacotamento avançado com executável standalone.
- Novas funcionalidades de gameplay não planejadas.

### Dependências

- M6 concluída.
- Jogo local minimamente jogável.
- Comandos de validação funcionando.

### Critérios de conclusão

- O jogo pode ser executado localmente a partir de instruções documentadas.
- O README reflete o estado real do projeto.
- Testes e lint possuem comandos documentados.
- Limitações conhecidas foram registradas.
- O projeto permanece dentro do escopo definido pela visão e arquitetura.
- Há base suficiente para uma revisão de milestone ou planejamento de ciclo futuro.

### Evidência mínima esperada

- README revisado.
- Comandos documentados.
- Resultado de validação disponível.
- Registro de limitações e próximos possíveis incrementos.

### Observações para geração futura de issues

Issues futuras podem separar atualização de README, documentação de comandos, registro de limitações, revisão de consistência e preparação de evidência de fechamento.

---

## 6. Observações para geração futura de issues

As issues futuras devem ser derivadas de uma milestone vigente e devem preservar os limites deste documento.

Uma issue deve:

- declarar a milestone relacionada;
- declarar objetivo específico;
- declarar escopo e fora de escopo;
- indicar arquivos prováveis ou áreas afetadas;
- indicar critérios de aceitação;
- indicar validações esperadas;
- respeitar Vision e Architecture;
- manter o n8n fora do runtime do jogo.

Issues não devem:

- introduzir funcionalidades fora do escopo sem decisão explícita;
- alterar a arquitetura sem registrar a decisão;
- espalhar `python-chess` fora do domínio;
- colocar regras de xadrez dentro da interface gráfica;
- transformar o projeto em aplicação web;
- adicionar banco de dados sem nova decisão arquitetural;
- automatizar gameplay pelo n8n.

---

## 7. Sequência recomendada

A sequência recomendada é:

```text
M0 → M1 → M2 → M3 → M4 → M5 → M6 → M7
```

M0 representa a fundação documental e pode ser considerada a milestone de entrada do projeto no fluxo SIC/n8n.

M1 é a primeira milestone de implementação técnica.

M2 a M5 constroem a capacidade funcional do jogo.

M6 consolida validação técnica e aderência arquitetural.

M7 fecha a versão inicial como aplicação local documentada e revisável.

---

## 8. Agrupamentos rejeitados

### 8.1 Criar uma milestone final de preparação para n8n

Rejeitado.

Motivo: o projeto será conduzido pelo pipeline do `n8n-local-stack` desde o início da implementação. Portanto, a relação com n8n é transversal e operacional, não uma capacidade final do jogo.

### 8.2 Implementar interface, domínio e aplicação em uma única milestone

Rejeitado.

Motivo: isso misturaria responsabilidades diferentes e dificultaria validação incremental.

### 8.3 Criar uma milestone para engine própria de xadrez

Rejeitado.

Motivo: a arquitetura decidiu usar `python-chess` como motor inicial de regras, encapsulado no domínio.

### 8.4 Criar uma milestone para aplicação web

Rejeitado.

Motivo: o projeto é explicitamente local e não web.

### 8.5 Criar uma milestone para integração runtime com n8n

Rejeitado.

Motivo: o n8n atua como orquestrador externo de processo, não como dependência funcional do jogo.

---

## 9. Lacunas conhecidas

As lacunas abaixo não bloqueiam o início da implementação, mas devem ser tratadas quando se tornarem relevantes:

- licença do projeto;
- nível final de refinamento visual;
- presença ou não de histórico de movimentos;
- presença ou não de desfazer jogada;
- presença ou não de salvamento local;
- formato final das issues formais derivadas de cada milestone;
- critérios operacionais específicos definidos no projeto `n8n-local-stack` para execução de cada etapa.

---

## 10. Critério macro de fechamento da versão inicial

A versão inicial do projeto poderá ser considerada concluída quando:

- o jogo executar localmente;
- dois jogadores puderem jogar no mesmo ambiente;
- o tabuleiro e as peças forem compreensíveis;
- turnos forem respeitados;
- movimentos inválidos forem rejeitados;
- capturas funcionarem;
- regras essenciais de xeque ou encerramento forem tratadas conforme suporte do domínio;
- testes mínimos de domínio e aplicação existirem;
- comandos de execução e validação estiverem documentados;
- a estrutura respeitar a arquitetura definida;
- o projeto permanecer independente do n8n em runtime;
- o repositório puder ser usado pelo pipeline do `n8n-local-stack` para implementação, validação e revisão externas.
