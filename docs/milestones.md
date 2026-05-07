# Milestones

## Finalidade

Este documento registra o planejamento consolidado de milestones do projeto `simple-chess-python`.

O objetivo do `docs/milestones.md` é organizar a evolução planejada do projeto em capacidades verificáveis, deriváveis e proporcionais ao escopo definido em `docs/vision.md` e `docs/architecture.md`.

Este documento serve para:

- orientar continuidade do projeto;
- apoiar validação documental e arquitetural;
- apoiar derivação futura de drafts de issues;
- preservar os limites definidos na visão;
- respeitar as fronteiras arquiteturais definidas;
- permitir que workflows externos do `n8n-local-stack` leiam o planejamento sem assumir execução automática.

Este documento não substitui State operacional, não define milestone vigente, não autoriza execução automática, não gera issues formais e não publica alterações.

---

## Regras de leitura

A ordem das milestones indica a sequência planejada de evolução do projeto.

A ordem textual não deve ser usada como único cursor operacional. Se o workflow precisar identificar a milestone vigente, essa informação deve ser lida de um State operacional próprio, como `docs/project-status/milestone-state.json`, caso esse artefato venha a ser adotado.

Issues previstas neste documento são apenas candidatas a drafts futuros. Elas não são issues formais, não representam backlog publicado e não autorizam implementação.

Critérios de derivação indicam como uma milestone pode ser quebrada futuramente em drafts de issues, mas não autorizam execução, patch, commit, pull request, publicação ou alteração de State operacional.

Nenhuma milestone deste documento autoriza integração runtime com o `n8n-local-stack`. O n8n deve ser tratado como orquestrador externo do processo de implementação, validação e revisão, não como parte interna do jogo.

---

## Relação com State operacional

A separação esperada é:

```text
docs/milestones.md = planejamento
docs/project-status/milestone-state.json = State operacional, se adotado
workflow/scripts/validações = Control
runtime = execução local do jogo
```

Este documento define capacidades planejadas.

Ele não registra estado de execução, não informa qual milestone está ativa e não substitui artefatos operacionais de controle.

Se o projeto ainda não possuir `milestone-state.json`, a milestone vigente deve ser controlada por State operacional próprio caso o pipeline do `n8n-local-stack` precise desse controle.

---

## Relação com Vision e Architecture

O `docs/vision.md` define o propósito macro do projeto: criar um jogo simples de xadrez em Python, local, compreensível, incremental e adequado como projeto controlado para aplicação prática do SIC e workflows do `n8n-local-stack`.

O `docs/architecture.md` define as decisões estruturais iniciais:

- aplicação local, não web;
- Python como linguagem principal;
- Pygame como interface gráfica;
- arquitetura modular simples em camadas leves;
- separação entre interface, aplicação e domínio;
- uso de `python-chess` encapsulado na camada de domínio;
- uso de `pytest` para testes;
- uso de Ruff para lint e formatação;
- manutenção do `n8n-local-stack` fora do runtime do jogo.

Este documento transforma essas decisões em planejamento de capacidades. Ele não redefine visão, não altera arquitetura e não cria escopo novo.

---

## Relação operacional com SIC e n8n-local-stack

O projeto `simple-chess-python` será usado como projeto-alvo do pipeline de workflows do `n8n-local-stack` desde as primeiras milestones de implementação.

Isso significa que o pipeline poderá apoiar atividades como:

- leitura dos documentos fundacionais;
- identificação da milestone vigente a partir de State operacional próprio, se existir;
- geração posterior de drafts de issues;
- análise estruturada;
- geração de State, Intent e Control quando aplicável;
- apoio à implementação;
- validação;
- revisão;
- atualização documental controlada.

Essa relação é transversal às milestones.

Não deve existir uma milestone final apenas para “preparar o projeto para o n8n”, pois o projeto já nasce como alvo do pipeline após a consolidação documental inicial.

O `n8n-local-stack` não faz parte do runtime do jogo. O jogo deve continuar independente, executável localmente e sem dependência funcional do n8n.

---

## Visão geral das milestones

