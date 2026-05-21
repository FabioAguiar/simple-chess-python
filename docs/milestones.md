# Milestones

## Finalidade

Este documento registra o planejamento de milestones do projeto `simple-chess-python`.

O objetivo é transformar a visão renovada e a arquitetura inicial do projeto em um conjunto de capacidades planejadas, proporcionais, verificáveis e deriváveis em trabalhos futuros.

Este documento orienta continuidade, validação, geração posterior de drafts de issues, formalização futura de issues e handoffs de implementação.

Este documento não executa implementação, não publica issues, não gera drafts de issues, não define milestone vigente, não substitui State operacional e não cria mapa de implementação.

---

## Regras de Leitura

- Milestones representam capacidades planejadas, não microtarefas.
- Milestones não são issues formais.
- Issues previstas são apenas candidatas conceituais para futura derivação.
- A ordem das milestones indica sequência lógica planejada, mas não deve ser usada isoladamente como cursor operacional.
- A milestone vigente, quando existir, deve ser controlada por artefato próprio de State operacional, como `docs/project-status/milestone-state.json`.
- Implementação depende de etapa posterior autorizada, como issue formal e handoff de implementação.
- Nenhuma milestone autoriza patch, commit, pull request, publicação ou execução automática.
- Documentação acumulativa de implementação depende de decisão arquitetural e autorização posterior.
- Workflows externos podem apoiar implementação e validação, mas não fazem parte do runtime do jogo.

---

## Relação com docs/vision.md

O `docs/vision.md` define a direção macro do projeto: criar um jogo simples de xadrez em Python, local, compreensível, com modo PvP local e modo PvC local contra uma IA simples.

A visão orienta este planejamento ao estabelecer que o projeto deve:

- permanecer pequeno e controlado;
- permitir execução local;
- oferecer PvP local;
- oferecer PvC local com IA simples;
- evitar engine competitiva;
- evitar aplicação web e multiplayer online;
- manter automações externas fora do runtime;
- preservar documentação suficiente para continuidade.

Este documento não transforma automaticamente todas as capacidades desejadas da visão em obrigações imediatas. Recursos opcionais, como salvamento, desfazer jogada, refinamento visual avançado e IA mais inteligente, permanecem fora do núcleo inicial salvo decisão posterior.

---

## Relação com docs/architecture.md

O `docs/architecture.md` define as fronteiras técnicas e responsabilidades que orientam este planejamento.

As milestones devem respeitar as seguintes decisões arquiteturais:

- aplicação local, não web;
- linguagem Python;
- interface local com Pygame;
- arquitetura modular simples em camadas leves;
- separação entre `ui`, `app`, `domain` e `ai`;
- uso de biblioteca de xadrez encapsulada no domínio;
- IA aleatória como estratégia inicial;
- humano joga de brancas no PvC inicial;
- IA não altera diretamente o estado do jogo;
- sem desfazer jogada na versão inicial;
- sem salvar/carregar partida na versão inicial;
- workflows externos fora do runtime;
- estratégia inicial de documentação da implementação: `milestones-only`.

Este documento não redefine arquitetura e não cria componentes fora das fronteiras já estabelecidas.

---

## Relação com State Operacional

`docs/milestones.md` é planejamento.

Ele não deve ser usado como State operacional do projeto e não define qual milestone está ativa.

Se o projeto precisar controlar milestone vigente, esse controle deve ocorrer em artefato separado, como:

```text
docs/project-status/milestone-state.json
```

A separação esperada é:

```text
docs/vision.md = direção macro
docs/architecture.md = fronteiras e decisões estruturais
docs/milestones.md = planejamento de capacidades
docs/project-status/milestone-state.json = State operacional, se adotado
issues formais = unidades de trabalho autorizadas posteriormente
implementation_handoff = orientação operacional posterior
runtime = execução local do jogo
```

Nenhuma milestone deste documento altera State operacional.

---

## Relação com Documentação da Implementação

Estratégia aplicável: `milestones-only`.

A arquitetura define que, no estágio inicial, o projeto não exige Implementation Map dedicado. O próprio `docs/milestones.md`, junto com `docs/vision.md`, `docs/architecture.md`, issues futuras e handoffs autorizados, deve ser suficiente para orientar continuidade.

As milestones devem avaliar documentação da implementação de forma proporcional:

- criar documentação acumulativa apenas se houver necessidade real de navegação entre módulos;
- não criar Implementation Map por padrão;
- não tratar mapa de implementação como changelog;
- não tratar mapa de implementação como State operacional;
- não substituir leitura dos arquivos reais por documentação resumida;
- reavaliar a estratégia se o custo de contexto crescer com evolução simultânea de domínio, aplicação, IA e interface.

A ausência de Implementation Map não é falha enquanto a estratégia vigente for `milestones-only`.

---

## Visão Geral das Milestones

| Milestone | Foco | Resultado esperado | Derivável? |
|---|---|---|---|
| M1 | Fundação documental renovada | Visão, arquitetura e milestones alinhados à versão com PvP e PvC | Sim |
| M2 | Estrutura base Python | Projeto organizado em estrutura modular inicial | Sim |
| M3 | Domínio e regras do xadrez | Regras e estado do jogo encapsulados no domínio com biblioteca de xadrez | Sim |
| M4 | Aplicação e sessão de partida | Fluxo central de partida, modos de jogo e turnos coordenados pela aplicação | Sim |
| M5 | Interface Pygame inicial | Tabuleiro local renderizado e interação básica por mouse | Sim |
| M6 | Modo PvP local | Dois jogadores humanos conseguem jogar localmente | Sim |
| M7 | IA aleatória | Computador escolhe movimentos legais por estratégia aleatória isolada | Sim |
| M8 | Modo PvC local | Jogador humano joga de brancas contra IA aleatória local | Sim |
| M9 | Validação e aderência arquitetural | Testes e validações proporcionais cobrem domínio, aplicação, IA e fronteiras | Sim |
| M10 | Fechamento da versão inicial | Versão inicial executável, documentada e coerente com visão e arquitetura | Com ressalvas |

