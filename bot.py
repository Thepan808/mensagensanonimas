import os
import logging
import psycopg2
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do bot
try:
    API_ID = int(os.getenv("API_ID"))  # Converter API_ID para inteiro
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CANAL_PUBLICO = os.getenv("CANAL_PUBLICO")  # Canal público em formato @nome_do_canal
    DATABASE_URL = os.getenv("DATABASE_URL")  # URL da conexão PostgreSQL

    if not all([API_ID, API_HASH, BOT_TOKEN, CANAL_PUBLICO, DATABASE_URL]):
        raise ValueError("Certifique-se de que todas as variáveis de ambiente estão configuradas no arquivo .env.")
    if not CANAL_PUBLICO.startswith("@"):
        raise ValueError("O valor de CANAL_PUBLICO deve começar com '@'.")
except Exception as e:
    raise SystemExit(f"Erro na configuração do bot: {e}")

# Configuração do logger para registrar erros
logging.basicConfig(
    level=logging.ERROR,
    filename="bot_errors.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Inicialização do bot
bot = Client(
    "anon_messages_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Variável global para controlar o estado do bot
bot_status = False  # True para ativo, False para inativo

# Seu ID de usuário como dono do bot
OWNER_ID = 737737727  # Substitua pelo seu ID

# Conexão com o banco de dados PostgreSQL
try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL UNIQUE,
            is_admin BOOLEAN DEFAULT FALSE
        );
    """)
    conn.commit()
except Exception as e:
    raise SystemExit(f"Erro ao conectar ao banco de dados: {e}")

# Função para verificar se um usuário é administrador
def is_admin(user_id):
    try:
        # O dono do bot é sempre considerado administrador
        if user_id == OWNER_ID:
            return True
        cursor.execute("SELECT is_admin FROM users WHERE user_id = %s;", (user_id,))
        result = cursor.fetchone()
        return result is not None and result[0]
    except Exception as e:
        logging.error(f"Erro ao verificar administrador: {e}")
        return False

# Comando /on - Ativar o bot
@bot.on_message(filters.command("on"))
async def activate_bot(client, message):
    global bot_status
    if is_admin(message.from_user.id):
        bot_status = True
        await message.reply("✅ O bot foi ativado para todos os usuários.")
        
        try:
            # Enviar uma mensagem no canal configurado informando que o bot está ativo
            await client.send_message(
                chat_id=CANAL_PUBLICO,
                text="✅ **O bot está agora ativo!**\n\nEnvie suas mensagens anônimas diretamente para este canal."
            )
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem de ativação para o canal: {e}")
    else:
        await message.reply("⛔ Você não tem permissão para usar este comando.")

# Comando /off - Desativar o bot
@bot.on_message(filters.command("off"))
async def deactivate_bot(client, message):
    global bot_status
    if is_admin(message.from_user.id):
        bot_status = False
        await message.reply(
            "⛔ O bot foi desativado para todos os usuários.\n\n"
            "Por favor, aguarde o aviso no canal para saber quando ele estará disponível novamente.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔗 Acompanhe no canal", url=f"https://t.me/{CANAL_PUBLICO[1:]}")]]
            )
        )

        try:
            # Enviar uma mensagem ao canal configurado informando que o bot está inativo
            await client.send_message(
                chat_id=CANAL_PUBLICO,
                text="⛔ **O bot foi desativado.**\n\nPor favor, aguarde para novas atualizações."
            )
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem de desativação para o canal: {e}")
    else:
        await message.reply("⛔ Você não tem permissão para usar este comando.")

# Comando /start
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    user_id = message.from_user.id
    try:
        # Registrar o ID do usuário na base de dados
        cursor.execute(
            "INSERT INTO users (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING;",
            (user_id,)
        )
        conn.commit()

        # Mensagem de boas-vindas e botões
        buttons = [
            [InlineKeyboardButton("ℹ️ Como usar", callback_data="help")],
            [
                InlineKeyboardButton("👨‍💻 Criador", url="https://t.me/mulheres_apaixonadas"),
                InlineKeyboardButton("🛠️ Dev", url="https://t.me/lndescritivel")
            ]
        ]
        await message.reply(
            "🤖 Olá! Bem-vindo ao bot de mensagens anônimas!\n"
            "Envie qualquer mensagem aqui e ela será enviada anonimamente para o canal configurado.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        logging.error(f"Erro ao registrar usuário no banco de dados: {e}")
        await message.reply("❌ Ocorreu um erro ao registrar seu acesso. Tente novamente mais tarde.")

# Callback dos botões
@bot.on_callback_query()
async def callback_query_handler(client, callback_query):
    if callback_query.data == "help":
        await callback_query.message.edit(
            "ℹ️ **Como usar o bot de mensagens anônimas:**\n\n"
            "1. Escreva sua mensagem diretamente no chat com o bot.\n"
            "2. O bot enviará sua mensagem anonimamente para o canal.\n\n"
            "🛸 **zoeira autorizada!**\n\n"
            "🎭 Entre no clima da provocação divertida com estilo e criatividade. Aqui, as farpas voam como discos voadores — mas sempre com respeito.\n\n"
            "⚠️ Sem ofensas pessoais, sem baixaria. Brinque, provoque, mas lembre-se: até os ETs têm limite! 👽"
        )

# Recebendo mensagens do usuário
@bot.on_message(filters.private & ~filters.command(["start", "help", "on", "off", "add_admin"]))
async def handle_anonymous_message(client, message):
    global bot_status
    if not bot_status:
        await message.reply(
            "⚠️ O bot está indisponível no momento.\n"
            "Por favor, aguarde o aviso no canal para saber quando ele estará disponível novamente.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔗 Acompanhe no canal", url=f"https://t.me/{CANAL_PUBLICO[1:]}")]]
            )
        )
        return

    if message.text:
        try:
            # Enviando a mensagem para o canal público configurado no .env
            await client.send_message(
                chat_id=CANAL_PUBLICO,
                text=f"📢 **Nova mensagem anônima:**\n\n{message.text}"
            )

            # Confirmação de envio para o usuário
            await message.reply("✅ Sua mensagem anônima foi enviada com sucesso no canal!")
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem: {e}")
            await message.reply(
                "❌ Ocorreu um erro ao enviar sua mensagem. Por favor, tente novamente mais tarde ou verifique as configurações do bot."
            )
    else:
        await message.reply("❌ Apenas mensagens de texto são suportadas no momento.")

# Iniciar o bot
if __name__ == "__main__":
    print("Bot iniciado...")
    bot.run()