| Milestone | Título | Propósito | Dependências | Derivável em issues |
|---|---|---|---|---|
| M1 | Fundação documental e entrada no fluxo SIC/n8n | Consolidar os documentos fundacionais mínimos para orientar o projeto e permitir leitura por workflows externos | `README.md`, `docs/vision.md`, `docs/architecture.md` | Sim |
| M2 | Estrutura base Python e configuração do projeto | Criar a fundação técnica mínima do projeto Python local | M1 | Sim |
| M3 | Domínio de xadrez e encapsulamento do motor de regras | Criar a camada de domínio com uso encapsulado de `python-chess` | M2 | Sim |
| M4 | Camada de aplicação e controle da partida | Criar a camada que coordena estado, seleção, movimentos e fluxo da partida | M3 | Sim |
| M5 | Interface gráfica local com Pygame | Criar a interface local mínima para visualizar e interagir com o tabuleiro | M4 | Sim |
| M6 | Jogabilidade local mínima | Integrar domínio, aplicação e interface em uma experiência jogável local | M5 | Sim |
| M7 | Testes, lint e validação arquitetural | Validar comportamento central, qualidade de código e aderência às fronteiras arquiteturais | M6 | Sim |
| M8 | Execução local documentada e fechamento da versão inicial | Consolidar documentação de uso, critérios de fechamento e evidência mínima da versão inicial | M7 | Com ressalvas |

---

## M1 — Fundação documental e entrada no fluxo SIC/n8n

### Objetivo

Consolidar a fundação documental mínima do projeto para orientar sua evolução e permitir que workflows externos do `n8n-local-stack` usem o repositório como projeto-alvo desde as primeiras etapas de implementação.

### Problema ou lacuna

Um projeto greenfield sem documentos fundacionais claros tende a gerar decisões implícitas, escopo instável e dificuldade de continuidade por IA ou workflow externo.

Antes de iniciar implementação, o projeto precisa ter visão, arquitetura e planejamento de milestones suficientemente claros para orientar futuras derivações de issues.

### Contexto

O projeto `simple-chess-python` nasce como um jogo simples de xadrez em Python e também como experimento controlado de aplicação da metodologia SIC.

A visão define o propósito macro e os limites do projeto. A arquitetura define as fronteiras técnicas iniciais. Este documento de milestones deve completar a fundação documental inicial.

### Escopo núcleo

- Consolidar `README.md`.
- Consolidar `docs/vision.md`.
- Consolidar `docs/architecture.md`.
- Consolidar `docs/milestones.md`.
- Registrar que o `n8n-local-stack` atua como orquestrador externo do processo.
- Registrar que o n8n não faz parte do runtime do jogo.
- Preservar separação entre visão, arquitetura, milestones, State, issues e Control.

### Fora de escopo

- Implementar código do jogo.
- Criar estrutura Python completa.
- Gerar issues formais.
- Gerar drafts de issues.
- Definir milestone vigente por ordem textual.
- Criar ou alterar State operacional.
- Integrar runtime do jogo com n8n.
- Automatizar gameplay pelo n8n.
- Publicar no GitHub.

### Entregáveis esperados

- `README.md`.
- `docs/vision.md`.
- `docs/architecture.md`.
- `docs/milestones.md`.
- Registro documental claro da relação entre SIC, projeto e `n8n-local-stack`.

### Dependências

Nenhuma dependência bloqueante identificada.

### Componentes afetados

- Documentation.
- Architecture.
- Milestone Planning.
- Issue Derivation.
- Review Pipeline.
- Project Profiles.
- Validation.

### Issues previstas

- Criar README inicial do projeto.
- Criar ou revisar Vision Spec.
- Criar ou revisar Architecture Spec.
- Criar Milestones Document.
- Validar consistência entre visão, arquitetura e milestones.

### Critérios de derivação de issues

- Separar criação/revisão de cada documento quando houver mudanças significativas.
- Não misturar documentação fundacional com implementação de código.
- Não gerar issue formal a partir deste documento sem etapa posterior de draft e validação.
- Criar issue separada para validação documental se o workflow exigir evidência própria.

### Definition of Done

- `README.md` existe e descreve o projeto de forma compatível com a visão.
- `docs/vision.md` existe e define propósito, escopo núcleo e fora de escopo.
- `docs/architecture.md` existe e define fronteiras técnicas iniciais.
- `docs/milestones.md` existe e organiza as capacidades planejadas.
- O papel do `n8n-local-stack` está descrito como orquestração externa do processo.
- O n8n não é tratado como dependência runtime do jogo.
- Não há conteúdo sensível versionado.
- O documento não define milestone vigente como State operacional.

### Evidência mínima

- Presença dos documentos fundacionais no repositório.
- Revisão textual confirmando coerência entre visão, arquitetura e milestones.
- Evidência reduzida de validação documental, quando o workflow externo exigir.

### Riscos e lacunas

- Risco de confundir planejamento com State operacional.
- Risco de tratar issues previstas como backlog formal.
- Risco de interpretar o n8n como dependência interna do jogo.
- Risco de excesso documental antes da primeira implementação.

### Observações de continuidade

Após esta milestone, a evolução deve seguir para a fundação técnica do projeto Python.

Se o pipeline do `n8n-local-stack` precisar controlar milestone vigente, esse controle deve ocorrer em State operacional próprio, não neste documento.