---

## M1 — Fundação documental renovada

### Objetivo

Consolidar a fundação documental do projeto com a visão renovada de um jogo de xadrez local em Python com PvP local e PvC local contra IA simples.

### Problema ou Lacuna

A visão anterior do projeto estava orientada a um jogo simples de xadrez, mas não fechava o escopo de modo de jogo, IA, PvC e limites de funcionalidades opcionais. Sem essa renovação documental, futuras implementações poderiam seguir interpretações divergentes.

### Contexto

O projeto passou a aceitar uma complexidade mínima adicional: manter PvP local e adicionar PvC local com IA aleatória. Essa mudança exige realinhamento da visão, arquitetura e milestones antes da implementação técnica.

### Escopo Núcleo

- Consolidar `docs/vision.md` renovado.
- Consolidar `docs/architecture.md` renovado.
- Consolidar `docs/milestones.md` renovado.
- Registrar PvP local e PvC local como núcleo da visão inicial.
- Registrar IA aleatória como estratégia inicial.
- Registrar limites: sem engine competitiva, sem web, sem multiplayer online, sem salvar/carregar e sem desfazer jogada na versão inicial.
- Preservar o papel de workflows externos como apoio ao processo, não como runtime do jogo.

### Fora de Escopo

- Implementar código.
- Criar estrutura Python.
- Criar issues formais.
- Gerar drafts de issues.
- Alterar State operacional.
- Criar Implementation Map.
- Criar workflow externo.
- Publicar release.

### Entregáveis Esperados

- `docs/vision.md` renovado.
- `docs/architecture.md` renovado.
- `docs/milestones.md` renovado.
- Coerência explícita entre visão, arquitetura e planejamento.

### Documentação da Implementação

- Estratégia aplicável: `milestones-only`.
- Avaliação esperada: confirmar que a documentação fundacional é suficiente para orientar próximas etapas.
- Documentos candidatos: não se aplica neste estágio.
- Critério para criar: não criar documentação acumulativa nesta milestone.
- Critério para atualizar: atualizar apenas documentos fundacionais diretamente afetados pela renovação.
- Critério para não atualizar: não criar Implementation Map ou documentação de implementação antes de existir implementação.

### Dependências

Nenhuma dependência bloqueante identificada.

### Componentes ou Áreas Afetadas

- Documentation.
- Architecture.
- Milestone Planning.
- Issue Derivation.
- Review.

### Issues Previstas ou Critérios de Derivação

- Critério: separar revisão de visão, arquitetura e milestones se houver necessidade de controle fino.
- Possível tipo de issue: documentação fundacional.
- Observação: nenhuma issue formal é criada por este documento.

### Definition of Done

- A visão renovada define PvP local e PvC local.
- A arquitetura define fronteiras entre domínio, aplicação, IA e interface.
- As milestones refletem a nova visão e a nova arquitetura.
- A estratégia `milestones-only` está refletida.
- O runtime do jogo permanece independente de workflows externos.
- Nenhum State operacional é alterado por este documento.

### Evidência Mínima

- Presença dos documentos fundacionais renovados.
- Revisão textual de coerência entre visão, arquitetura e milestones.
- Ausência de conteúdo sensível ou comandos operacionais nos documentos.

### Riscos e Lacunas

- Risco de transformar documentação fundacional em plano de implementação.
- Risco de iniciar implementação antes de fechar fronteiras de IA e PvC.
- Risco de documentar recursos opcionais como obrigatórios.

### Critérios de Derivabilidade

A milestone estará pronta para derivação quando visão, arquitetura e milestones estiverem coerentes, versionáveis e sem conflito sobre PvP, PvC, IA inicial e fora de escopo.

### Notas de Continuidade

Após esta milestone, a próxima capacidade natural é a criação da estrutura técnica base do projeto Python.

---

## M2 — Estrutura base Python e organização modular

### Objetivo

Criar a estrutura técnica inicial do projeto Python, organizada para receber domínio, aplicação, IA, interface, testes e documentação sem misturar responsabilidades.

### Problema ou Lacuna

O projeto precisa sair da fundação documental e passar a ter uma base técnica organizada. Sem essa estrutura, implementações futuras podem criar acoplamento prematuro ou dispersar responsabilidades.

### Contexto

A arquitetura define um modelo modular simples em camadas leves. Esta milestone materializa a organização inicial sem implementar regras completas, interface jogável ou IA funcional.

### Escopo Núcleo

- Criar estrutura base do pacote Python.
- Separar áreas previstas para domínio, aplicação, IA e interface.
- Preparar estrutura inicial de testes.
- Preparar configuração mínima do projeto.
- Garantir que a organização reflita as fronteiras arquiteturais.

### Fora de Escopo

- Implementar regras do xadrez.
- Implementar interface gráfica funcional.
- Implementar IA aleatória.
- Implementar PvP ou PvC.
- Criar persistência.
- Criar workflow externo.
- Criar Implementation Map.
- Alterar State operacional.

