# Architecture

## Finalidade

Este documento registra a arquitetura inicial do projeto `simple-chess-python`.

O objetivo é transformar a visão renovada do projeto em decisões arquiteturais explícitas, proporcionais e consultáveis, capazes de orientar futuras etapas de planejamento, derivação de issues e handoffs de implementação.

Este documento não executa implementação, não define roadmap detalhado, não cria milestones, não gera issues, não substitui documentação de uso e não descreve comandos operacionais.

---

## Resumo da Arquitetura

O `simple-chess-python` será uma aplicação local de xadrez em Python, não web, com suporte a dois modos de jogo:

- PvP local: dois jogadores humanos jogando no mesmo ambiente;
- PvC local: um jogador humano contra uma IA simples.

A arquitetura adotará um modelo **modular simples em camadas leves**, preservando separação entre interface, aplicação, domínio, IA e ferramentas externas.

A direção geral de dependências será:

```text
ui → app → domain → python-chess
        ↘ ai → domain
```

A biblioteca `python-chess` será usada como motor de regras de xadrez e deverá permanecer encapsulada na camada de domínio.

A interface local será implementada com Pygame, com interação principal por mouse.

A IA inicial será aleatória: ela escolherá um movimento legal disponível. A IA não deverá alterar diretamente o estado do jogo. Ela deverá apenas selecionar uma jogada candidata, cabendo à camada de aplicação coordenar a aplicação do movimento por meio do domínio.

O `n8n-local-stack`, Codex CLI ou qualquer outro workflow externo poderá apoiar o processo de implementação, validação e revisão, mas não fará parte do runtime do jogo.

---

## Contexto Derivado da Visão

A visão renovada define o projeto como um jogo simples de xadrez em Python, executado localmente, com foco em clareza, aprendizado, evolução incremental e apoio a fluxos futuros de desenvolvimento assistido por IA.

A visão também define que o projeto deve oferecer uma complexidade mínima adicional em relação a um xadrez local básico, incluindo:

- modo PvP local;
- modo PvC local;
- IA simples;
- representação funcional do tabuleiro;
- validação de movimentos legais;
- rejeição de movimentos inválidos;
- captura de peças;
- controle de turnos;
- interface local simples;
- documentação fundacional suficiente para continuidade.

A visão exclui explicitamente recursos como aplicação web, multiplayer online, engine competitiva, integração com Stockfish, persistência complexa, banco de dados obrigatório, automação do gameplay e arquitetura pesada.

---

## Objetivos Arquiteturais

A arquitetura deve garantir:

- execução local do jogo;
- simplicidade proporcional ao tamanho do projeto;
- separação clara de responsabilidades;
- baixo acoplamento entre interface, regras, fluxo de partida e IA;
- uso confiável de uma biblioteca de xadrez para regras;
- encapsulamento da biblioteca de regras no domínio;
- suporte aos modos PvP local e PvC local;
- IA simples, substituível e limitada;
- facilidade de teste das regras, do fluxo da partida e da IA simples;
- legibilidade para humanos e para ferramentas de IA;
- independência do runtime em relação a workflows externos;
- documentação suficiente para orientar futuras etapas sem gerar excesso documental.

---

## Não Objetivos Arquiteturais

A arquitetura não pretende resolver, nesta fase:

- multiplayer online;
- autenticação;
- ranking ou matchmaking;
- aplicação web;
- API HTTP;
- banco de dados;
- persistência complexa;
- salvamento e carregamento de partidas;
- desfazer jogada;
- relógio de xadrez obrigatório;
- engine própria competitiva;
- integração com Stockfish;
- análise avançada de posições;
- automação de gameplay por ferramentas externas;
- arquitetura orientada a eventos;
- Clean Architecture rígida;
- arquitetura de microserviços;
- criação de Implementation Map nesta etapa.

---

## Drivers Arquiteturais

Os principais fatores que influenciam a arquitetura são:

- o projeto deve continuar pequeno e compreensível;
- a aplicação deve ser local e não web;
- o jogo precisa suportar PvP e PvC;
- a IA deve existir, mas ser simples;
- as regras do xadrez devem ser confiáveis;
- o projeto será implementado de forma incremental;
- sessões futuras de IA devem conseguir compreender o projeto com baixo custo de contexto;
- documentação, workflows e ferramentas externas devem apoiar o processo, mas não pertencer ao runtime;
- decisões relevantes devem ser registradas antes de alterar fronteiras arquiteturais;
- recursos opcionais não devem virar requisitos obrigatórios sem decisão explícita.

---

## Princípios e Restrições

A arquitetura deve seguir os seguintes princípios:

- manter o jogo executável localmente;
- preservar a separação entre runtime do jogo e automação externa;
- preservar a separação entre estado da partida e estado operacional do projeto;
- manter `python-chess` encapsulado no domínio;
- manter Pygame restrito à camada de interface;
- manter a IA separada da interface;
- manter a IA impedida de alterar diretamente o estado do jogo;
- evitar overengineering;
- evitar dependências externas desnecessárias;
- registrar decisões relevantes de forma clara;
- não tratar documentação como implementação;
- não tratar workflows como parte funcional do jogo;
- não versionar segredos, caches, artefatos locais ou saídas brutas de runtime.

---

## Componentes ou Áreas Principais

A arquitetura será organizada em áreas principais:

- **Domínio**: regras do xadrez, tabuleiro, movimentos legais, estado da partida e integração encapsulada com `python-chess`.
- **Aplicação**: coordenação de modo de jogo, turno, seleção, tentativa de movimento, chamada da IA e atualização do estado.
- **IA**: estratégia simples de escolha de movimento para o computador.
- **Interface**: janela local, renderização do tabuleiro, entrada do usuário e feedback visual.
- **Testes e validação**: verificação mínima de domínio, aplicação, IA e fronteiras arquiteturais.
- **Documentação**: visão, arquitetura, milestones e documentos de apoio ao processo.
- **Tooling externo**: ferramentas e workflows usados para apoiar implementação, validação e revisão, sem participação no runtime.

---

## Responsabilidades

### Domínio

A área de domínio é responsável por:

- representar o tabuleiro;
- consultar posição das peças;
- validar movimentos legais;
- aplicar movimentos válidos;
- rejeitar movimentos inválidos;
- consultar turno atual;
- consultar estados como xeque, xeque-mate, empate ou partida em andamento;
- encapsular o uso de `python-chess`.

O domínio não deve depender de Pygame, de workflows externos, de entrada de mouse ou de lógica visual.

### Aplicação

A área de aplicação é responsável por:

- controlar a sessão da partida;
- manter o modo de jogo ativo;
- distinguir jogador humano e jogador computador;
- controlar o fluxo de turnos;
- receber intenções de movimento vindas da interface;
- solicitar validação ao domínio;
- aplicar movimentos por meio do domínio;
- chamar a IA quando for a vez do computador;
- expor informações necessárias para a interface.

A aplicação não deve desenhar tela, manipular eventos de Pygame diretamente ou implementar regras de xadrez manualmente.

### IA

A área de IA é responsável por:

- receber uma visão suficiente do estado atual da partida;
- consultar movimentos legais disponíveis por meio de interfaces do domínio ou da aplicação;
- escolher um movimento legal;
- retornar o movimento escolhido para a aplicação.

A IA inicial será aleatória.

A IA não deve:

- alterar diretamente o estado da partida;
- conhecer detalhes de Pygame;
- substituir a validação de regras do domínio;
- implementar uma engine competitiva;
- depender de workflows externos.

### Interface

A área de interface é responsável por:

- abrir a janela local do jogo;
- renderizar o tabuleiro;
- representar peças de forma compreensível;
- capturar cliques do usuário;
- converter interações em intenções de movimento;
- exibir turno atual, mensagens e estados básicos;
- permitir seleção de modo PvP ou PvC;
- solicitar ações à camada de aplicação.

A interface não deve validar regras de xadrez, escolher movimentos da IA ou manipular diretamente `python-chess`.

### Testes e validação

A área de testes e validação é responsável por verificar, de forma proporcional:

- movimentos legais e ilegais;
- controle de turnos;
- fluxo de aplicação;
- comportamento da IA aleatória como seletora de movimentos legais;
- preservação das fronteiras entre camadas;
- independência do runtime em relação a ferramentas externas.

### Documentação e tooling externo

A documentação registra decisões e orienta continuidade.

Ferramentas externas, como workflows, agentes ou CLI de apoio, podem auxiliar implementação e validação, mas não são parte do runtime do jogo.

---

## Fronteiras e Boundaries

### Runtime do jogo vs automação externa

O runtime do jogo é a aplicação Python local.

Fazem parte do runtime:

- código Python do jogo;
- biblioteca de xadrez;
- Pygame;
- módulo de IA simples;
- assets locais necessários à interface, se existirem.

Não fazem parte do runtime:

- workflows externos;
- arquivos de controle operacional do pipeline;
- logs brutos;
- evidências de validação;
- documentos de planejamento;
- ferramentas de implementação assistida.

### Estado da partida vs estado operacional do projeto

O estado da partida representa informações do jogo, como:

- tabuleiro;
- turno;
- modo de jogo;
- jogador atual;
- estado da partida;
- movimento selecionado;
- histórico interno mínimo, se necessário.

O estado operacional do projeto representa informações de processo, como milestone vigente, validações ou controle de workflow.

Esses dois conceitos não devem ser misturados.

### Interface vs regras

A interface captura interação e exibe informação.

A validação de movimentos pertence ao domínio.

### IA vs regras

A IA escolhe entre movimentos legais.

Ela não define o que é legal ou ilegal. Essa responsabilidade pertence ao domínio.

### Aplicação vs domínio

A aplicação coordena fluxo.

O domínio protege regras e estado central da partida.

### Documentação vs execução

Documentos orientam decisões e continuidade.

Eles não executam ações, não substituem código e não autorizam alterações automáticas.

---

## Fluxos Principais

### Inicialização do jogo

```text
abrir aplicação
→ inicializar interface local
→ exibir opção de modo de jogo
→ criar sessão de partida
→ inicializar estado do tabuleiro
→ renderizar tabuleiro inicial
```

### Fluxo PvP local

```text
jogador humano seleciona peça
→ jogador humano seleciona destino
→ interface envia intenção à aplicação
→ aplicação solicita validação ao domínio
→ domínio valida movimento
→ aplicação aplica movimento válido
→ turno alterna
→ interface redesenha estado atualizado
```

### Fluxo PvC local

```text
jogador humano joga com brancas
→ interface envia intenção à aplicação
→ aplicação valida e aplica movimento humano via domínio
→ aplicação identifica turno do computador
→ aplicação solicita movimento à IA
→ IA escolhe movimento legal aleatório
→ aplicação aplica movimento da IA via domínio
→ interface redesenha estado atualizado
```

### Fluxo de movimento inválido

```text
usuário tenta movimento
→ aplicação solicita validação ao domínio
→ domínio rejeita movimento
→ aplicação preserva estado da partida
→ interface exibe feedback mínimo
```

### Fluxo de fim de partida

```text
movimento válido é aplicado
→ domínio atualiza estado
→ aplicação consulta estado final
→ interface exibe mensagem de encerramento quando aplicável
```

---

## Dados, Artefatos ou Documentos Relevantes

### Dados de jogo

Dados relevantes ao runtime:

- estado do tabuleiro;
- lado atual;
- modo de jogo;
- tipo de jogador por lado;
- movimento selecionado;
- movimentos legais disponíveis;
- estado da partida;
- mensagem de feedback para o usuário.

