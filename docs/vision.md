# Vision

## Finalidade

Este documento registra a direção macro do projeto `simple-chess-python`.

Ele descreve o que o projeto pretende ser, por que existe, quais capacidades fazem parte da visão inicial, quais limites devem ser preservados e quais decisões ainda precisam ser tomadas antes das próximas etapas.

Este documento não é arquitetura detalhada, roadmap, backlog, lista de milestones, issue, plano de execução ou especificação de implementação.

---

## Visão Geral do Projeto

`simple-chess-python` é um projeto de jogo de xadrez simples em Python, executado localmente, com foco em clareza, aprendizado, evolução incremental e apoio a fluxos futuros de desenvolvimento assistido por IA.

A visão renovada do projeto é construir um jogo de xadrez local que permita duas formas principais de jogo:

- **PvP local**: dois jogadores humanos jogando no mesmo ambiente;
- **PvC local**: um jogador humano jogando contra uma IA simples.

O projeto deve continuar pequeno e compreensível, mas agora passa a aceitar uma complexidade mínima adicional para torná-lo mais interessante como produto, como estudo de lógica de jogo e como alvo de implementação incremental.

A IA adversária não deve ser competitiva ou avançada. Ela deve ser simples, suficiente para criar uma experiência básica de jogo contra o computador, sem transformar o projeto em uma engine de xadrez.

---

## Problema ou Oportunidade

O projeto nasce da oportunidade de criar uma aplicação de xadrez pequena, mas não trivial, que sirva ao mesmo tempo para:

- praticar desenvolvimento em Python;
- exercitar separação entre lógica de jogo, interação do usuário e controle da partida;
- experimentar implementação incremental assistida por IA;
- fornecer um projeto controlado para validação de fluxos externos de automação e documentação;
- explorar uma IA simples sem entrar em complexidade de motor competitivo.

A oportunidade principal é construir algo pequeno o suficiente para ser implementável por etapas, mas rico o suficiente para exigir decisões reais de produto, arquitetura e validação.

---

## Público-Alvo ou Usuários

O público principal do projeto é o próprio mantenedor/desenvolvedor, que usará o projeto para aprendizado, experimentação e validação de processo.

Usuários secundários possíveis:

- pessoas interessadas em executar um jogo simples de xadrez local;
- avaliadores de portfólio;
- ferramentas ou fluxos externos que precisem ler a documentação do projeto para apoiar implementação, validação ou revisão;
- futuras sessões de IA que precisem entender o projeto com baixo custo de contexto.

O projeto não tem, nesta visão inicial, foco em usuários finais comerciais, ambiente de produção ou distribuição ampla.

---

## Objetivo Principal

Construir um jogo simples de xadrez em Python, executável localmente, que permita jogar uma partida básica em modo PvP local e em modo PvC contra uma IA simples.

O projeto deve preservar clareza estrutural, escopo controlado e documentação suficiente para orientar arquitetura, milestones e futuras implementações assistidas por IA.

---

## Objetivos Secundários

- Manter o projeto adequado para aprendizado e portfólio.
- Permitir evolução incremental sem exigir arquitetura pesada.
- Registrar decisões importantes de forma clara e versionável.
- Evitar que a IA adversária transforme o projeto em uma engine complexa.
- Permitir testes ou validações mínimas das regras centrais e do fluxo de partida.
- Preservar independência do jogo em relação a automações externas.
- Facilitar futuras derivações de issues sem inventar escopo.

---

## Núcleo do Projeto

O núcleo da visão inicial inclui:

- jogo de xadrez implementado em Python;
- execução local;
- modo PvP local;
- modo PvC local com IA simples;
- representação funcional do tabuleiro;
- representação das peças principais do xadrez;
- controle de turnos;
- validação de movimentos legais;
- rejeição de movimentos inválidos;
- captura de peças;
- identificação básica de estados relevantes da partida, como xeque, xeque-mate ou empate, conforme viabilidade técnica futura;
- interface local simples para interação com o jogo;
- separação conceitual entre lógica do jogo, controle da partida, interface e comportamento da IA;
- documentação fundacional suficiente para orientar próximas etapas.

---

## Funcionalidades ou Capacidades Desejadas

As capacidades desejadas em nível de visão são:

- iniciar uma nova partida;
- escolher modo de jogo PvP ou PvC;
- permitir que dois jogadores humanos joguem localmente;
- permitir que um jogador humano enfrente uma IA simples;
- permitir escolha ou definição inicial de lado, se isso não aumentar excessivamente o escopo;
- movimentar peças por uma interação local simples;
- exibir o tabuleiro e as peças de forma compreensível;
- indicar turno atual;
- impedir jogadas inválidas;
- aplicar capturas corretamente;
- informar estados básicos da partida;
- exibir mensagem de fim de jogo;
- manter histórico simples de movimentos, se isso se mostrar proporcional;
- permitir desfazer jogada, se isso não aumentar demais a complexidade inicial;
- registrar limitações conhecidas da IA simples.

Estas capacidades não devem ser tratadas automaticamente como backlog ou milestones. A priorização deve ser feita em documentos posteriores.

---

## Fora de Escopo

Não fazem parte da visão inicial:

- motor de xadrez competitivo;
- integração com Stockfish ou engines externas avançadas;
- IA forte ou com busca profunda complexa;
- multiplayer online;
- autenticação de usuários;
- ranking, matchmaking ou sistema de contas;
- servidor web obrigatório;
- aplicação web;
- banco de dados obrigatório;
- persistência complexa;
- suporte formal a torneios;
- relógio de xadrez obrigatório;
- análise avançada de posições;
- estudo aprofundado de aberturas;
- geração automática de partidas pelo sistema;
- automação do gameplay por ferramentas externas;
- transformar o projeto em framework genérico de jogos;
- criar uma arquitetura pesada incompatível com o tamanho do projeto.

---

## Restrições Conhecidas

- O projeto deve ser desenvolvido em Python.
- O jogo deve ser local e não web.
- O escopo deve permanecer pequeno e controlado.
- A IA adversária deve ser simples.
- O projeto deve ser compreensível para humanos e para IA.
- A documentação deve apoiar continuidade e implementação incremental.
- A automação externa pode apoiar o processo de desenvolvimento, mas não deve ser dependência funcional do jogo.
- Artefatos locais, caches, saídas de runtime e arquivos sensíveis não devem ser tratados como parte da visão do produto.
- Decisões arquiteturais detalhadas devem ser tomadas em etapa própria.
- A escolha final de bibliotecas, estrutura interna e estratégia de IA deve ser confirmada na arquitetura.

---

## Preferências do Usuário

- O usuário deseja manter o projeto como um jogo simples de xadrez em Python.
- O usuário deseja aumentar minimamente a complexidade do jogo antes da implementação.
- O usuário escolheu seguir com o caminho **PvP local + PvC com IA simples**.
- O usuário deseja que o projeto continue adequado para implementação por IA, especialmente por fluxo assistido com Codex CLI.
- O usuário deseja que o projeto sirva como alvo de validação prática de documentação e processo.
- O usuário prefere decisões explícitas e bem documentadas antes da implementação.
- O usuário não quer transformar o projeto em algo grande ou excessivamente sofisticado.

---

## Critérios de Sucesso

A visão será atendida quando:

- o jogo puder ser executado localmente;
- o usuário puder iniciar uma partida de xadrez;
- o usuário puder escolher entre PvP local e PvC local;
- dois jogadores humanos puderem jogar localmente;
- um jogador humano puder jogar contra uma IA simples;
- o tabuleiro e as peças forem compreensíveis;
- os turnos forem controlados corretamente;
- movimentos inválidos forem rejeitados;
- capturas forem aplicadas corretamente;
- estados básicos de encerramento forem tratados de forma suficiente para uma versão simples;
- a IA simples conseguir escolher movimentos legais;
- a complexidade da IA permanecer compatível com o escopo do projeto;
- a documentação fundacional estiver coerente com o comportamento esperado do projeto;
- o projeto permanecer independente de automações externas para funcionar.

---

## Riscos e Incertezas