### Entregáveis Esperados

- Estrutura inicial do projeto Python.
- Configuração mínima do projeto.
- Estrutura inicial de testes.
- Organização coerente com as áreas `domain`, `app`, `ai` e `ui`.

### Documentação da Implementação

- Estratégia aplicável: `milestones-only`.
- Avaliação esperada: confirmar se a estrutura é simples o suficiente para ser entendida via milestones e arquitetura.
- Documentos candidatos: não se aplica neste estágio.
- Critério para criar: não criar documentação acumulativa apenas pela criação da estrutura base.
- Critério para atualizar: atualizar documentação fundacional apenas se a estrutura real divergir da arquitetura.
- Critério para não atualizar: não registrar cada arquivo criado como documentação acumulativa.

### Dependências

- M1 concluída ou suficientemente validada.
- Arquitetura inicial disponível.

### Componentes ou Áreas Afetadas

- Project Structure.
- Tooling.
- Tests.
- Documentation.
- Validation.

### Issues Previstas ou Critérios de Derivação

- Critério: separar estrutura de projeto de configuração se a validação exigir.
- Possível tipo de issue: fundação técnica.
- Observação: não misturar criação de estrutura com implementação de domínio ou interface.

### Definition of Done

- A estrutura base do projeto existe.
- As áreas principais previstas estão representadas.
- A configuração inicial do projeto existe.
- A estrutura de testes está preparada.
- A organização não mistura runtime do jogo com tooling externo.
- A estrutura respeita a separação entre domínio, aplicação, IA e interface.

### Evidência Mínima

- Listagem reduzida da estrutura criada.
- Revisão de aderência à arquitetura.
- Validação de que não há artefatos sensíveis ou locais indevidamente versionados.

### Riscos e Lacunas

- Risco de criar arquivos demais antes da necessidade.
- Risco de adotar estrutura pesada para um projeto pequeno.
- Risco de misturar IA com domínio ou interface.

### Critérios de Derivabilidade

A milestone estará pronta para derivação quando a arquitetura indicar claramente as áreas necessárias e a estrutura puder ser criada sem decidir detalhes de implementação funcional.

### Notas de Continuidade

A estrutura criada deve permitir que o domínio seja implementado antes da interface e antes do PvC completo.

---

## M3 — Domínio e regras do xadrez

### Objetivo

Criar o domínio do jogo, responsável por representar o estado central da partida, validar movimentos e encapsular a biblioteca de xadrez.

### Problema ou Lacuna

O jogo precisa de uma base confiável para regras do xadrez. Implementar regras manualmente aumentaria risco e desviaria o foco do projeto. Usar a biblioteca diretamente em várias camadas também criaria acoplamento indevido.

### Contexto

A arquitetura define que a biblioteca de xadrez deve ficar encapsulada no domínio. O domínio deve proteger regras e estado central, sem depender de interface ou IA.

### Escopo Núcleo

- Representar estado inicial da partida.
- Consultar turno atual.
- Consultar movimentos legais.
- Validar movimentos.
- Aplicar movimentos válidos.
- Rejeitar movimentos inválidos.
- Expor estado básico da partida.
- Encapsular a biblioteca de xadrez.

### Fora de Escopo

- Criar interface Pygame.
- Criar IA aleatória.
- Criar modos PvP/PvC completos.
- Implementar regras manualmente sem necessidade.
- Implementar engine competitiva.
- Implementar persistência.
- Criar análise avançada de posição.

### Entregáveis Esperados

- Camada de domínio funcional.
- Encapsulamento da biblioteca de xadrez.
- Consultas básicas de estado e movimentos.
- Testes iniciais de domínio.

### Documentação da Implementação

- Estratégia aplicável: `milestones-only`.
- Avaliação esperada: verificar se as responsabilidades do domínio continuam compreensíveis pela arquitetura e pelos testes.
- Documentos candidatos: não se aplica neste estágio.
- Critério para criar: considerar documentação adicional apenas se o domínio ganhar abstrações difíceis de entender por leitura direta.
- Critério para atualizar: atualizar arquitetura se o encapsulamento da biblioteca mudar.
- Critério para não atualizar: não criar mapa apenas para registrar funções internas.

### Dependências

- M2 concluída.
- Biblioteca de xadrez definida pela arquitetura.

### Componentes ou Áreas Afetadas

- Domain.
- Runtime.
- Tests.
- Validation.
- Architecture.

### Issues Previstas ou Critérios de Derivação

- Critério: separar encapsulamento da biblioteca de regras dos testes, se necessário.
- Possível tipo de issue: domínio/regras.
- Observação: a biblioteca não deve vazar para `ui` ou `ai`.

### Definition of Done

- O domínio inicia uma partida válida.
- O domínio expõe movimentos legais.
- O domínio valida movimentos.
- O domínio aplica movimentos válidos.
- O domínio rejeita movimentos inválidos.
- A biblioteca de xadrez permanece encapsulada.
- Testes mínimos de domínio existem.

### Evidência Mínima

- Resultado resumido de testes de domínio.
- Revisão de dependências confirmando ausência de Pygame no domínio.
- Revisão confirmando que a biblioteca de xadrez não foi espalhada por outras áreas.

### Riscos e Lacunas

- Risco de vazar objetos internos da biblioteca para outras camadas.
- Risco de duplicar regras do xadrez fora do domínio.
- Risco de criar abstrações excessivas sobre a biblioteca.

