from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""⎉︙مرحـباً بـك عزيـزي  {msg.from_user.mention} فـي بـوت اسـتـخـراج الـجـلـسـات لسـورس المطور زين 
⎉︙يمكنك استخراج الجلسات الـتالية
⎉︙بايروجرام v1 للميوزك والتليثون الإصدار القديم
⎉︙بايروجرام v2 للميوزك والتليثون الاصدار الجديد
⎉︙تريمكس (تليثون)  للحسابات & للبوتات

⎉︙بواسطـة : [ ❝ 𝗦𝗼𝘂𝗿𝗰𝗲➠𝗩𝗥 ❞ ](t.me/D_Z_J_N) """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="‹ بـدء إسـتـخـراج جـلـسـة ›", callback_data="generate")
                ],
                [
                    InlineKeyboardButton("𝙈𝙔➠𝙒𝙊𝙍𝙇𝘿", url="https://t.me/Jecthon"),
                    InlineKeyboardButton("𓏺𝗦𝗼𝘂𝗿𝗰𝗲➠𝗩𝗥 ", url="https://t.me/Jaithon")
                ],
                [
                    InlineKeyboardButton("𓏺❝ 𝘿𝙑➠𝗩𝗥 ❞", user_id=5529899678)
                ]
            ]
        ),
        disable_web_page_preview=True,
    )