---

## M2 — Estrutura base Python e configuração do projeto

### Objetivo

Criar a estrutura técnica mínima do projeto Python local, preparando o repositório para receber domínio, aplicação, interface, testes e validações futuras.

### Problema ou lacuna

O repositório precisa deixar de ser apenas documental e passar a ter uma estrutura Python organizada, compatível com a arquitetura aprovada e adequada para evolução incremental.

Sem essa base, futuras implementações podem misturar responsabilidades, dificultar testes e quebrar a separação entre interface, aplicação e domínio.

### Contexto

A arquitetura define uma estrutura modular simples em camadas leves, com diretórios para `app`, `domain` e `ui`.

Esta milestone materializa apenas a base estrutural e de configuração, sem implementar regras de xadrez ou interface funcional.

### Escopo núcleo

- Criar estrutura inicial de diretórios sob `src/simple_chess/`.
- Criar pacotes internos para `app`, `domain` e `ui`.
- Criar ponto de entrada inicial do projeto, sem lógica complexa.
- Criar `pyproject.toml` simples.
- Declarar dependências principais previstas.
- Preparar estrutura inicial de testes.
- Manter compatibilidade com execução local.

### Fora de escopo

- Implementar regras completas do xadrez.
- Implementar interface gráfica jogável.
- Implementar fluxo de partida.
- Criar engine própria de xadrez.
- Criar banco de dados.
- Criar API web.
- Criar workflow n8n dentro deste repositório.
- Alterar State operacional.
- Publicar issues formais.

### Entregáveis esperados

- Estrutura `src/simple_chess/`.
- Pacotes `app`, `domain` e `ui`.
- Arquivos `__init__.py` necessários.
- Arquivo de entrada inicial.
- `pyproject.toml`.
- Estrutura `tests/`.
- Ajustes documentais mínimos se necessários.

### Dependências

- M1 concluída ou suficientemente validada.
- Decisões arquiteturais iniciais disponíveis em `docs/architecture.md`.

### Componentes afetados

- Runtime.
- Project Structure.
- Tooling.
- Documentation.
- Validation.

### Issues previstas

- Criar estrutura base do pacote Python.
- Criar configuração inicial do projeto em `pyproject.toml`.
- Criar estrutura inicial de testes.
- Validar estrutura inicial contra arquitetura.

### Critérios de derivação de issues

- Separar estrutura de diretórios de configuração quando isso facilitar validação.
- Não misturar instalação/configuração com implementação de domínio.
- Não incluir interface gráfica funcional nesta milestone.
- Criar issue separada para ajustes documentais se a estrutura real divergir da arquitetura planejada.

### Definition of Done

- A estrutura principal do projeto existe.
- `pyproject.toml` existe e é coerente com a stack definida.
- Os diretórios `app`, `domain` e `ui` existem.
- A estrutura de testes existe.
- Não há dependência runtime do n8n.
- A estrutura respeita a separação arquitetural planejada.
- Não há arquivos de ambiente, caches ou artefatos locais versionados indevidamente.

### Evidência mínima

- Listagem reduzida da estrutura de arquivos.
- Validação documental de aderência à arquitetura.
- Resultado resumido de validação estrutural, se houver workflow ou script externo.

### Riscos e lacunas

- Risco de criar arquivos prematuros demais.
- Risco de configurar ferramentas além do necessário.
- Risco de misturar camada de aplicação com domínio antes da hora.
- Risco de tratar ambiente Conda como fonte de decisão arquitetural.

### Observações de continuidade

Esta milestone prepara o terreno para a implementação do domínio de xadrez.

A estrutura pode ser simplificada futuramente se algum arquivo planejado se mostrar desnecessário, desde que a decisão seja registrada.

---

## M3 — Domínio de xadrez e encapsulamento do motor de regras

### Objetivo

Criar a camada de domínio responsável por representar o estado central do jogo e encapsular o uso de `python-chess` como motor inicial de regras.

### Problema ou lacuna

O projeto precisa validar movimentos e estados do xadrez sem espalhar dependências externas pela interface ou pela camada de aplicação.

Sem encapsulamento, `python-chess` pode se tornar acoplamento transversal, dificultando testes, manutenção e futura substituição ou extensão.

### Contexto

A arquitetura define que `python-chess` deve ser usado inicialmente para reduzir riscos nas regras do xadrez, mas deve ficar encapsulado na camada de domínio.

Esta milestone implementa a base funcional do domínio, sem interface gráfica e sem fluxo completo de partida.

### Escopo núcleo