### Critérios de Derivabilidade

A milestone estará pronta para derivação quando as operações mínimas do domínio estiverem claras: iniciar partida, consultar movimentos, validar e aplicar movimento.

### Notas de Continuidade

O domínio deve ser estável o suficiente para ser usado pela aplicação e pela IA sem expor detalhes internos da biblioteca.

---

## M4 — Aplicação, sessão de partida e modos de jogo

### Objetivo

Criar a camada de aplicação que coordena sessão de partida, modo de jogo, turno, jogadores e comunicação entre interface, domínio e IA.

### Problema ou Lacuna

O projeto precisa de uma camada que controle o fluxo da partida sem colocar lógica de regras na interface ou lógica de sessão no domínio.

### Contexto

A arquitetura estabelece que a aplicação coordena o fluxo, enquanto o domínio protege regras e a IA apenas escolhe movimentos legais. Esta milestone cria a base de orquestração antes da jogabilidade completa.

### Escopo Núcleo

- Representar sessão de partida.
- Representar modo de jogo PvP ou PvC.
- Representar jogador humano e jogador computador.
- Controlar turno atual.
- Receber intenção de movimento.
- Solicitar validação ao domínio.
- Aplicar movimento por meio do domínio.
- Preparar ponto de chamada para IA quando aplicável.
- Expor estado necessário para a interface.

### Fora de Escopo

- Implementar IA aleatória completa.
- Implementar interface gráfica completa.
- Implementar PvC final.
- Implementar salvar/carregar.
- Implementar desfazer jogada.
- Criar engine competitiva.
- Criar gameplay automatizado externo.

### Entregáveis Esperados

- Camada de aplicação.
- Representação de sessão de partida.
- Representação de modos de jogo.
- Fluxo básico de intenção de movimento.
- Testes da aplicação sem depender da interface.

### Documentação da Implementação

- Estratégia aplicável: `milestones-only`.
- Avaliação esperada: confirmar se os conceitos de sessão, modo e jogador estão claros o suficiente.
- Documentos candidatos: não se aplica neste estágio.
- Critério para criar: considerar documentação adicional apenas se a aplicação concentrar fluxos difíceis de reconstruir pelos testes.
- Critério para atualizar: atualizar arquitetura se a separação entre aplicação e domínio mudar.
- Critério para não atualizar: não criar mapa apenas para listar classes ou métodos.

### Dependências

- M3 concluída.
- Domínio capaz de validar e aplicar movimentos.

### Componentes ou Áreas Afetadas

- Application.
- Domain.
- Runtime.
- Tests.
- Validation.

### Issues Previstas ou Critérios de Derivação

- Critério: separar sessão, modos de jogo e fluxo de movimento se houver complexidade suficiente.
- Possível tipo de issue: camada de aplicação.
- Observação: a aplicação não deve implementar regras do xadrez manualmente.

### Definition of Done

- A aplicação cria uma sessão de partida.
- A aplicação registra modo PvP ou PvC.
- A aplicação controla turno.
- A aplicação recebe intenção de movimento.
- A aplicação usa o domínio para validar e aplicar movimento.
- A aplicação expõe estado para futura interface.
- Testes de aplicação existem sem depender de Pygame.

### Evidência Mínima

- Resultado resumido de testes da aplicação.
- Revisão estrutural confirmando ausência de Pygame na aplicação.
- Revisão confirmando que regras permanecem no domínio.

### Riscos e Lacunas

- Risco de a aplicação virar uma camada grande demais.
- Risco de duplicar validação de regras na aplicação.
- Risco de antecipar detalhes de UI.
- Risco de acoplamento prematuro com a IA antes da estratégia estar pronta.

### Critérios de Derivabilidade

A milestone estará pronta para derivação quando sessão, modos de jogo, fluxo de movimento e dependências com domínio estiverem claramente delimitados.

### Notas de Continuidade

Esta milestone prepara tanto o modo PvP quanto a futura integração PvC.

---

## M5 — Interface local inicial com Pygame

### Objetivo

Criar uma interface local inicial com Pygame para renderizar o tabuleiro, capturar interação por mouse e comunicar intenções à aplicação.

### Problema ou Lacuna

O projeto precisa de uma camada visual local para tornar o jogo interativo sem transformar a interface em responsável por regras ou estado central da partida.

### Contexto

A arquitetura define Pygame como interface local e interação principal por mouse. A interface deve ser simples, compreensível e desacoplada das regras.

### Escopo Núcleo

- Abrir janela local.
- Renderizar tabuleiro.
- Representar peças de forma compreensível.
- Capturar cliques do usuário.
- Converter clique em intenção de seleção ou movimento.
- Enviar intenções para a aplicação.
- Exibir feedback básico.
- Permitir seleção inicial de modo de jogo de forma simples, se necessário para integração futura.

### Fora de Escopo

- Refinamento visual avançado.
- Animações complexas.
- Assets definitivos obrigatórios.
- Validação de regras na interface.
- IA.
- Salvar/carregar.
- Desfazer jogada.
- Testes gráficos profundos.

### Entregáveis Esperados

- Interface Pygame inicial.
- Renderização básica do tabuleiro.
- Representação simples de peças.
- Entrada por mouse conectada à aplicação.
- Feedback básico ao usuário.

### Documentação da Implementação