### Artefatos documentais

Documentos relevantes ao projeto:

- `README.md`;
- `docs/vision.md`;
- `docs/architecture.md`;
- `docs/milestones.md`;
- documentação futura de validação ou encerramento, se adotada.

### Artefatos operacionais

Artefatos operacionais externos podem existir para apoiar workflows e validações, mas não devem ser tratados como parte do jogo.

Se houver estado operacional de milestone, ele deve controlar o processo do projeto, não o estado da partida.

---

## Runtime, Tooling e Workflows

### Runtime

O runtime esperado é uma aplicação Python local.

Dependências funcionais previstas:

- biblioteca de xadrez para regras;
- Pygame para interface local;
- módulo interno de IA simples.

### Tooling de desenvolvimento

Ferramentas de desenvolvimento podem incluir:

- testes automatizados;
- lint e formatação;
- ambiente local de desenvolvimento;
- ferramentas assistivas de implementação.

Essas ferramentas não devem ser confundidas com o runtime do jogo.

### Workflows externos

Workflows externos podem apoiar:

- leitura de documentação;
- derivação futura de trabalho;
- validação estrutural;
- validação de testes;
- revisão de aderência arquitetural;
- geração de evidência reduzida.

Workflows externos não devem:

- controlar o gameplay;
- ser requisito para abrir o jogo;
- alterar estado da partida;
- substituir revisão humana em decisões relevantes;
- ser fonte única de verdade sobre o comportamento do jogo.

---

## Segurança, Versionamento e Rastreabilidade

O projeto deve preservar regras básicas de segurança e higiene de versionamento:

- não versionar segredos;
- não versionar `.env` real;
- não versionar tokens;
- não versionar credenciais;
- não versionar caches locais;
- não versionar logs brutos;
- não versionar payloads sensíveis;
- não versionar saídas locais de runtime sem necessidade explícita;
- manter decisões arquiteturais relevantes registradas;
- registrar mudanças de fronteira antes de implementá-las;
- manter rastreabilidade entre visão, arquitetura, milestones e implementação futura.

O projeto não deve exigir dados sensíveis para funcionamento.

---

## Estratégia de Documentação da Implementação

Estratégia escolhida: `milestones-only`.

Justificativa:

- o projeto ainda é pequeno;
- a arquitetura é modular, mas não grande o suficiente para exigir mapa dedicado;
- `docs/milestones.md` deve ser suficiente para orientar continuidade inicial;
- criar um Implementation Map agora adicionaria custo documental prematuro;
- o foco inicial deve permanecer em visão, arquitetura, milestones, issues futuras e handoffs controlados.

Quando revisar esta decisão:

- se o projeto crescer além dos módulos centrais previstos;
- se a navegação entre domínio, aplicação, IA e interface começar a gerar alto custo de contexto;
- se handoffs futuros exigirem descrição acumulativa de módulos e decisões locais;
- se a documentação de milestones deixar de ser suficiente para orientar continuidade.

Quando criar documentação acumulativa:

- se houver múltiplas áreas evoluindo em paralelo;
- se a IA precisar de orientação recorrente sobre módulos já implementados;
- se decisões locais começarem a se perder entre implementações.

Quando não criar ou atualizar documentação acumulativa:

- para mudanças pequenas e autoexplicativas;
- para registrar cada microalteração como se fosse changelog;
- para substituir leitura dos arquivos reais;
- para duplicar conteúdo já claro em visão, arquitetura ou milestones.

Limites:

- um Implementation Map, se adotado futuramente, deve orientar navegação;
- ele não deve substituir arquivos reais;
- ele não deve virar fonte absoluta de verdade;
- ele não deve substituir issues, handoffs ou revisão humana;
- a ausência de Implementation Map não é falha enquanto a estratégia vigente for `milestones-only`.

