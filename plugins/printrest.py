from pyrogram import Client, filters
import requests
import os

@Client.on_message(filters.command("download"))
async def download(client, message):
 try:
    url = message.text.split()[1]
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open('image.jpg', 'wb') as f:
            f.write(response.content)

        await message.reply_photo(photo='image.jpg')
        os.remove('image.jpg')
    else:
        await message.reply_text('Failed to download image.')
 except Exception as e:
        await message.reply_text(f"{e}")

