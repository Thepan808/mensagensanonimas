import os
import logging
import asyncio
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do bot
try:
    API_ID = int(os.getenv("API_ID"))
except ValueError:
    raise ValueError("O valor de API_ID deve ser um número inteiro válido.")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Configuração de logging detalhado
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Inicializando o bot
bot = Client(
    "anon_messages_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=8,
    sleep_threshold=10,
    in_memory=True
)

# Função para envio com retentativa
async def enviar_mensagem_anonima(client, canal, texto):
    for tentativa in range(3):  # Tentar até 3 vezes
        try:
            await client.send_message(chat_id=canal, text=texto)
            return True
        except Exception as e:
            logging.error(f"Tentativa {tentativa + 1} falhou: {e}")
            await asyncio.sleep(2)
    return False

# Comando /start
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    buttons = [
        [InlineKeyboardButton("ℹ️ Como usar", callback_data="help")],
        [InlineKeyboardButton("👨‍💻 Criador", url="https://t.me/seu_usuario_aqui"),
         InlineKeyboardButton("🛠️ Dev", url="https://t.me/lndescritivel")]
    ]
    await message.reply(
        "🤖 Olá! Bem-vindo ao bot de mensagens anônimas!\n"
        "Envie qualquer mensagem aqui e ela será enviada anonimamente para o canal configurado.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Callback dos botões
@bot.on_callback_query()
async def callback_query_handler(client, callback_query):
    if callback_query.data == "help":
        await callback_query.message.edit(
            "ℹ️ **Como usar o bot de mensagens anônimas:**\n\n"
            "1. Escreva sua mensagem diretamente no chat com o bot.\n"
            "2. O bot enviará sua mensagem anonimamente para o canal.\n\n"
            "⚠️ **Nota:** Não envie informações pessoais para manter o anonimato."
        )

# Recebendo mensagens do usuário
@bot.on_message(filters.private & ~filters.command(["start", "help"]))
async def handle_anonymous_message(client, message):
    if message.text:
        texto = message.text.strip()
        if len(texto) < 5:  # Validação para mensagens curtas
            await message.reply("❌ A mensagem deve conter pelo menos 5 caracteres.")
            return

        sucesso = await enviar_mensagem_anonima(
            client,
            CHANNEL_ID if CHANNEL_ID.isdigit() else CHANNEL_ID.strip(),
            f"📢 **Nova mensagem anônima:**\n\n{texto}"
        )

        if sucesso:
            await message.reply("✅ Sua mensagem anônima foi enviada com sucesso no canal!")
        else:
            await message.reply("❌ Ocorreu um erro ao enviar sua mensagem. Por favor, tente novamente mais tarde.")
    else:
        await message.reply("❌ Apenas mensagens de texto são suportadas no momento.")

# Iniciar o bot com tratamento de exceções
if __name__ == "__main__":
    try:
        print("Bot iniciado...")
        bot.run()
    except Exception as e:
        logging.critical(f"Ocorreu um erro crítico: {e}")