- Estratégia aplicável: `milestones-only`.
- Avaliação esperada: verificar se decisões visuais mínimas precisam ser registradas na arquitetura ou README.
- Documentos candidatos: não se aplica neste estágio.
- Critério para criar: criar documentação adicional apenas se a interface exigir convenções visuais não óbvias.
- Critério para atualizar: atualizar documentação de uso quando a interface se tornar executável.
- Critério para não atualizar: não criar mapa para detalhes gráficos simples.

### Dependências

- M4 concluída ou suficientemente validada.
- Decisão de interface com Pygame consolidada.

### Componentes ou Áreas Afetadas

- UI.
- Application.
- Runtime.
- Documentation.
- Validation.

### Issues Previstas ou Critérios de Derivação

- Critério: separar renderização, entrada e feedback se o escopo ficar grande.
- Possível tipo de issue: interface local.
- Observação: a UI não deve validar regras nem acessar diretamente a biblioteca de xadrez.

### Definition of Done

- A janela local abre.
- O tabuleiro é renderizado.
- As peças são compreensíveis.
- Cliques são capturados.
- A interface envia intenções à aplicação.
- A interface não decide legalidade de movimento.
- O jogo permanece local e não web.

### Evidência Mínima

- Registro reduzido de execução local da interface.
- Revisão estrutural confirmando separação entre UI e regras.
- Descrição ou captura validada da tela inicial, se adotado pelo fluxo de validação.

### Riscos e Lacunas

- Risco de a interface concentrar lógica de jogo.
- Risco de excesso de tempo em refinamento visual prematuro.
- Risco de indefinição sobre representação das peças.
- Risco de dificuldade de teste automatizado da interface.

### Critérios de Derivabilidade

A milestone estará pronta para derivação quando a arquitetura definir interface local, responsabilidade da UI e limite contra validação de regras na interface.

### Notas de Continuidade

A interface inicial deve ser suficiente para permitir a integração do modo PvP local.

---

## M6 — Modo PvP local jogável

### Objetivo

Integrar domínio, aplicação e interface para permitir que dois jogadores humanos joguem uma partida local básica.

### Problema ou Lacuna

O projeto precisa demonstrar a jogabilidade humana local antes de adicionar comportamento de computador. Sem PvP funcional, o PvC ficaria dependente de uma base de partida ainda instável.

### Contexto

O PvP local é uma capacidade central da visão e serve como base natural para validar tabuleiro, movimentos, turnos, capturas e feedback.

### Escopo Núcleo

- Permitir que dois jogadores humanos joguem localmente.
- Controlar alternância de turnos.
- Permitir seleção e movimentação por mouse.
- Aplicar movimentos válidos.
- Rejeitar movimentos inválidos.
- Aplicar capturas.
- Exibir turno atual e feedback básico.
- Exibir estados básicos de fim de partida quando disponíveis.

### Fora de Escopo

- IA.
- PvC.
- Multiplayer online.
- Salvar/carregar.
- Desfazer jogada.
- Relógio de xadrez obrigatório.
- Refinamento visual avançado.
- Engine competitiva.

### Entregáveis Esperados

- Fluxo PvP local funcional.
- Integração entre UI, aplicação e domínio.
- Feedback básico de movimento inválido.
- Controle de turno visível ou consultável.
- Testes ou validações proporcionais do fluxo.

### Documentação da Implementação

- Estratégia aplicável: `milestones-only`.
- Avaliação esperada: registrar apenas limitações relevantes do PvP na documentação de uso ou fechamento.
- Documentos candidatos: não se aplica neste estágio.
- Critério para criar: não criar documentação acumulativa para fluxo PvP se ele for claro por arquitetura, testes e UI.
- Critério para atualizar: atualizar README futuramente quando houver versão executável.
- Critério para não atualizar: não registrar cada ajuste de jogabilidade como documentação separada.

### Dependências

- M5 concluída.
- Domínio e aplicação funcionais.

### Componentes ou Áreas Afetadas

- UI.
- Application.
- Domain.
- Runtime.
- Tests.
- Validation.

### Issues Previstas ou Critérios de Derivação

- Critério: separar integração PvP de refinamento visual.
- Possível tipo de issue: jogabilidade PvP.
- Observação: correções de regras devem permanecer no domínio, não na UI.

### Definition of Done

- Dois jogadores humanos conseguem jogar localmente.
- O tabuleiro inicia em posição válida.
- Movimentos legais são aplicados.
- Movimentos ilegais são rejeitados.
- Turnos alternam corretamente.
- Capturas são refletidas no tabuleiro.
- Feedback básico é exibido.
- A UI não valida regras diretamente.

### Evidência Mínima

- Registro reduzido de uma sequência de jogadas PvP.
- Resultado resumido de testes relevantes.
- Revisão de aderência às fronteiras UI, app e domain.

### Riscos e Lacunas

- Risco de bugs na conversão de clique para casa.
- Risco de feedback insuficiente para o usuário.
- Risco de misturar regra de movimento com renderização.
- Risco de antecipar PvC antes do PvP estar estável.

### Critérios de Derivabilidade

A milestone estará pronta para derivação quando o domínio, a aplicação e a UI já tiverem responsabilidades claras e puderem ser integrados em um fluxo humano local.

### Notas de Continuidade

O PvP local deve servir como base para a introdução da IA e posterior modo PvC.

---

## M7 — IA aleatória isolada

### Objetivo

Implementar a IA aleatória como módulo isolado capaz de escolher um movimento legal sem alterar diretamente o estado da partida.

### Problema ou Lacuna

