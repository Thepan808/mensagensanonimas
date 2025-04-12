import os
import logging
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do bot
try:
    API_ID = int(os.getenv("API_ID"))  # Certifique-se de que está como inteiro
    CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Certifique-se de que o ID é um número inteiro
except ValueError as e:
    raise ValueError("Verifique se API_ID e CHANNEL_ID são números inteiros válidos.") from e

API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Inicializando o logger para registrar erros
logging.basicConfig(level=logging.ERROR, filename="bot_errors.log", format="%(asctime)s - %(levelname)s - %(message)s")

# Inicializando o bot
bot = Client(
    "anon_messages_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

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
    text = message.text.strip() if message.text else None

    if not text:  # Apenas verifica se a mensagem não está vazia
        await message.reply("❌ A mensagem não pode estar vazia.")
        return

    try:
        # Enviando a mensagem para o canal especificado
        await client.send_message(
            chat_id=CHANNEL_ID,
            text=f"📢 **Nova mensagem anônima:**\n\n{text}"
        )
        await message.reply("✅ Sua mensagem anônima foi enviada com sucesso no canal!")
    except RPCError as e:
        logging.error(f"Erro ao enviar mensagem (RPC): {e}")
        await message.reply("❌ Ocorreu um erro no envio. Verifique as permissões do bot no canal.")
    except Exception as e:
        logging.error(f"Erro inesperado ao enviar mensagem: {e}")
        await message.reply("❌ Ocorreu um erro inesperado. Contate o suporte ou tente novamente mais tarde.")

# Iniciar o bot
if __name__ == "__main__":
    print("Bot iniciado...")
    try:
        bot.run()
    except Exception as e:
        logging.critical(f"Erro crítico ao iniciar o bot: {e}")
        print("Erro crítico ao iniciar o bot. Verifique os logs para mais informações.")