---

## Impacto Esperado sobre Milestones

A futura geração de milestones deve respeitar as seguintes diretrizes:

- começar por fundação documental e estrutura técnica mínima;
- separar domínio, aplicação, IA e interface em capacidades planejáveis;
- tratar PvP e PvC como capacidades relacionadas, mas com complexidades diferentes;
- não antecipar recursos fora do escopo inicial, como salvar/carregar, desfazer jogada ou IA avançada;
- validar cedo o encapsulamento da biblioteca de xadrez;
- validar cedo que a IA só escolhe movimentos legais e não altera estado diretamente;
- manter n8n, workflows e tooling fora do runtime;
- planejar testes proporcionais para domínio, aplicação e IA;
- reservar refinamentos visuais para depois da jogabilidade mínima;
- não tratar recursos opcionais como obrigatórios sem decisão explícita.

A documentação de milestones deve refletir a estratégia `milestones-only` e não criar Implementation Map por padrão.

---

## Riscos e Trade-offs

### Simplicidade vs extensibilidade

A arquitetura deve ser simples, mas ainda permitir evolução da IA. O risco é criar abstrações demais antes da necessidade.

### IA aleatória vs experiência do usuário

A IA aleatória é simples e fácil de validar, mas joga mal. Essa decisão favorece implementação controlada em vez de qualidade competitiva.

### Uso de biblioteca de xadrez vs controle total

Usar uma biblioteca reduz risco de erro nas regras, mas cria dependência externa. O encapsulamento no domínio reduz esse acoplamento.

### Interface simples vs refinamento visual

Uma interface simples acelera a versão inicial, mas pode limitar a percepção de qualidade. Refinamentos visuais devem ser tratados como evolução futura.

### Documentação suficiente vs documentação excessiva

A estratégia `milestones-only` reduz custo documental, mas pode precisar ser revista se o projeto crescer.

### Automação externa vs independência do jogo

Workflows externos podem apoiar o processo, mas devem permanecer fora do runtime para preservar independência da aplicação.

---

## Lacunas e Decisões Pendentes

As seguintes decisões permanecem pendentes:

- definir se a interface usará peças em Unicode, imagens simples ou sprites;
- definir o nível visual mínimo aceitável para a primeira versão;
- definir como a seleção de modo PvP/PvC será apresentada;
- definir se haverá menu inicial ou configuração simples dentro da própria tela;
- definir como mensagens de xeque, xeque-mate e empate serão exibidas;
- definir se haverá histórico interno mínimo apenas para suporte técnico;
- definir se uma estratégia de IA material simples será considerada em versão futura;
- definir critérios mínimos de validação para considerar o modo PvC concluído;
- definir se haverá documentação futura específica para decisões de IA.

Essas lacunas não bloqueiam a arquitetura inicial, mas devem ser resolvidas antes de afetarem implementação.

---

## Critérios de Validação Arquitetural

A arquitetura será considerada aderente se:

- estiver alinhada à visão renovada;
- preservar aplicação local e não web;
- suportar PvP local e PvC local;
- mantiver IA simples e limitada;
- mantiver a IA separada da interface;
- impedir que a IA altere diretamente o estado do jogo;
- mantiver validação de regras no domínio;
- mantiver a biblioteca de xadrez encapsulada;
- mantiver Pygame restrito à interface;
- preservar separação entre runtime e workflows externos;
- preservar separação entre estado da partida e estado operacional do projeto;
- evitar overengineering;
- orientar futuras milestones sem criá-las;
- declarar estratégia de documentação da implementação;
- não introduzir recursos fora do escopo inicial.

---

## Notas para Futuras Milestones

A futura etapa de planejamento deve considerar que:

- documentação fundacional deve vir antes da implementação técnica;
- estrutura base do projeto deve vir antes de domínio, aplicação, IA e interface;
- domínio e validação de regras devem ser tratados antes da integração visual completa;
- a IA aleatória deve ser introduzida como capacidade isolável;
- o modo PvP pode ser uma base natural para o modo PvC;
- o modo PvC deve validar que a aplicação coordena a chamada da IA;
- testes devem cobrir pelo menos domínio, aplicação e IA simples;
- refinamentos visuais, salvar/carregar, desfazer jogada e IA mais inteligente não devem entrar na versão inicial sem nova decisão;
- workflows externos podem validar e revisar, mas não devem ser tratados como parte do jogo.

---

## Decisões Arquiteturais Registradas

### ADR-001 — Arquitetura modular simples em camadas leves

Decisão: adotar arquitetura modular simples em camadas leves.

Motivo: o projeto precisa continuar pequeno, compreensível e adequado para implementação incremental.

Consequência: o projeto separará domínio, aplicação, IA e interface sem adotar arquitetura pesada.

### ADR-002 — Aplicação local, não web

Decisão: manter o jogo como aplicação local.

Motivo: a visão exclui aplicação web e multiplayer online da versão inicial.

Consequência: não haverá servidor web, API HTTP ou autenticação na arquitetura inicial.

### ADR-003 — Uso de biblioteca de xadrez para regras

Decisão: usar uma biblioteca de xadrez para validação de regras.

Motivo: isso reduz risco de erro em regras complexas e mantém o foco do projeto no jogo, na interface, na IA simples e no processo incremental.

Consequência: a implementação inicial não será uma engine própria de xadrez.

### ADR-004 — Encapsulamento da biblioteca de xadrez no domínio

Decisão: encapsular a biblioteca de xadrez na camada de domínio.

Motivo: evitar acoplamento externo espalhado pelo projeto.

Consequência: interface, aplicação e IA não devem depender diretamente da biblioteca de regras.

### ADR-005 — Separação de IA em módulo próprio

Decisão: manter a IA em área própria.

Motivo: a IA representa comportamento de jogador computador, não regra do xadrez nem renderização.

Consequência: a IA poderá evoluir sem reescrever interface ou domínio.

### ADR-006 — IA aleatória como estratégia inicial

Decisão: usar IA aleatória na versão inicial.

Motivo: é a opção mais simples, verificável e proporcional ao projeto.

Consequência: a IA jogará mal, mas deverá sempre escolher movimentos legais.

### ADR-007 — Humano joga de brancas no PvC inicial

Decisão: no modo PvC inicial, o jogador humano joga de brancas.

Motivo: reduz complexidade de fluxo e evita decisões adicionais na primeira versão.

Consequência: escolha de cor pode ser considerada futuramente, mas não pertence ao núcleo inicial.

### ADR-008 — Sem desfazer jogada na versão inicial

Decisão: não incluir desfazer jogada na versão inicial.

Motivo: em PvC, desfazer pode envolver regras adicionais sobre desfazer movimento humano e resposta da IA.

Consequência: a funcionalidade pode ser reavaliada futuramente.

### ADR-009 — Sem salvar/carregar partida na versão inicial

Decisão: manter salvamento e carregamento fora do escopo inicial.

Motivo: persistência adicionaria complexidade desnecessária para a primeira versão.

Consequência: formatos como FEN, PGN ou JSON podem ser avaliados futuramente.

### ADR-010 — Workflows externos fora do runtime

Decisão: manter workflows externos fora do runtime do jogo.

Motivo: ferramentas de implementação e validação não devem ser dependência funcional da aplicação.

Consequência: o jogo deve funcionar localmente sem orquestração externa.

### ADR-011 — Estratégia inicial de documentação da implementação: milestones-only

Decisão: adotar `milestones-only` como estratégia inicial de documentação da implementação.

Motivo: o projeto ainda é pequeno e não justifica mapa dedicado neste estágio.

Consequência: a criação de Implementation Map deve ser reavaliada apenas se o custo de contexto crescer.