O modo PvC exige que o computador escolha jogadas. Sem separar a IA, há risco de misturar comportamento do computador com regras, interface ou controle da sessão.

### Contexto

A arquitetura define a IA inicial como aleatória, limitada e substituível futuramente. A IA deve apenas selecionar um movimento legal e retornar essa escolha para a aplicação.

### Escopo Núcleo

- Criar módulo de IA.
- Implementar estratégia aleatória.
- Receber ou consultar movimentos legais disponíveis.
- Escolher um movimento legal.
- Retornar a escolha para a aplicação.
- Garantir que a IA não altera o estado do jogo diretamente.
- Criar testes para validar que a IA retorna apenas movimentos legais.

### Fora de Escopo

- IA material.
- Minimax.
- Stockfish.
- Engine competitiva.
- Avaliação avançada de posição.
- Aprendizado de máquina.
- Ajuste de dificuldade.
- Interface visual da IA.
- PvC completo.

### Entregáveis Esperados

- Módulo de IA.
- Estratégia aleatória.
- Testes da IA.
- Integração mínima com aplicação apenas quando necessária para seleção de movimento.

### Documentação da Implementação

- Estratégia aplicável: `milestones-only`.
- Avaliação esperada: verificar se a separação da IA está clara o suficiente em arquitetura e testes.
- Documentos candidatos: não se aplica neste estágio.
- Critério para criar: considerar documentação adicional apenas se novas estratégias de IA forem adicionadas futuramente.
- Critério para atualizar: atualizar arquitetura se a IA deixar de ser aleatória ou ganhar estratégia substituível mais complexa.
- Critério para não atualizar: não criar mapa apenas para uma estratégia aleatória simples.

### Dependências

- M4 concluída.
- Domínio capaz de expor movimentos legais de forma segura.

### Componentes ou Áreas Afetadas

- AI.
- Application.
- Domain.
- Tests.
- Validation.

### Issues Previstas ou Critérios de Derivação

- Critério: separar criação da estratégia de IA dos ajustes de aplicação, se necessário.
- Possível tipo de issue: IA simples.
- Observação: a IA não deve conhecer Pygame nem manipular diretamente a biblioteca de xadrez se isso violar encapsulamento.

### Definition of Done

- A IA recebe acesso a movimentos legais.
- A IA escolhe um movimento legal aleatório.
- A IA retorna a escolha para a aplicação.
- A IA não altera estado da partida diretamente.
- Testes validam que movimentos escolhidos são legais.
- A IA não depende da interface.

### Evidência Mínima

- Resultado resumido de testes da IA.
- Revisão confirmando que a IA não altera estado diretamente.
- Revisão confirmando independência em relação à interface.

### Riscos e Lacunas

- Risco de a IA acessar detalhes internos demais do domínio.
- Risco de a IA aplicar movimento diretamente.
- Risco de a IA aleatória gerar experiência fraca, embora aceita pela arquitetura.
- Risco de antecipar estratégia mais inteligente sem necessidade.

### Critérios de Derivabilidade

A milestone estará pronta para derivação quando a arquitetura indicar claramente que a IA apenas escolhe movimentos legais e não controla o estado do jogo.

### Notas de Continuidade

A IA aleatória prepara a integração do modo PvC local.

---

## M8 — Modo PvC local

### Objetivo

Integrar o modo PvC local, permitindo que o jogador humano jogue de brancas contra a IA aleatória jogando de pretas.

### Problema ou Lacuna

O projeto precisa concretizar a segunda forma principal de jogo definida na visão. A IA isolada precisa ser coordenada pela aplicação dentro do fluxo real da partida.

### Contexto

A arquitetura define que o humano joga de brancas no PvC inicial. A aplicação deve chamar a IA no turno do computador e aplicar o movimento escolhido por meio do domínio.

### Escopo Núcleo

- Permitir seleção do modo PvC.
- Configurar humano como brancas.
- Configurar computador como pretas.
- Aplicar jogada humana.
- Detectar turno do computador.
- Solicitar movimento à IA aleatória.
- Aplicar movimento da IA por meio do domínio.
- Atualizar interface após resposta da IA.
- Preservar validação de regras no domínio.

### Fora de Escopo

- Escolha de cor pelo usuário.
- Níveis de dificuldade.
- IA material ou minimax.
- Engine competitiva.
- Desfazer ciclo humano + IA.
- Salvar/carregar partida.
- Automação de gameplay por workflow externo.
- Multiplayer online.

### Entregáveis Esperados

- Modo PvC funcional.
- Integração entre aplicação e IA.
- Fluxo humano branco contra IA preta.
- Feedback básico após movimento da IA.
- Testes ou validações proporcionais do modo PvC.

### Documentação da Implementação

- Estratégia aplicável: `milestones-only`.
- Avaliação esperada: registrar limitações da IA e do modo PvC em documentação de uso ou fechamento futuro.
- Documentos candidatos: não se aplica neste estágio.
- Critério para criar: considerar documentação adicional apenas se múltiplas estratégias de IA ou configurações forem adicionadas.
- Critério para atualizar: atualizar README futuramente quando o modo PvC estiver disponível ao usuário.
- Critério para não atualizar: não criar mapa apenas para a integração inicial PvC.

### Dependências

- M6 concluída ou suficientemente validada.
- M7 concluída.

### Componentes ou Áreas Afetadas

- Application.
- AI.
- Domain.
- UI.
- Runtime.
- Tests.
- Validation.

### Issues Previstas ou Critérios de Derivação

