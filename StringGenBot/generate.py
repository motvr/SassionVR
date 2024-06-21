from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from pyrogram1 import Client as Client1
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from pyrogram1.errors import (
    ApiIdInvalid as ApiIdInvalid1,
    PhoneNumberInvalid as PhoneNumberInvalid1,
    PhoneCodeInvalid as PhoneCodeInvalid1,
    PhoneCodeExpired as PhoneCodeExpired1,
    SessionPasswordNeeded as SessionPasswordNeeded1,
    PasswordHashInvalid as PasswordHashInvalid1
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import config



ask_ques = "**⎉︙اذا كنت تريد تنـصيـب مـيوزك إصدار قديم \n⎉︙فـاسـتـخـرج جـلـسـة بـايـروجـرام v1 \n⎉︙اذا كنت تريد تنصيب تليثون إصدار قديم\n⎉︙فـاسـتـخـرج جـلـسـة تـليثون \n⎉︙واذا كـنـت تـريـد تنـصـيب ميوزك او تليثون إصدار جديد \n⎉︙فـاسـتـخـرج جـلـسـة بايروجرام v2 \n⎉︙يوجد أيضاً استخراج جـلسـات للـبوتات في الخيارات :**"


buttons_ques = [
    [
        InlineKeyboardButton("‹ بـايروجرام v1 ›", callback_data="pyrogram1"),
        InlineKeyboardButton("‹ بـايروجرام v2 ›", callback_data="pyrogram"),
    ],
    [
        InlineKeyboardButton("‹ تـلـيـثـون ›", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("‹ بـايروجرام بوت ›", callback_data="pyrogram_bot"),
        InlineKeyboardButton("‹ تـلـيثون بوت ›", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="‹ بـدء إسـتـخـراج جـلـسـة ›", callback_data="generate")
    ]
]




@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, old_pyro: bool = False, is_bot: bool = False):
    if telethon:
        ty = "تـلـيـثـون"
    else:
        ty = "بـايـروجـرام"
        if not old_pyro:
            ty += " ᴠ2"
    if is_bot:
        ty += " بـوت"
    await msg.reply(f"⎉︙إنـشـاء جـلسـة **{ty}** ...")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "⎉︙أرسـل الان ايبي ايدي API_ID\n\n⎉︙اضـغـط /skip لـلـتـخـطـي", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("⎉︙يجب ان يكون الايبي ايدي عدداً صحيحاً \n⎉︙يرجى المحـاولة مـرة أخـرى...", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "⎉︙ارسـل الان ايبي هاش API_HASH", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "⎉︙ارسـل الان رقمك مع رمـز دولتك\n⎉︙مثـال : +201023456789"
    else:
        t = "⎉︙ارسل الان توكن بوتك BOT_TOKEN\n⎉︙مثل : `5432198765:abcdanonymousterabaaplol`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("⎉︙يـتـم إرسـال رمـز إلـيـك الآن إنتظر قليلاً...")
    else:
        await msg.reply("⎉︙محاولة تسجيل الدخول عبر توكن البوت...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        await msg.reply("⎉︙لا يتطابق الايبي ايدي و الايبي هاش ❌\n⎉︙مع نظام تطبيقات تيليجرام 🌐\n⎉︙يرجى المحاولة مـرة أخـرى...", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        await msg.reply("⎉︙لا ينتمي رقم الهاتف الذي أرسلتة ❌\n⎉︙إلى اي حساب علي التيليجرام 🌐\n⎉︙يرجى المحاولة مـرة أخـرى...", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "⎉︙ارسل الان كود االتحقق (الرمز) الذي تم ارسالة لك\n⎉︙ارسل كود التحقق مثل: 1 2 3 4 5\n⎉︙مع وضع فراغ (مسافه) بين الارقام...", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("⎉︙تم انتهاء وقت انشاء الجلسه\n⎉︙يرجى محاولة انشاء الجلسة من البداية.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
            await msg.reply("⎉︙كود التحقق الذي ارسلته غير صحيح\n⎉︙يرجى التأكد منه... ", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
            await msg.reply("⎉︙انتهت صلاحية  كود التحقق الذي أرسلته\n⎉︙يرجى المحاولة مرة أخرى... ", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
            try:
                two_step_msg = await bot.ask(user_id, "⎉︙يرجي إرسال كلمة مرور التحقق بخطوتين (المصادقة الثنائية) للمتابعة", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("⎉︙تم انتهاء وقت الجلسه 5 دقائق يرجى اعاده استخراج الجلسه من البدايه.", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
                await two_step_msg.reply("⎉︙كلمة المرور التي أرسلتها غير صحيحة\n⎉︙يرجى التأكد منها والمحاوله مـرة أخـرى...", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**⎉︙هذه هي جلسة {ty} الخاصة بك** \n\n`{string_session}` \n\n⎉︙**تم استخراج الجلسة بواسطة سورس زين جيمثون @Jaithon \n⎉︙لا تقوم بمشاركة الجلسة مع الآخرين لـعدم اختراق حسابك الشخصي او حذفه\n⎉: ولا تنسى الانضمام لـقناه المطور زين @Jecthon ♥"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, " تم انشاء جلستك بنجاح ✅ \nيرجى التحقق من رسائلك المحفوظة للحصول عليها !\n⎉︙**تم الاستخراج بواسطة سورس زين جيمثون**".format("تـيـلـثـون" if telethon else "بـايـروجـرام"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("⎉︙**تم إلغاء عملية إنشاء الجلسة !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("⎉︙** تم بنجاح إعادة تشغيل هذا الروبوت !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("⎉︙**تم إلغاء عملية إنشاء الجلسة !**", quote=True)
        return True
    else:
        return False