- Criar representação interna mínima do tabuleiro.
- Criar abstração para movimentos.
- Encapsular operações essenciais de `python-chess`.
- Permitir consulta de turno atual.
- Permitir validação de movimento.
- Permitir aplicação de movimento válido.
- Permitir rejeição de movimento inválido.
- Expor estado básico da partida.
- Preparar testes mínimos de domínio.

### Fora de escopo

- Criar interface Pygame.
- Criar controle visual de seleção.
- Criar camada completa de aplicação.
- Implementar manualmente todas as regras do xadrez.
- Criar engine de IA.
- Implementar persistência.
- Criar automação de gameplay pelo n8n.
- Criar issue formal.
- Alterar State operacional.

### Entregáveis esperados

- Módulos de domínio.
- Encapsulamento de `python-chess`.
- Abstrações internas mínimas para tabuleiro e movimento.
- Testes iniciais de domínio.
- Documentação atualizada apenas se houver decisão relevante.

### Dependências

- M2 concluída.
- Dependência `python-chess` declarada na configuração do projeto.
- Fronteira `domain → python-chess` preservada.

### Componentes afetados

- Domain.
- Runtime.
- Validation.
- Tests.
- Architecture.

### Issues previstas

- Criar wrapper de domínio para `python-chess`.
- Criar representação mínima de movimento.
- Criar consultas de estado do tabuleiro.
- Criar testes de validação de movimentos básicos.
- Validar que `python-chess` não foi usado fora do domínio.

### Critérios de derivação de issues

- Separar encapsulamento do motor de regras dos testes, se necessário.
- Não misturar domínio com interface gráfica.
- Não implementar regras manualmente quando `python-chess` já resolver o caso inicial.
- Criar issue específica para regra especial apenas se houver lacuna real.

### Definition of Done

- O domínio consegue representar uma partida inicial.
- O domínio consegue validar movimento permitido.
- O domínio rejeita movimento inválido.
- O domínio aplica movimento válido.
- O domínio expõe turno ou estado mínimo necessário.
- `python-chess` permanece encapsulado na camada de domínio.
- Testes mínimos de domínio existem.
- Nenhum módulo de interface depende diretamente de `python-chess`.

### Evidência mínima

- Resultado resumido dos testes de domínio.
- Revisão estrutural confirmando encapsulamento de `python-chess`.
- Evidência reduzida de que a camada `domain` não depende de Pygame.

### Riscos e lacunas

- Risco de vazar objetos de `python-chess` para outras camadas.
- Risco de implementar regra manual desnecessária.
- Risco de criar abstrações demais antes da necessidade.
- Risco de não cobrir regras especiais inicialmente.

### Observações de continuidade

A camada de domínio deve ser estável o suficiente para ser consumida pela camada de aplicação na próxima milestone.

Regras especiais tratadas por `python-chess` podem ser expostas gradualmente conforme a aplicação precisar.

---

## M4 — Camada de aplicação e controle da partida

### Objetivo

Criar a camada de aplicação responsável por coordenar o fluxo da partida entre interface e domínio, incluindo seleção, tentativa de movimento, atualização de estado e mensagens básicas de feedback.

### Problema ou lacuna

O projeto precisa de uma camada intermediária que impeça a interface gráfica de controlar diretamente regras, estado interno do motor ou lógica completa da partida.

Sem essa camada, a interface Pygame tende a acumular renderização, entrada do usuário, validação de movimento e estado do jogo.

### Contexto

A arquitetura define a direção de dependência `ui → app → domain → python-chess`.

Após a criação do domínio, a aplicação deve coordenar intenções de movimento sem depender de detalhes de renderização.

### Escopo núcleo

- Criar controlador de partida.
- Controlar seleção de casa ou peça.
- Receber intenção de movimento.
- Consultar domínio para validar movimento.
- Atualizar estado após movimento válido.
- Preservar estado após movimento inválido.
- Expor dados necessários para a interface renderizar o tabuleiro.
- Expor mensagens básicas de feedback.
- Criar testes da camada de aplicação sem depender de Pygame.

### Fora de escopo

- Implementar renderização Pygame.
- Criar assets gráficos definitivos.
- Implementar IA adversária.
- Implementar multiplayer.
- Implementar persistência.
- Criar API web.
- Alterar regras internas de `python-chess`.
- Criar integração runtime com n8n.

### Entregáveis esperados

- Módulos da camada `app`.
- Controlador de partida.
- Estado de aplicação mínimo.
- Testes da camada de aplicação.
- Ajustes no domínio apenas se necessários para suportar a aplicação.

### Dependências

- M3 concluída.
- Domínio capaz de validar e aplicar movimentos básicos.
- Estrutura `app` disponível.

### Componentes afetados

- Application.
- Domain.
- Runtime.
- Tests.
- Validation.

