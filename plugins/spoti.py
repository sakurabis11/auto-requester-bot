import asyncio
import os
import pytube
import ffmpeg
from pyrogram import Client, filters

def get_song_details(spotify_link):
    try:
        yt = pytube.YouTube(spotify_link)

        # Check song availability
        if not yt.is_playable():
            raise Exception(f"❌ Song unavailable: {yt.title} by {yt.author}")

        song_title = yt.title
        song_artist = yt.author

        return song_title, song_artist

    except Exception as e:
        raise e

def download_song(song_title, song_artist, spotify_link):
    try:
        # Download the song
        video = pytube.YouTube(spotify_link).streams.first()
        video.download(filename=f"{song_title}.mp4")

        # Convert MP4 to MP3
        os.system(f"ffmpeg -i {song_title}.mp4 -q:a 0 -b:a 192k {song_title}.mp3")

        # Delete the temporary MP4 file
        os.remove(f"{song_title}.mp4")

        return f"{song_title}.mp3"

    except Exception as e:
        raise e

@Client.on_message(filters.command(["download"]))
async def download_song_handler(client, message):
    if message.chat.id != message.from_user.id:
        return

    if message.reply_to_message is None or message.reply_to_message.text is None:
        await message.reply_text("Please reply to a message containing a Spotify song link.")
        return

    spotify_link = message.reply_to_message.text

    try:
        song_title, song_artist = get_song_details(spotify_link)

        await message.reply_text(f"Downloading: {song_title} by {song_artist}")

        downloaded_file_path = await download_song(song_title, song_artist, spotify_link)

        # Send the downloaded MP3 file to the user
        await message.reply_document(downloaded_file_path)

        # Delete the temporary MP3 file
        os.remove(downloaded_file_path)

        await message.reply_text(f"✅ Song downloaded: {song_title} by {song_artist}")

    except Exception as e:
        await message.reply_text(f"❌ Error downloading song: {e}")