- Critério: separar seleção de modo, chamada da IA e feedback visual se necessário.
- Possível tipo de issue: integração PvC.
- Observação: a aplicação, não a IA, deve aplicar movimentos no domínio.

### Definition of Done

- O usuário consegue iniciar uma partida PvC.
- O humano joga de brancas.
- A IA joga de pretas.
- A jogada humana válida é aplicada.
- A aplicação chama a IA no turno do computador.
- A IA retorna movimento legal.
- A aplicação aplica o movimento da IA via domínio.
- A interface reflete o estado atualizado.
- O jogo permanece local e independente de workflows externos.

### Evidência Mínima

- Registro reduzido de uma sequência humano → IA.
- Resultado resumido de testes ou validações do fluxo PvC.
- Revisão confirmando que a IA não altera estado diretamente.
- Revisão confirmando que o humano joga de brancas no modo inicial.

### Riscos e Lacunas

- Risco de fluxo assíncrono ou visual confuso após jogada da IA.
- Risco de a aplicação chamar a IA em momento incorreto.
- Risco de falta de feedback claro para o usuário.
- Risco de acoplamento entre IA e UI.

### Critérios de Derivabilidade

A milestone estará pronta para derivação quando PvP, aplicação e IA aleatória estiverem suficientemente definidos para integração.

### Notas de Continuidade

Após esta milestone, o projeto terá as duas formas centrais de jogo previstas na visão.

---

## M9 — Testes, validação e aderência arquitetural

### Objetivo

Consolidar testes e validações proporcionais para domínio, aplicação, IA, modos de jogo e fronteiras arquiteturais.

### Problema ou Lacuna

Com PvP e PvC presentes, o projeto precisa de confiança mínima contra regressões e contra acoplamento indevido entre camadas.

### Contexto

A arquitetura exige separação entre UI, aplicação, domínio e IA, além de garantir que a IA só escolha movimentos legais e que workflows externos permaneçam fora do runtime.

### Escopo Núcleo

- Testar domínio e regras básicas.
- Testar aplicação e fluxo de turnos.
- Testar IA aleatória como seletora de movimentos legais.
- Validar fluxo PvP essencial.
- Validar fluxo PvC essencial.
- Validar fronteiras arquiteturais.
- Validar que a biblioteca de xadrez permanece encapsulada.
- Validar que a IA não altera estado diretamente.
- Validar lint e formatação, se adotados.

### Fora de Escopo

- Teste gráfico exaustivo de Pygame.
- Cobertura total obrigatória.
- Testes de engine competitiva.
- Testes de multiplayer online.
- CI/CD obrigatório.
- Workflow externo dentro do runtime.
- Implementation Map obrigatório.

### Entregáveis Esperados

- Testes de domínio.
- Testes de aplicação.
- Testes de IA.
- Validações mínimas de PvP e PvC.
- Validação de fronteiras arquiteturais.
- Evidência reduzida de execução das validações.

### Documentação da Implementação

- Estratégia aplicável: `milestones-only`.
- Avaliação esperada: verificar se os testes e validações bastam para orientar manutenção futura.
- Documentos candidatos: não se aplica neste estágio.
- Critério para criar: considerar documentação acumulativa se os testes revelarem dificuldade recorrente para entender responsabilidades entre módulos.
- Critério para atualizar: atualizar README ou documentação de validação se houver forma consolidada de verificar o projeto.
- Critério para não atualizar: não criar Implementation Map apenas por existir suíte de testes.

### Dependências

- M8 concluída ou suficientemente validada.
- Testes estruturais disponíveis desde milestones anteriores.

### Componentes ou Áreas Afetadas

- Tests.
- Validation.
- Domain.
- Application.
- AI.
- UI.
- Tooling.
- Architecture.

### Issues Previstas ou Critérios de Derivação

- Critério: separar testes de domínio, aplicação, IA e validação de fronteiras se o trabalho ficar grande.
- Possível tipo de issue: testes e validação.
- Observação: não transformar validação em autorização automática de execução ou publicação.

### Definition of Done

- Testes essenciais de domínio existem.
- Testes essenciais de aplicação existem.
- Testes da IA aleatória existem.
- Fluxos PvP e PvC possuem validação proporcional.
- Fronteiras arquiteturais são revisadas.
- A biblioteca de xadrez permanece encapsulada no domínio.
- A IA não altera estado diretamente.
- Evidência mínima de validação é registrada de forma reduzida.

### Evidência Mínima

- Resultado resumido dos testes.
- Resultado resumido de lint/formatação, se adotado.
- Revisão reduzida de fronteiras entre módulos.
- Registro sanitizado de validação, se usado por workflow externo.

### Riscos e Lacunas

- Risco de testes frágeis por dependerem de detalhes internos.
- Risco de baixa cobertura para regras especiais.
- Risco de validação insuficiente do fluxo PvC.
- Risco de confundir evidência de workflow com fonte de verdade.

### Critérios de Derivabilidade

A milestone estará pronta para derivação quando os principais fluxos e fronteiras já existirem e puderem ser testados sem inventar novo escopo funcional.

### Notas de Continuidade

Esta milestone prepara o fechamento da versão inicial e reduz risco de regressão em futuras melhorias.

---

## M10 — Fechamento da versão inicial

### Objetivo

Consolidar a versão inicial do projeto como jogo local executável, documentado, com PvP local, PvC local com IA aleatória e limites conhecidos registrados.

### Problema ou Lacuna

