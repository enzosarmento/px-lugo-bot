# Px Bot

Este é um bot para o [Lugo](https://github.com/lugobots/lugo), um jogo de futebol de robôs 5x5. O bot foi desenvolvido em Python e utiliza a biblioteca `lugo4py`.

## Como Começar

Primeiro, você precisa ter o código do projeto na sua máquina.

```bash
git clone https://github.com/enzosarmento/px_bot.git
cd px_bot
```

## Como Rodar o Projeto

### Rodando com Docker (Recomendado)

Esta é a maneira mais simples de rodar o projeto, pois já configura todo o ambiente necessário, incluindo o servidor do jogo. Você não precisa executar o `main.py` manualmente.

1.  **Tenha o Docker e o Docker Compose instalados.**

2.  **(Opcional) Baixe as imagens Docker para acelerar o processo:**

    ```bash
    docker pull lugobots/server
    docker pull lugobots/the-dummies-go:latest
    docker pull python:3.9-slim-buster
    ```

3.  **Execute o serviço do construtor para instalar as dependências:**

    Este comando irá construir a imagem do bot com todas as dependências necessárias. Espere até que ele seja concluído.

    ```bash
    docker compose up builder
    ```

4.  **Execute o jogo:**

    ```bash
    docker compose up
    ```

5.  **Abra o navegador em [http://localhost:8080](http://localhost:8080)** para assistir ao jogo.

### Rodando Localmente para Desenvolvimento

Esta abordagem é ideal para quando você está desenvolvendo e testando o bot. Você precisará de um ambiente Python configurado.

1.  **Crie um ambiente virtual:**

    A biblioteca `lugo4py` pode ter conflitos com outras bibliotecas, então é altamente recomendado usar um ambiente virtual.

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # No Windows, use `.venv\Scripts\activate`
    ```

2.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute o bot:**

    Você precisará ter o servidor do Lugo rodando separadamente (por exemplo, via Docker). Então, você pode rodar o bot:

    ```bash
    python src/main.py
    ```

## Ferramentas Úteis

### Lugo Studio

Na pasta `lugo_studio` você encontrará o **Lugo Studio**, uma ferramenta para ajudar no desenvolvimento e análise do seu bot. Existe um instalador para Windows e um AppImage para Linux.

**Importante:** Se você utilizar o Lugo Studio, não é necessário rodar os comandos do Docker manualmente. O próprio Lugo Studio cuidará de iniciar os contêineres, mas você **ainda precisa ter o Docker instalado** na sua máquina.

### Criador de Estratégias

Para ajudar a criar e visualizar as posições táticas dos jogadores, você pode usar esta ferramenta online:

[**Strategy Creator for Lugo Bots**](https://mauriciorobertodev.github.io/strategy-creator-lugo-bots/)

## Como Contribuir

Contribuições são bem-vindas! Se você quiser melhorar este bot, siga os passos abaixo:

1.  **Faça um fork do projeto.**
2.  **Crie uma nova branch para sua feature:** `git checkout -b feature/nova-feature`
3.  **Faça suas alterações e commit:** `git commit -m 'Adiciona nova feature'`
4.  **Envie para a sua branch:** `git push origin feature/nova-feature`
5.  **Abra um Pull Request.**

## Funcionalidades (`my_bot.py`)

O arquivo `my_bot.py` contém a lógica principal do bot. Ele é dividido em vários métodos que são chamados dependendo do estado do jogo.

### Principais Métodos

*   `on_disputing(...)`: Chamado quando a bola está em disputa. O bot decide se tenta pegar a bola ou se posiciona.
*   `on_defending(...)`: Chamado quando o time adversário tem a posse da bola. O bot decide se pressiona o adversário ou mantém a posição defensiva.
*   `on_holding(...)`: Chamado quando o bot tem a posse da bola. Ele decide se chuta para o gol, avança ou passa para um companheiro.
*   `on_supporting(...)`: Chamado quando um companheiro de time tem a posse da bola. O bot se posiciona para receber um passe ou para apoiar o jogador.
*   `as_goalkeeper(...)`: Lógica específica para o goleiro. Decide se passa a bola, intercepta um chute ou se posiciona no gol.
*   `dynamic_defensive_position(...)`: Calcula uma posição defensiva dinâmica com base na posição da bola, para que a defesa se mova em bloco.
*   `find_best_shot_target(...)`: Encontra o melhor lugar para chutar no gol, tentando evitar o goleiro adversário.

## Configurações (`settings.py`)

O arquivo `settings.py` é usado para definir as posições e táticas do time.

*   `MAPPER_COLS` e `MAPPER_ROWS`: Definem o número de "regiões" no campo. Quanto maior o número, mais preciso será o posicionamento dos jogadores.
*   `PLAYER_INITIAL_POSITIONS`: Um dicionário que define a posição inicial de cada jogador no campo.
*   `get_my_expected_position(...)`: Esta função determina a posição que o jogador deve ocupar com base no estado do jogo (defensivo, normal ou ofensivo). A tática muda dependendo da posição da bola no campo.
