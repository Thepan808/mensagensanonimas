import os
import logging
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do bot
try:
    API_ID = int(os.getenv("API_ID"))  # Certifique-se de que está como inteiro
except ValueError:
    raise ValueError("O valor de API_ID deve ser um número inteiro válido.")
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
            "🛸 **Farpas Área 52: treta controlada, zoeira autorizada!**\n\n"
            "🎭 Entre no clima da provocação divertida com estilo e criatividade. Aqui, as farpas voam como discos voadores — mas sempre com respeito.\n\n"
            "⚠️ Sem ofensas pessoais, sem baixaria. Brinque, provoque, mas lembre-se: até os ETs têm limite! 👽"
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
            await client.send_message(
                chat_id=CHANNEL_ID,
                text=f"📢 **Nova mensagem anônima:**\n\n{message.text}"
            )

            # Resposta simples de sucesso
            await message.reply("✅ Sua mensagem anônima foi enviada com sucesso no canal!")
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem: {e}")
            await message.reply("❌ Ocorreu um erro ao enviar sua mensagem. Por favor, verifique as configurações do bot ou tente novamente mais tarde.")
    else:
        await message.reply("❌ Apenas mensagens de texto são suportadas no momento.")

# Iniciar o bot
if __name__ == "__main__":
    print("Bot iniciado...")
    bot.run()