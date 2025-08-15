# GRAD-Survivor


## 📜 Introdução

**GRAD-Survivor** é um jogo de ação e sobrevivência do gênero *top-down shooter*, onde o jogador assume o papel de um estudante tentando sobreviver a uma noite caótica no prédio da graduação. Enfrentando hordas crescentes de monstros, o jogador deve usar sua agilidade e power-ups — como Red Bulls para aumentar a velocidade e Subways para recuperar vida — para derrotar os inimigos e aguentar até o fim.
---

## 📖 História

A noite de sexta-feira prometia ser longa. No silêncio do prédio da graduação, um estudante dedicado corria contra o tempo para finalizar o temido projeto de Introdução à Programação. O café já não fazia efeito, e o cansaço começava a pesar. De repente, um barulho estranho ecoa pelos corredores vazios — um som que não pertencia àquele lugar.

Ao investigar, o estudante se depara com uma cena de pesadelo: a universidade foi invadida por criaturas bizarras, nascidas do estresse acadêmico e de códigos que deram errado. Armado apenas com sua coragem (e uma habilidade recém-descoberta de atirar cursores de mouse), ele precisa sobreviver a hordas de monstros até o amanhecer para, finalmente, entregar seu projeto.

---

## 🎮 Como Jogar

O objetivo é simples: sobreviver o maior tempo possível, derrotando todas as hordas de inimigos.

### Controles
* **Movimentação:** Use as teclas `W`, `A`, `S`, `D` para mover o personagem.
* **Mira:** A mira segue o cursor do seu mouse.
* **Atirar:** Clique com o **botão esquerdo do mouse** para disparar.

### Power-Ups
Ao derrotar inimigos, itens especiais podem aparecer. Pegue-os para ganhar vantagens:
* **Red Bull:** Aumenta temporariamente a sua velocidade de movimento.
* **Subway:** Recupera um coração de vida instantaneamente.
* **Crachá:** Aumenta temporariamente a sua velocidade de tiro.

---

## 🖼️ Galeria

| Tela Inicial | Gameplay Intenso | Fim de Jogo |
| :---: | :---: | :---: |
| ![Tela de Início do GRAD-Survivor](assets/images/inicio.png) | ![Gameplay do GRAD-Survivor](assets/images/win.png) | ![Tela de Game Over do GRAD-Survivor](assets/images/gameover.png) |

---

## 👥 Equipe e Divisão de Tarefas