### Issues previstas

- Criar controlador de jogo.
- Criar estado de aplicação.
- Implementar fluxo de seleção e tentativa de movimento.
- Criar testes da aplicação sem Pygame.
- Validar direção de dependência `app → domain`.

### Critérios de derivação de issues

- Separar estado da aplicação de controle de movimento, se a implementação crescer.
- Não misturar aplicação com renderização.
- Não acessar `python-chess` diretamente pela camada de aplicação se isso violar o encapsulamento.
- Criar issue separada para mensagens de feedback se necessário.

### Definition of Done

- A aplicação consegue iniciar uma partida.
- A aplicação consegue receber uma intenção de movimento.
- Movimentos válidos são aplicados via domínio.
- Movimentos inválidos são rejeitados sem corromper estado.
- A aplicação expõe estado suficiente para a futura interface.
- Testes da camada de aplicação existem e não dependem de Pygame.
- A camada `app` não desenha tela.

### Evidência mínima

- Resultado resumido dos testes de aplicação.
- Revisão estrutural confirmando ausência de dependência com Pygame.
- Evidência reduzida de fluxo válido e inválido de movimento.

### Riscos e lacunas

- Risco de a camada de aplicação duplicar regras do domínio.
- Risco de a aplicação expor detalhes internos demais.
- Risco de a seleção visual ser antecipada antes da interface.
- Risco de acoplamento prematuro com Pygame.

### Observações de continuidade

Esta milestone prepara a criação da interface gráfica.

A interface futura deve consumir a camada de aplicação, não o domínio diretamente para regras e mutações centrais.

---

## M5 — Interface gráfica local com Pygame

### Objetivo

Criar uma interface gráfica local mínima com Pygame para renderizar o tabuleiro e permitir interação inicial do usuário com o jogo.

### Problema ou lacuna

O projeto precisa deixar de ser apenas uma lógica testável e passar a oferecer uma interação visual local, coerente com a decisão arquitetural de não ser uma aplicação web.

Sem uma interface mínima, o jogo ainda não cumpre a proposta de ser jogável por dois usuários no mesmo ambiente.

### Contexto

A arquitetura definiu Pygame como biblioteca gráfica inicial e estabeleceu que a interface não deve decidir regras de movimento.

Esta milestone deve criar a camada visual sem transformar Pygame em centro da lógica do jogo.

### Escopo núcleo

- Criar janela Pygame.
- Renderizar tabuleiro.
- Representar peças de forma compreensível.
- Capturar eventos de mouse.
- Converter cliques em coordenadas do tabuleiro.
- Comunicar intenções de movimento à camada de aplicação.
- Redesenhar o tabuleiro conforme estado exposto pela aplicação.
- Exibir feedback visual ou textual mínimo.

### Fora de escopo

- Criar refinamento visual avançado.
- Criar animações complexas.
- Criar assets definitivos obrigatórios.
- Implementar IA adversária.
- Implementar multiplayer online.
- Implementar persistência.
- Automatizar gameplay pelo n8n.
- Fazer testes automatizados profundos da interface gráfica.
- Criar integração runtime com n8n.

### Entregáveis esperados

- Módulos da camada `ui`.
- Aplicação Pygame mínima.
- Renderizador de tabuleiro.
- Tratador básico de entrada.
- Integração com a camada `app`.
- Atualização documental se houver decisão visual relevante.

### Dependências

- M4 concluída.
- Camada de aplicação capaz de fornecer estado renderizável.
- Pygame declarado na configuração do projeto.

### Componentes afetados

- UI.
- Application.
- Runtime.
- Documentation.
- Validation.

### Issues previstas

- Criar janela e loop principal do Pygame.
- Criar renderização inicial do tabuleiro.
- Criar renderização simples das peças.
- Criar conversão de clique para coordenada.
- Integrar UI com controlador de aplicação.
- Validar que UI não decide regras de movimento.

### Critérios de derivação de issues

- Separar renderização de entrada se a implementação ficar grande.
- Não misturar regras do xadrez com código de interface.
- Não exigir assets gráficos sofisticados para concluir a milestone.
- Criar issue separada para melhorias visuais opcionais.

### Definition of Done

- A janela do jogo abre localmente.
- O tabuleiro é exibido.
- As peças são representadas de forma compreensível.
- Cliques do usuário são capturados.
- A interface envia intenções para a camada de aplicação.
- A interface redesenha o estado após atualização.
- A interface não valida movimentos diretamente.
- O jogo continua sem dependência runtime do n8n.

### Evidência mínima

- Registro reduzido de execução local da interface.
- Captura ou descrição validada da tela inicial, se adotado pelo workflow.
- Revisão estrutural confirmando separação entre `ui`, `app` e `domain`.

