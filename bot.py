from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Configurações do bot
API_ID = "sua_api_id"
API_HASH = "sua_api_hash"
BOT_TOKEN = "seu_token_do_bot"
CHANNEL_ID = -1001234567890  # Substitua pelo ID do canal onde as mensagens serão enviadas
CANAL_PUBLICO = "seu_canal_publico"  # Substitua pelo @ ou nome público do canal (sem o @, ex: "mensagensanonimas")

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
         InlineKeyboardButton("🛠️ Dev", url="https://t.me/seu_usuario_aqui")]
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
            await message.reply("❌ Ocorreu um erro ao enviar sua mensagem. Tente novamente mais tarde.")
            print(f"Erro ao enviar mensagem: {e}")
    else:
        await message.reply("❌ Apenas mensagens de texto são suportadas no momento.")

# Iniciar o bot
if __name__ == "__main__":
    print("Bot iniciado...")
    bot.run()
