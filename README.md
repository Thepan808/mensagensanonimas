O mensagensanonimas é um bot escrito em Python que permite o envio de mensagens anônimas. Ele pode ser utilizado para criar interações anônimas entre usuários, geralmente em plataforma como o Telegram. O funcionamento exato vai depender do código do bot, mas a ideia principal é gerenciar mensagens de forma que o remetente não seja identificado.

#### Primeiro, CONFIGURE O .ENV
------------------

via Heroku

### Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Thepan808/mensagensanonimas)

Para rodar via Render:

<a href="https://render.com/deploy?repo=https://github.com/Thepan808/mensagensanonimas">
<img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render" />
</a>

#### Implantando este bot no Render. Basta seguir os passos abaixo:

- Faça um fork do repositório e importe-o no Render escolhendo a opção de serviços web.
- Escolha Python se algum servidor solicitar.
- No Render, use este comando como build: `pip install -r requirements.txt`.
- No comando de execução ou inicialização, use o seguinte comando: `gunicorn app:app & python3 bot.py`.
- Adicione todas as variáveis de ambiente na seção de variáveis de ambiente.

no final, troque as configuraçoes do .env e logo após hospedar, copie o link da implementação e vem aki
https://dashboard.uptimerobot.com/
e coloque o link pra monitorar caso desligar, já que render é free e encerra caso identifique ausência.

# Termux

Passo 1: Instale as dependências necessárias
Abra o Termux e atualize os pacotes:

`bash`
`pkg update && pkg upgrade`

# Instale o Python:

`bash
pkg install python`

# Instale o Git:

`bash
pkg install git`
# Instale o pip (gerenciador de pacotes do Python):

`bash
pkg install python-pip`

# Instale dependências adicionais:

`bash
pip install gunicorn`

# Passo 2: Clone o repositório
Faça o clone do repositório do GitHub:

`bash
git clone https://github.com/Thepan808/mensagensanonimas.git`

# Entre na pasta do repositório:

`bash
cd mensagensanonimas`
# Passo 3: Configure as dependências do projeto
Instale as dependências listadas no arquivo requirements.txt:
`bash
pip install -r requirements.txt`
# Passo 4: Configure o arquivo .env
Crie um arquivo .env na pasta do repositório:

`bash
nano .env`
# Adicione as variáveis de ambiente necessárias ao arquivo (baseando-se no README do projeto). Após editar, salve o arquivo pressionando CTRL + O, depois ENTER e CTRL + X para sair.

# Passo 5: Execute o bot
Execute o bot usando o Gunicorn e o script Python:
`bash
gunicorn app:app & python3 bot.py`
# Passo 6: Mantenha o bot ativo
# Para manter o bot rodando, você pode usar o tmux (um multiplexador de terminal):

`bash
pkg install tmux
tmux new -s bot_session`
# Dentro da nova sessão do tmux, inicie o bot:

`bash
gunicorn app:app & python3 bot.py`
# Para sair da sessão do tmux sem encerrar o bot, pressione `CTRL + B e depois D.`

# Para voltar à sessão do tmux, use:

`bash
tmux attach -t bot_session`