Após implementação e validação das capacidades centrais, o projeto precisa de fechamento claro para evitar expansão indefinida de escopo e para orientar futuras melhorias sem confundir opcionais com pendências obrigatórias.

### Contexto

A visão define uma versão simples, local e compreensível. A arquitetura define fronteiras e decisões iniciais. Esta milestone consolida o estado inicial entregue e registra limitações.

### Escopo Núcleo

- Revisar documentação de uso em alto nível.
- Registrar capacidades entregues.
- Registrar limitações conhecidas.
- Confirmar PvP local.
- Confirmar PvC local com IA aleatória.
- Confirmar humano como brancas no PvC inicial.
- Confirmar ausência de salvar/carregar.
- Confirmar ausência de desfazer jogada.
- Confirmar independência do runtime em relação a workflows externos.
- Confirmar aderência à visão e arquitetura.

### Fora de Escopo

- Publicar release obrigatória.
- Criar instalador.
- Criar pacote distribuível complexo.
- Adicionar novas funcionalidades.
- Implementar IA material.
- Implementar salvar/carregar.
- Implementar desfazer jogada.
- Criar CI/CD obrigatório.
- Criar Implementation Map sem nova decisão.
- Alterar State operacional.

### Entregáveis Esperados

- Documentação de uso revisada.
- Registro de capacidades entregues.
- Registro de limitações conhecidas.
- Evidência reduzida de execução local.
- Evidência reduzida de validação.
- Revisão de aderência à visão e arquitetura.

### Documentação da Implementação

- Estratégia aplicável: `milestones-only`.
- Avaliação esperada: reavaliar se a estratégia ainda é suficiente após a versão inicial.
- Documentos candidatos: possível documentação acumulativa futura apenas se houver custo real de contexto.
- Critério para criar: criar Implementation Map somente em rodada posterior se manutenção entre módulos se tornar difícil.
- Critério para atualizar: atualizar README e documentos fundacionais conforme comportamento real da versão inicial.
- Critério para não atualizar: não criar mapa como changelog ou checklist de fechamento.

### Dependências

- M9 concluída.
- Versão inicial validada de forma proporcional.

### Componentes ou Áreas Afetadas

- Documentation.
- Runtime.
- Validation.
- Review.
- Issue Derivation.
- Architecture.

### Issues Previstas ou Critérios de Derivação

- Critério: separar correções funcionais de documentação de fechamento.
- Possível tipo de issue: fechamento de versão inicial.
- Observação: recursos futuros devem ser tratados como nova rodada de planejamento, não como pendências automáticas.

### Definition of Done

- O jogo executa localmente.
- O modo PvP local está disponível.
- O modo PvC local está disponível.
- A IA aleatória escolhe movimentos legais.
- O humano joga de brancas no PvC inicial.
- Movimentos inválidos são rejeitados.
- Capturas e turnos funcionam de forma suficiente para a versão inicial.
- Testes e validações essenciais foram registrados.
- A documentação descreve corretamente o estado entregue.
- Limitações conhecidas estão registradas.
- Workflows externos permanecem fora do runtime.

### Evidência Mínima

- Registro reduzido de execução local.
- Resultado resumido de testes e validações.
- Revisão de aderência à visão.
- Revisão de aderência à arquitetura.
- Registro de limitações conhecidas sem logs brutos ou payloads sensíveis.

### Riscos e Lacunas

- Risco de transformar fechamento em nova implementação.
- Risco de incluir funcionalidades opcionais no escopo obrigatório.
- Risco de documentação divergir do comportamento real.
- Risco de fechar versão sem explicitar limitações da IA aleatória.
- Risco de adotar Implementation Map sem necessidade real.

### Critérios de Derivabilidade

A milestone estará pronta para derivação quando as capacidades centrais já estiverem implementadas e o trabalho restante for principalmente validação, documentação e fechamento proporcional.

### Notas de Continuidade

Após esta milestone, melhorias como IA material simples, escolha de cor, histórico visível, desfazer jogada, salvar/carregar ou refinamento visual devem ser planejadas como nova evolução, não como pendência automática da versão inicial.

---

## Agrupamentos Rejeitados

### Milestone de integração runtime com workflows externos

Rejeitada.

Workflows externos podem apoiar o processo, mas não pertencem ao runtime do jogo.

### Milestone de engine competitiva

Rejeitada para a versão inicial.

A IA inicial é aleatória e limitada.

### Milestone de salvar/carregar partida

Rejeitada para a versão inicial.

Persistência foi definida como fora do escopo inicial.

### Milestone de desfazer jogada

Rejeitada para a versão inicial.

Desfazer jogada pode ser reavaliado futuramente, especialmente por causa da complexidade adicional no modo PvC.

### Milestone de aplicação web

Rejeitada.

O projeto é local e não web.

### Milestone de Implementation Map

Rejeitada neste estágio.

A estratégia vigente é `milestones-only`. A criação de mapa de implementação deve ser reavaliada apenas se o custo de contexto crescer.

---

## Observações Finais

Este documento orienta a futura geração de drafts de issues e handoffs de implementação, mas não executa nenhuma ação.

A derivação futura deve preservar:

- escopo núcleo de cada milestone;
- fora de escopo declarado;
- dependências entre capacidades;
- fronteiras de arquitetura;
- estratégia `milestones-only`;
- separação entre planejamento e State operacional;
- independência do runtime em relação a workflows externos;
- ausência de automação de gameplay por ferramentas externas.

Nenhuma informação deste documento deve ser interpretada como autorização automática de execução.
