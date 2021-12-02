import os
import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from .commands import start, BATCH
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
DB_CHANNEL_ID = os.environ.get("DB_CHANNEL_ID")
OWNER_ID = os.environ.get("OWNER_ID")


@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m):
    await m.answer()

    # help text
    help_text = """**You need Help?? Contact @groupdc **
"""

    # creating buttons
    buttons = [
        [
            InlineKeyboardButton('🏡Home🏡', callback_data='home'),
            InlineKeyboardButton('😎About😎', callback_data='about')
        ],
        [
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]

    # editing as help message
    await m.message.edit(
        text=help_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(filters.regex('^close$'))
async def close_cb(c, m):
    await m.message.delete()
    await m.message.reply_to_message.delete()


@Client.on_callback_query(filters.regex('^about$'))
async def about_cb(c, m):
    await m.answer()
    owner = await c.get_users(int(OWNER_ID))
    bot = await c.get_me()

    # about text
    about_text = f"""--**My Details:**--

🤖 I am : {bot.mention(style='md')}
    
📝 Python: [Python 3](https://www.python.org/)

🤹 GitHub: [Pyrogram](https://github.com/pyrogram/pyrogram)

👨‍💻 Owner: {owner.mention(style='md')}

📢 Updates: [Group Dc Bots](https://t.me/Groupdcbots)

👥 Support: [Group Dc](https://t.me/groupdc)

🌐 Source code: [Press Me 🥰](https://github.com/selfie-bd)
"""

    # creating buttons
    buttons = [
        [
            InlineKeyboardButton('🏡Home🏡', callback_data='home'),
            InlineKeyboardButton('⚠️Help⚠️', callback_data='help')
        ],
        [
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]

    # editing message
    await m.message.edit(
        text=about_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex('^home$'))
async def home_cb(c, m):
    await m.answer()
    await start(c, m, cb=True)


@Client.on_callback_query(filters.regex('^done$'))
async def done_cb(c, m):
    BATCH.remove(m.from_user.id)
    c.cancel_listener(m.from_user.id)
    await m.message.delete()


@Client.on_callback_query(filters.regex('^delete'))
async def delete_cb(c, m):
    await m.answer()
    cmd, msg_id = m.data.split("+")
    chat_id = m.from_user.id if not DB_CHANNEL_ID else int(DB_CHANNEL_ID)
    message = await c.get_messages(chat_id, int(msg_id))
    await message.delete()
    await m.message.edit("Deleted files successfully 👨‍✈️")