### Riscos e lacunas

- Risco de a interface concentrar lógica de partida.
- Risco de excesso de esforço visual antes da jogabilidade.
- Risco de dificuldade de testar interface gráfica automaticamente.
- Risco de acoplamento direto entre UI e `python-chess`.

### Observações de continuidade

A interface mínima deve ser suficiente para permitir a próxima milestone: jogabilidade local mínima.

Melhorias visuais devem permanecer não bloqueantes, salvo se afetarem compreensão básica do jogo.

---

## M6 — Jogabilidade local mínima

### Objetivo

Integrar domínio, aplicação e interface para permitir que dois jogadores realizem uma partida simples localmente, com turnos, movimentos válidos, rejeição de movimentos inválidos e feedback básico.

### Problema ou lacuna

Mesmo com domínio, aplicação e interface existentes, o projeto só cumpre sua visão central quando esses componentes funcionam juntos em uma experiência jogável mínima.

A lacuna desta milestone é transformar componentes separados em um fluxo de jogo funcional.

### Contexto

A visão define que a conclusão macro depende de uma partida simples jogável localmente, com controle de turnos, rejeição de movimentos inválidos, capturas e tratamento básico de fim de partida conforme arquitetura.

Esta milestone integra as capacidades anteriores.

### Escopo núcleo

- Permitir partida local para dois jogadores no mesmo ambiente.
- Controlar alternância de turnos.
- Permitir seleção e movimentação por clique.
- Aplicar capturas válidas.
- Rejeitar movimentos inválidos.
- Exibir feedback mínimo para movimento inválido.
- Exibir estado básico da partida.
- Tratar xeque, xeque-mate ou encerramento conforme suporte exposto pelo domínio.
- Manter fluxo jogável sem persistência.

### Fora de escopo

- Multiplayer online.
- IA adversária.
- Ranking.
- Autenticação.
- Relógio de xadrez obrigatório.
- Salvamento e carregamento de partidas.
- Histórico visual avançado.
- Animações complexas.
- Automação do gameplay pelo n8n.
- Implementação manual completa das regras do xadrez.

### Entregáveis esperados

- Fluxo integrado de jogo local.
- Feedback básico de jogada inválida.
- Controle de turno funcional.
- Captura de peças funcional.
- Estado de fim de partida quando suportado.
- Ajustes de integração entre `ui`, `app` e `domain`.
- Testes adicionais onde aplicável.

### Dependências

- M5 concluída.
- Domínio e aplicação integráveis com a interface.
- Regras essenciais suportadas via `python-chess`.

### Componentes afetados

- Runtime.
- UI.
- Application.
- Domain.
- Tests.
- Validation.

### Issues previstas

- Integrar fluxo completo de movimento por clique.
- Implementar controle visual ou textual de turno.
- Implementar feedback para movimento inválido.
- Validar capturas e atualização de tabuleiro.
- Validar estados de xeque ou fim de partida quando disponíveis.
- Revisar aderência da integração às fronteiras arquiteturais.

### Critérios de derivação de issues

- Separar jogabilidade básica de refinamentos visuais.
- Não misturar persistência com jogabilidade mínima.
- Não adicionar IA adversária nesta milestone.
- Criar issue separada para tratamento de fim de partida se o escopo crescer.
- Não transformar validação manual em autorização automática de fechamento.

### Definition of Done

- O jogo permite dois jogadores locais.
- O tabuleiro inicia em posição válida.
- O jogador atual consegue mover uma peça válida.
- O turno alterna corretamente após movimento válido.
- Movimentos inválidos são rejeitados.
- Capturas válidas atualizam o tabuleiro.
- Feedback mínimo é exibido quando necessário.
- A aplicação permanece local e não web.
- O jogo não depende de n8n para funcionar.

### Evidência mínima

- Registro reduzido de execução de uma sequência simples de jogadas.
- Resultado resumido de testes relevantes.
- Validação visual ou descritiva de que o tabuleiro atualiza após jogada.
- Revisão estrutural confirmando que regras continuam fora da UI.

### Riscos e lacunas

- Risco de bugs de integração entre clique, coordenada e movimento.
- Risco de feedback insuficiente para o usuário entender erro.
- Risco de regras especiais não serem bem expostas na interface.
- Risco de escopo crescer para recursos opcionais antes do fechamento da jogabilidade mínima.

### Observações de continuidade

Após esta milestone, o projeto deve ter uma versão funcional mínima.

As milestones seguintes devem priorizar validação, qualidade e fechamento da versão inicial, não expansão de escopo.

---

## M7 — Testes, lint e validação arquitetural

### Objetivo

