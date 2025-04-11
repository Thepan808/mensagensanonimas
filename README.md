O mensagensanonimas é um bot escrito em Python que permite o envio de mensagens anônimas. Ele pode ser utilizado para criar interações anônimas entre usuários, geralmente em plataforma como o Telegram. O funcionamento exato vai depender do código do bot, mas a ideia principal é gerenciar mensagens de forma que o remetente não seja identificado.

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
