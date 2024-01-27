import time
import os
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asyncio import sleep
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from info import *  # Consider providing details of this file's contents
from plugins.Rename.r_utils import progress_message, humanbytes

DOWNLOAD_LOCATION = "./DOWNLOADS"

@Client.on_message(filters.private & filters.command("rename"))
async def rename_file(bot, msg):
    reply = msg.reply_to_message
    if len(msg.command) < 2 or not reply:
        return await msg.reply_text("Please Reply To An File or video or audio With filename + .extension eg:-(`.mkv` or `.mp4` or `.zip`)")

    media = reply.document or reply.audio or reply.video
    if not media:
        await msg.reply_text("Please Reply To An File or video or audio With filename + .extension eg:-(`.mkv` or `.mp4` or `.zip`)")

    og_media = getattr(reply, reply.media.value)
    new_name = msg.text.split(" ", 1)[1]

    sts = await msg.reply_text("Trying to Downloading.....⚡")
    c_time = time.time()
    downloaded = await reply.download(file_name=new_name, progress=progress_message, progress_args=("Download Started...⚡️", sts, c_time))
    filesize = humanbytes(og_media.file_size)

    c_caption = await db.get_caption(update.message.chat.id)  # Assuming `db` is defined elsewhere
    c_thumb = await db.get_thumbnail(update.message.chat)

    if c_caption:
        try:
            caption = c_caption.format(filename=new_filename, filesize=humanbytes(media.file_size), duration=convert(duration))  # Assuming `convert` is defined
        except Exception as e:
            return await sts.edit(text=f"Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ Exᴄᴇᴩᴛ Kᴇyᴡᴏʀᴅ Aʀɢᴜᴍᴇɴᴛ ●> ({e})")
    else:
        caption = f"**{new_filename}**"

    if c_thumb:
        try:
            ph_path = await bot.download_media(c_thumb)
            Image.open(ph_path).convert("RGB").save(ph_path)
            img = Image.open(ph_path)
            img.resize((320, 320)).save(ph_path, "JPEG")
        except Exception as e:
            return await message.reply_text(f"error in thumbanil({e})") 

    await sts.edit("Trying to Uploading...⚡")
    c_time = time.time()
    try:
        await bot.send_document(msg.chat.id, document=downloaded, thumb=ph_path, caption=caption, progress=progress_message, progress_args=("Uploade Started.....", sts, c_time))
    except Exception as e:
        return await sts.edit(f"Error {e}")

    try:
        if ph_path:
            os.remove(ph_path)
        os.remove(downloaded)
    except:
        pass

    await sts.delete()