Consolidar testes automatizados, lint, formatação e validação de aderência arquitetural mínima para aumentar confiança na versão jogável inicial.

### Problema ou lacuna

Um jogo funcional sem validação mínima pode regredir facilmente e dificultar o uso do projeto como alvo confiável para workflows do `n8n-local-stack`.

A lacuna é garantir que domínio, aplicação e estrutura mantenham comportamento verificável e fronteiras coerentes.

### Contexto

A arquitetura definiu `pytest` para testes e Ruff para lint e formatação.

A visão também exige testes ou validações mínimas para regras centrais e documentação coerente para uso pelo pipeline externo.

### Escopo núcleo

- Criar ou ampliar testes de domínio.
- Criar ou ampliar testes da camada de aplicação.
- Validar movimentos básicos.
- Validar rejeição de movimentos inválidos.
- Validar alternância de turno.
- Validar encapsulamento de `python-chess`.
- Configurar ou consolidar Ruff.
- Verificar que a UI não concentra regras do jogo.
- Produzir evidência reduzida de validação.

### Fora de escopo

- Testar profundamente renderização Pygame.
- Criar suíte exaustiva de todas as regras especiais.
- Criar CI/CD obrigatório.
- Criar workflow n8n dentro do repositório.
- Publicar release.
- Criar cobertura total obrigatória.
- Alterar State operacional.
- Gerar issue formal.

### Entregáveis esperados

- Testes automatizados de domínio.
- Testes automatizados de aplicação.
- Configuração de Ruff.
- Critérios de validação documentados ou refletidos no README.
- Evidência reduzida de execução das validações.
- Ajustes de código necessários para passar nas validações.

### Dependências

- M6 concluída.
- Projeto com fluxo jogável mínimo.
- Estrutura de testes existente.

### Componentes afetados

- Tests.
- Validation.
- Tooling.
- Domain.
- Application.
- Architecture.
- Documentation.

### Issues previstas

- Criar testes de domínio para movimentos básicos.
- Criar testes da aplicação para fluxo de movimento.
- Configurar Ruff.
- Validar encapsulamento de `python-chess`.
- Revisar aderência arquitetural das dependências.
- Registrar evidência reduzida de validação.

### Critérios de derivação de issues

- Separar testes de domínio e aplicação.
- Separar configuração de tooling da correção de falhas.
- Não transformar evidência de validação em State operacional.
- Não exigir teste gráfico completo para concluir a milestone.
- Criar issue específica para cobertura adicional apenas se houver lacuna relevante.

### Definition of Done

- Testes essenciais de domínio existem.
- Testes essenciais de aplicação existem.
- Validação de movimento válido está coberta.
- Rejeição de movimento inválido está coberta.
- Alternância de turno está coberta.
- Ruff está configurado.
- A arquitetura continua respeitando `ui → app → domain → python-chess`.
- Evidência mínima de validação foi registrada de forma reduzida e sem conteúdo sensível.

### Evidência mínima

- Resultado resumido dos testes.
- Resultado resumido da validação de lint/formatação, se executada.
- Revisão reduzida de dependências entre camadas.
- Registro sanitizado de validação, se usado pelo pipeline externo.

### Riscos e lacunas

- Risco de baixa cobertura para regras especiais.
- Risco de testes frágeis por dependerem demais de detalhes internos.
- Risco de transformar validações externas em fonte de verdade do projeto.
- Risco de excesso de tooling para um projeto pequeno.

### Observações de continuidade

Esta milestone aumenta a confiança na versão inicial e prepara o fechamento documental e operacional da primeira versão.

Validações futuras podem ser orquestradas pelo `n8n-local-stack`, mas os resultados não devem substituir documentação, issues ou State operacional.

---

## M8 — Execução local documentada e fechamento da versão inicial

### Objetivo

Consolidar a versão inicial do projeto como aplicação local executável, documentada e coerente com visão, arquitetura e milestones.

### Problema ou lacuna

Após a implementação e validação da jogabilidade mínima, o projeto precisa de fechamento claro para que humanos, IA e workflows externos entendam o que foi entregue, o que ficou fora do escopo e quais capacidades futuras podem ser derivadas.

Sem esse fechamento, o projeto pode continuar expandindo sem critério ou confundir recursos opcionais com pendências obrigatórias.

### Contexto

A visão define uma Definition of Done macro para a versão central do projeto.

A arquitetura define critérios de aderência, incluindo execução local, separação entre interface e regras, encapsulamento de `python-chess`, testes mínimos e independência em relação ao n8n.

Esta milestone consolida o fechamento da versão inicial sem criar uma integração runtime com n8n.

### Escopo núcleo