- A inclusão de PvC pode aumentar o escopo além do desejado se a IA não for claramente limitada.
- A definição de “IA simples” precisa ser refinada antes da implementação.
- Ainda é necessário decidir se a IA será aleatória, baseada em avaliação material simples ou em outra estratégia leve.
- A interface local ainda precisa ser detalhada em etapa arquitetural.
- Histórico de movimentos, desfazer jogada e salvamento podem ser úteis, mas podem aumentar o escopo se forem tratados como obrigatórios cedo demais.
- O tratamento completo de regras especiais do xadrez pode gerar complexidade se não for apoiado por biblioteca apropriada.
- Há risco de misturar lógica de IA, lógica de regras e interface se a arquitetura não definir fronteiras claras.
- Há risco de overengineering se o projeto tentar antecipar recursos avançados.

---

## Decisões Pendentes

As seguintes decisões devem ser tomadas em etapas posteriores:

- biblioteca ou abordagem para interface local;
- forma final de interação do usuário, como mouse, teclado ou combinação;
- estratégia da IA simples;
- nível inicial de dificuldade da IA;
- se haverá escolha de cor no modo PvC;
- se histórico de movimentos entra no núcleo inicial ou fica como melhoria posterior;
- se desfazer jogada entra no núcleo inicial ou fica como melhoria posterior;
- se salvar/carregar partida entra no núcleo inicial ou fica como melhoria posterior;
- como representar visualmente estados como xeque, xeque-mate e empate;
- quais validações mínimas serão exigidas antes de considerar a versão inicial concluída;
- como a documentação da implementação será organizada ao longo do projeto.

---

## Âncoras para Arquitetura

A futura arquitetura deve considerar:

- separação entre regras do xadrez, fluxo da partida, interface e IA;
- manutenção da aplicação como local e não web;
- suporte a dois modos de jogo: PvP e PvC;
- limitação explícita da IA para evitar complexidade de engine competitiva;
- possibilidade de trocar ou evoluir a estratégia da IA sem reescrever o jogo inteiro;
- necessidade de validar movimentos legais de forma confiável;
- necessidade de manter baixo acoplamento entre interface e regras;
- necessidade de testes mínimos para domínio, fluxo de partida e IA simples;
- risco de overengineering;
- facilidade de compreensão por IA e por humanos;
- independência do runtime em relação a workflows externos;
- clareza sobre quais bibliotecas são dependências do jogo e quais ferramentas são apenas apoio de desenvolvimento.

A arquitetura não deve ser definida neste documento.

---

## Âncoras para Milestones

As futuras milestones devem considerar, em ordem conceitual, capacidades como:

- fundação documental do projeto;
- definição da estrutura técnica inicial;
- implementação das regras e estado base do jogo;
- implementação do fluxo de partida;
- implementação do modo PvP local;
- implementação da IA simples;
- integração do modo PvC;
- implementação da interface local;
- validação mínima de regras, turnos, movimentos e IA;
- fechamento de uma versão inicial executável.

As milestones devem separar capacidades reais, evitando misturar interface, IA, regras, testes e fechamento documental em uma única etapa grande demais.

A geração de milestones deve preservar os limites desta visão e não transformar funcionalidades opcionais em obrigações sem decisão explícita.

---

## Âncoras para Documentação da Implementação

Como o projeto será implementado com apoio recorrente de IA, a documentação da implementação pode se tornar útil para preservar continuidade entre etapas.

Sinais que devem ser avaliados futuramente:

- o projeto terá múltiplas áreas com responsabilidades diferentes;
- haverá lógica de jogo, interface e IA simples;
- decisões futuras podem precisar ser reaproveitadas por outras sessões de IA;
- o custo de contexto pode crescer conforme o projeto evoluir;
- documentação excessiva pode ser desproporcional para um jogo pequeno.

Estratégias possíveis a avaliar futuramente:

- `milestones-only`;
- `implementation-map-single`;
- `implementation-map-hierarchical`;
- `implementation-index-assisted`;
- `not-applicable`.

A estratégia final não deve ser decidida neste documento.

---

## Notas para Próximos Passos

O próximo passo documental provável é gerar ou reformular `docs/architecture.md` com base nesta visão renovada.

A arquitetura deve avaliar especialmente:

- fronteiras entre regras, aplicação, interface e IA;
- estratégia inicial da IA simples;
- biblioteca de interface local;
- dependências adequadas para regras de xadrez;
- estrutura de diretórios;
- estratégia mínima de testes;
- como preservar simplicidade sem bloquear evolução.

Depois da arquitetura, o projeto poderá ter `docs/milestones.md` reformulado para refletir a nova visão com PvP local e PvC com IA simples.
