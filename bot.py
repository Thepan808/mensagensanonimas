import os
import logging
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do bot
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Certifique-se de que o ID é um número inteiro
CANAL_PUBLICO = os.getenv("CANAL_PUBLICO")

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
    if message.text:
        if len(message.text.strip()) < 5:  # Validação para mensagens curtas
            await message.reply("❌ A mensagem deve conter pelo menos 5 caracteres.")
            return
        
        try:
            # Enviando a mensagem para o canal especificado
            sent_message = await client.send_message(
                chat_id=CHANNEL_ID,
                text=f"📢 **Nova mensagem anônima:**\n\n{message.text}"
            )

            # Gerando o link da mensagem (para canais públicos)
            if CANAL_PUBLICO:
                message_link = f"https://t.me/{CANAL_PUBLICO}/{sent_message.id}"
                await message.reply(
                    f"✅ Sua mensagem anônima foi enviada para o canal de mensagens anônimas!\n"
                    f"🔗 [Clique aqui para visualizar sua mensagem no canal]({message_link}).",
                    disable_web_page_preview=True
                )
            else:
                await message.reply("✅ Sua mensagem anônima foi enviada para o canal de mensagens anônimas!")
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem: {e}")
            await message.reply("❌ Ocorreu um erro ao enviar sua mensagem. Tente novamente mais tarde.")
    else:
        await message.reply("❌ Apenas mensagens de texto são suportadas no momento.")

# Iniciar o bot
if __name__ == "__main__":
    print("Bot iniciado...")
    bot.run()
