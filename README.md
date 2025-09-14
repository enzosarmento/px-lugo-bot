# px-lugo-bot

Este projeto é um bot de futebol para o simulador Lugo, escrito em Python. Ele utiliza a biblioteca [lugo4py](https://github.com/lugobots/lugo4py) para interagir com o ambiente do jogo.

## Como baixar e rodar o projeto

### Pré-requisitos
- Python >= 3.9
- Docker e Docker Compose (opcional, mas recomendado)

### Instalação rápida (recomendado)
1. Clone este repositório:
    ```bash
    git clone <url-do-repositorio>
    cd px-lugo-bot
    ```
2. Execute o script de setup para instalar dependências e preparar o ambiente virtual:
    - No Linux/Mac:
      ```bash
      ./setup.sh
      ```
    - No Windows:
      ```powershell
      .\setup.ps1
      ```
3. Para rodar o bot junto com o servidor Lugo, utilize:
    ```bash
    docker compose up
    ```
    Acesse [http://localhost:8080/](http://localhost:8080/) para assistir ao jogo.

### Rodando localmente (avançado)
Se quiser rodar o bot diretamente na sua máquina:
1. Ative o ambiente virtual:
    ```bash
    source venv/bin/activate
    ```
2. Execute o bot:
    ```bash
    BOT_TEAM=home BOT_NUMBER=1 python3.9 src/main.py
    ```

## Estrutura do Projeto
- `src/main.py`: Inicializa o bot.
- `src/settings.py`: Configurações de posições e táticas.
- `src/my_bot.py`: Lógica principal do bot (edite aqui para mudar o comportamento).

## Principais métodos do `my_bot.py`

- `on_disputing`: Chamado quando a bola está disputada. O bot decide se tenta pegar a bola ou se posiciona.
- `on_defending`: Chamado quando um adversário está com a bola. O bot pode pressionar, defender ou se reposicionar.
- `on_holding`: Chamado quando o bot está com a bola. Decide se chuta, avança ou passa para um aliado.
- `on_supporting`: Chamado quando um companheiro está com a bola. O bot apoia, se posiciona para receber passe ou defende.
- `as_goalkeeper`: Chamado quando o bot é o goleiro. Decide se intercepta, passa ou se posiciona no gol.
- `getting_ready`: Executado antes do início do jogo ou após um gol.

Além desses, há funções auxiliares, que você pode criar para te auxiliar na construção da lógica do bot.

## Como contribuir
1. Faça um fork do projeto.
2. Crie uma branch para sua feature ou correção:
    ```bash
    git checkout -b minha-feature
    ```
3. Faça suas alterações e envie um pull request.

## Dicas
- Consulte o arquivo `README.md` original para mais detalhes sobre o ambiente Lugo.
- Edite o arquivo `src/my_bot.py` para alterar a inteligência do bot.
- Comente e documente suas funções para facilitar a colaboração!

## Dicas avançadas e extras

### Configuração manual do ambiente Python (Linux/Mac)
Se preferir configurar o ambiente manualmente:
```bash
sudo apt install python3.9-venv
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Dicas para IDEs
No VS Code, use o comando `Python: Create Environment` e selecione Python 3.9. Em IDEs JetBrains (PyCharm, etc), configure o interpretador do projeto para Python 3.9 e instale as dependências sugeridas.

### Sobre o Lugo
Se você não conhece o Lugo, acesse [o site oficial](https://lugobots.ai) para entender as regras e o funcionamento do simulador.

### Otimizando o uso do Docker
Você pode baixar previamente as imagens necessárias para acelerar o setup:
```bash
docker pull lugobots/server
docker pull lugobots/the-dummies-go:latest
docker pull python:3.9-slim-bookworm
```
Para instalar dependências via Docker Compose:
```bash
docker compose up builder
```
Depois, rode normalmente:
```bash
docker compose up
```
Acesse [http://localhost:8080/](http://localhost:8080/) para assistir ao jogo.

### Rodando o bot localmente com o servidor Docker
Você pode iniciar apenas o servidor do jogo com:
```bash
docker compose up -d game_server
```
Depois, rode seu bot localmente:
```bash
BOT_TEAM=home BOT_NUMBER=1 python3.9 src/main.py
```
E, por fim, suba o restante dos bots:
```bash
docker compose up
```