- Revisar README para refletir estado real da versão inicial.
- Documentar forma de uso em linguagem descritiva, sem transformar este documento em manual de comandos.
- Registrar capacidades entregues.
- Registrar limitações conhecidas.
- Registrar escopo não implementado.
- Confirmar aderência à visão e arquitetura.
- Confirmar que o jogo é executável localmente.
- Confirmar que o n8n permanece externo ao runtime.

### Fora de escopo

- Publicar release obrigatória.
- Criar instalador.
- Criar pacote distribuível complexo.
- Criar CI/CD obrigatório.
- Criar integração runtime com n8n.
- Automatizar gameplay.
- Adicionar recursos opcionais como histórico, desfazer, salvar/carregar ou IA adversária.
- Gerar issues formais automaticamente.
- Alterar State operacional.

### Entregáveis esperados

- README revisado.
- Documentação de capacidades entregues.
- Registro de limitações conhecidas.
- Evidência reduzida de execução local.
- Evidência reduzida de validação.
- Revisão de aderência a `vision.md`, `architecture.md` e `milestones.md`.

### Dependências

- M7 concluída.
- Versão jogável mínima validada.
- Documentação fundacional existente.

### Componentes afetados

- Documentation.
- Runtime.
- Validation.
- Review Pipeline.
- Issue Derivation.
- Architecture.

### Issues previstas

- Atualizar README com estado real da versão inicial.
- Registrar limitações e fora de escopo da versão inicial.
- Validar aderência final à visão.
- Validar aderência final à arquitetura.
- Registrar evidência mínima de execução e validação.
- Preparar continuidade para possíveis melhorias futuras.

### Critérios de derivação de issues

- Separar documentação de fechamento de correções funcionais.
- Não adicionar novos recursos durante fechamento.
- Não criar issue formal diretamente a partir da milestone.
- Criar issue separada para cada lacuna futura relevante.
- Marcar recursos opcionais como futuras possibilidades, não pendências obrigatórias.

### Definition of Done

- O README descreve corretamente o estado do projeto.
- A versão inicial é executável localmente.
- A jogabilidade mínima está disponível.
- Testes e validações essenciais foram executados ou registrados de forma reduzida.
- A aderência à visão foi revisada.
- A aderência à arquitetura foi revisada.
- O n8n permanece fora do runtime.
- Limitações conhecidas estão registradas.
- Recursos opcionais não foram tratados como obrigatórios.

### Evidência mínima

- Registro reduzido de execução local.
- Resultado resumido dos testes e validações.
- Revisão textual de aderência à visão.
- Revisão textual de aderência à arquitetura.
- Registro de limitações conhecidas sem logs brutos ou payloads sensíveis.

### Riscos e lacunas

- Risco de transformar fechamento em nova implementação.
- Risco de incluir recursos opcionais no escopo obrigatório.
- Risco de documentação divergir do comportamento real.
- Risco de confundir evidência de workflow com fonte de verdade.
- Risco de fechar versão sem explicitar limitações.

### Observações de continuidade

Após esta milestone, o projeto pode evoluir para melhorias opcionais, como refinamento visual, histórico de movimentos, desfazer jogada, salvamento local ou IA simples.

Essas melhorias devem ser planejadas em nova rodada de milestones ou issues, preservando a separação entre visão, arquitetura, State operacional, issues e Control.

---

## Agrupamentos rejeitados

### Milestone final de preparação para n8n

Rejeitada.

O projeto já deve ser conduzido pelo pipeline do `n8n-local-stack` desde as primeiras milestones de implementação. Portanto, a relação com n8n é transversal ao processo e não uma capacidade final do jogo.

### Milestone de integração runtime com n8n

Rejeitada.

O `n8n-local-stack` não faz parte do runtime do jogo. O jogo deve ser executável localmente sem depender do n8n.

### Milestone de gameplay automatizado pelo n8n

Rejeitada.

Automação de gameplay não faz parte da visão inicial. O n8n pode apoiar implementação, validação e revisão, mas não deve controlar partidas.

### Milestone de engine própria de xadrez

Rejeitada para a versão inicial.

A arquitetura define uso de `python-chess` como motor inicial de regras, encapsulado no domínio.

### Milestone de aplicação web

Rejeitada.

A visão e a arquitetura definem aplicação local, não web.

---

## Observações finais

Este documento deve ser usado como base para derivação futura de drafts de issues.

A derivação deve respeitar:

- escopo núcleo de cada milestone;
- fora de escopo declarado;
- dependências;
- critérios de derivação;
- Definition of Done;
- evidência mínima;
- fronteiras arquiteturais;
- separação entre planejamento, State operacional e Control.

Nenhuma informação deste documento deve ser interpretada como autorização automática de execução.