| Foto | Membro | Responsabilidades Principais |
| :---: | :--- | :--- |
| <img src="https://github.com/henrique-github.png?size=100" width="100" alt="https://avatars.githubusercontent.com/u/163488602?v=4"> | [**Henrique**](https://github.com/henriqesl-github) | **[Líder Técnico / Gameplay]** - Lógica de tiro (`mouse.py`), integração do core (`game.py`), sistema de vida e música. |
| <img src="https://github.com/lucas-fernandes-github.png?size=100" width="100" alt="https://avatars.githubusercontent.com/u/207383959?v=4"> | [**Lucas Fernandes**](https://github.com/LucasFernandesCS) | **[Desenvolvedor de Gameplay]** - Implementação do jogador (`player.py`), sistema de itens coletáveis, UI (contadores) e lógica de vitória. |
| <img src="https://github.com/junior-cruz-github.png?size=100" width="100" alt="https://avatars.githubusercontent.com/u/224153797?v=4"> | [**Júnior Cruz**](https://github.com/juniorcruz7) | **[Desenvolvedor de Gameplay]** - Implementação do sistema de obstáculos e colisões, e ajustes na física dos monstros. |
| <img src="https://github.com/guilherme-siqueira-github.png?size=100" width="100" alt="https://avatars.githubusercontent.com/u/212376548?v=4"> | [**Guilherme Siqueira**](https://github.com/guimontenegro07) | **[Desenvolvedor de IA]** - Lógica de perseguição dos monstros (`enemies.py`) e integração da IA com o jogo principal. |
| <img src="https://github.com/luiz-taiguara-github.png?size=100" width="100" alt="https://avatars.githubusercontent.com/u/172301670?v=4"> | [**Luiz Taiguara**](https://github.com/LuizTaiguara) | **[Gerente de Projeto / Arquiteto]** - Organização da equipe, Gerenciamento do repositório (GitHub), definição da arquitetura modular, refatoração de código e apresentações. |
| <img src="https://github.com/tiago-mattos-github.png?size=100" width="100" alt="https://avatars.githubusercontent.com/u/223951608?v=4"> | [**Tiago Mattos**](https://github.com/tiagolmattos06) | **[Artista 2D / Designer de UI]** - Criação de todos os assets visuais (mapa, personagens, itens) e implementação do código da tela de início e das imagens de fim de jogo. |

---

## 💡 Metodologia

Adotamos uma abordagem inspirada em **Metodologias Ágeis**, focando em flexibilidade e entrega contínua. Em vez de planejar tudo no início, nossa estratégia foi construir primeiro uma **fundação de código forte e bem estruturada**.

Começamos desenvolvendo um **Produto Mínimo Viável (MVP)** — um protótipo simples, mas totalmente funcional, com o personagem se movendo, atirando e inimigos básicos. Com essa base sólida, pudemos iterar e desenvolver novas ideias de forma segura e organizada.

O progresso da **Equipe 7** foi dividido em ciclos curtos, refletidos nos checkpoints do projeto. A cada etapa, adicionávamos novas camadas de complexidade, como sistemas de itens, IA avançada e, por fim, o design e polimento visual. Essa abordagem nos permitiu adaptar e melhorar o jogo continuamente, atendendo as expectativas do grupo e ajudando no nosso desenvolvimento como alunos.

---

## 🏗️ Arquitetura e Estrutura do Projeto

Nossa arquitetura foi projetada para ser **modular e centralizada**, aplicando princípios importantes para a construção de softwares e criando uma base de código limpa, eficiente e passível de expansão.

### Visão Geral da Arquitetura

O coração do sistema é a classe `Game` (em `game.py`), que atua orquestrando todos os outros componentes. Lá acontece o loop principal, que controla os estados do jogo (menu, gameplay, etc.) e coordena a interação entre jogador, inimigos e itens.

As principais decisões de design incluem:

* **Separação de Responsabilidades:** Cada módulo tem uma função clara. O `monster_manager.py` cuida do ritmo e do spawn das hordas, enquanto o `collectible_items.py` gerencia a lógica de drop e os efeitos dos power-ups.
* **Desacoplamento de Dados:** O arquivo `game_data.py` funciona como uma configuração central, permitindo que o balanceamento do jogo (vida, velocidade, dano) seja ajustado sem alterar a lógica principal.
* **Reutilização de Código com Herança:** Em `enemies.py`, criamos uma classe `MonstroBase` que contém a lógica comum de movimento e a inteligência artificial (usando o algoritmo A* de `pathfinding.py`). As classes específicas `Monstro` e `Robo` **herdam** de `MonstroBase`, reutilizando todo esse comportamento e evitando a repetição de código. Essa abordagem torna a criação de novos inimigos muito mais simples.

Essa arquitetura modular não só organiza o projeto de forma lógica, mas também promove um código mais limpo e de fácil manutenção.

### Estrutura dos Diretórios e Arquivos

```
GRAD-SURVIVOR/
│
├── .gitignore
├── main.py
├── README.md
│
├── assets/
│   ├── images/
│   │   ├── sprites/
│   │   ├── maps/
│   │   └── icons/
│   │
│   └── sounds/
│       ├── music/
│       └── sfx/
│
└── src/  (ou grad_survivor/)
├── init.py
├── settings.py
├── game_data.py
├── game.py
├── player.py
├── enemies.py
├── monster_manager.py
├── collectible_items.py
├── mouse.py
├── obstacles.py
├── pathfinding.py
├── tela_inicial.py
└── end_screens.py
```

---

## 🛠️ Ferramentas e Bibliotecas

Para o desenvolvimento do **GRAD-Survivor**, utilizamos um conjunto de tecnologias que foram essenciais para transformar nossa visão em um jogo funcional e divertido.

### Tecnologias de Desenvolvimento
* **Python:** Linguagem principal do projeto, escolhida pela sua sintaxe clara e por ser a base da disciplina.
* **Pygame:** Framework fundamental que serviu como motor para o jogo, gerenciando gráficos, sons, animações e a captura de eventos (teclado e mouse).

### Bibliotecas Python Utilizadas
* **`os`:** Utilizada para a manipulação de caminhos de arquivos, garantindo que os assets (imagens e sons) fossem carregados corretamente.
* **`random`:** Essencial para adicionar elementos de aleatoriedade, como a chance de drop de itens e a escolha dos locais de spawn dos inimigos.
* **`heapq`:** Biblioteca crucial para a implementação performática do algoritmo A* em `pathfinding.py`, permitindo que a IA dos inimigos encontrasse o caminho mais curto de forma eficiente.
* **`math`:** Usada para criar efeitos visuais dinâmicos, como o brilho pulsante e as animações nas telas de vitória e game over.

### Ferramentas de Colaboração e Criação
* **GitHub:** Plataforma utilizada para o controle de versão do código, permitindo uma colaboração organizada e remota entre todos os membros da equipe.
* **Visual Studio Code:** Editor de código padrão adotado pelo grupo.
* **Discord / WhatsApp:** Ferramentas de comunicação utilizadas para o alinhamento constante da equipe.
* **Piskel:** Ferramenta online utilizada para a criação e edição de todas as sprites em pixel art do jogo, incluindo personagens, inimigos e itens.

---

## 🎓 Conceitos da Disciplina Utilizados

Durante o desenvolvimento do **GRAD-Survivor**, colocamos em prática diversos conceitos vistos ao longo da disciplina, aplicando-os diretamente na lógica e na estrutura do jogo, com uma complexidade crescente.

Começamos com os fundamentos. Os **comandos condicionais** (`if`, `else`) foram a base para toda a tomada de decisão no jogo, desde verificar se um tiro acertou um inimigo até aplicar o efeito de um item coletado. Os **laços de repetição** (`while` e `for`) foram igualmente essenciais, com o `while True` sustentando o *game loop* principal e os laços `for` sendo usados para atualizar cada inimigo na tela ou desenhar cada coração na interface.

Avançando, utilizamos **estruturas de dados** para organizar as informações. **Listas** foram usadas para gerenciar os obstáculos, enquanto **dicionários** se mostraram perfeitos para centralizar os atributos de personagens e itens no arquivo `game_data.py`, facilitando o balanceamento. Para a inteligência artificial, usamos uma **matriz** (lista de listas) para representar o mapa como uma grade, permitindo que o algoritmo A* encontrasse o melhor caminho.

Com a lógica se tornando mais complexa, o uso de **funções** foi crucial para organizar o código. Isolamos responsabilidades em blocos lógicos, como `drop_item()` e `aplicar_poder()`, tornando o código mais legível e evitando repetições.

Finalmente, adotamos o paradigma de **Programação Orientada a Objetos (POO)** para estruturar todo o projeto de forma modular. Criamos classes para representar cada entidade do jogo — `Player`, `MonstroBase`, `Mouse` —, encapsulando seus dados (atributos) e comportamentos (métodos). O conceito de **Herança** foi particularmente poderoso: criamos uma classe `MonstroBase` com toda a lógica de movimento e IA, e as classes `Monstro` e `Robo` simplesmente herdaram esse comportamento, o que nos permitiu criar diferentes tipos de inimigos de forma muito eficiente. Essa abordagem foi o que deu ao nosso projeto a organização e a escalabilidade necessárias para chegar ao resultado final.

---

## 🎯 Desafios e Lições Aprendidas

#### Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?

Nosso maior erro foi subestimar a complexidade da integração entre os diferentes sistemas do jogo. No início, a lógica de colisão dos obstáculos e a inteligência artificial dos inimigos foram desenvolvidas de forma isolada. Quando tentamos implementar o algoritmo de pathfinding, percebemos que a IA não "enxergava" os obstáculos, fazendo com que os inimigos ficassem presos.

**Como lidamos:** Tivemos que refatorar parte da inicialização do jogo. Criamos uma função que, ao carregar o mapa, converte as posições de todos os obstáculos em uma matriz que serve como um "mapa mental" para a IA. Isso nos ensinou a importância de planejar como os sistemas irão interagir desde o começo.

#### Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?

O maior desafio foi a **gestão do projeto e a comunicação da equipe**. Com cada membro desenvolvendo uma parte diferente, a tarefa de juntar as peças e unificar as ideias em um todo coeso foi complexa. Isso se refletiu no desafio técnico de utilizar o **GitHub**, uma ferramenta nova para a maioria, onde a dificuldade em gerenciar versões do código e resolver conflitos (*merge*) gerou atrasos.

**Como lidamos:** Superamos isso com comunicação constante e um fluxo de trabalho mais organizado. O membro com mais experiência em Git auxiliou os demais, e passamos a alinhar melhor as integrações. Esse processo, embora desafiador, se tornou um dos maiores aprendizados práticos sobre desenvolvimento do projeto.

#### Quais as lições aprendidas durante o projeto?

1.  **A Arquitetura Define o Sucesso:** Aprendemos que planejar uma boa arquitetura, usando conceitos de Programação Orientada a Objetos, não é um luxo, mas uma necessidade. Isso torna o código mais fácil de gerenciar, depurar e expandir.
2.  **Ferramentas de Colaboração São Essenciais:** Entendemos que o domínio de ferramentas como o Git é tão importante quanto saber programar. A capacidade de versionar e gerenciar o código de forma organizada é indispensável para o sucesso de qualquer projeto em equipe.
3.  **Refatorar Faz Parte do Processo:** Um código que funciona nem sempre é um código bom. Aprendemos a revisar e melhorar trechos do nosso próprio trabalho para aumentar a eficiência e a legibilidade, uma prática constante para garantir a qualidade do projeto.
4.  **Comece Simples, Adicione Complexidade:** A abordagem de criar um protótipo funcional primeiro e depois adicionar novas funcionalidades (como a IA avançada) nos permitiu ter um controle maior sobre o projeto e evitou que nos sentíssemos sobrecarregados.
