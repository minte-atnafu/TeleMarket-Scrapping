from telethon import TelegramClient
import csv
import os
import asyncio
import random
from dotenv import load_dotenv
from telethon.errors.rpcerrorlist import UserDeactivatedBanError, FloodWaitError

# Load environment variables
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Rate limit and delay configuration
REQUEST_DELAY = 2  # Delay between messages (seconds)
CHANNEL_DELAY_RANGE = (300, 600)  # Random delay between channels (5 to 10 minutes)

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title  # Extract the channel's title
        async for message in client.iter_messages(entity, limit=1000):
            await asyncio.sleep(REQUEST_DELAY)  # Delay between processing each message
            
            media_path = None
            if message.media and hasattr(message.media, 'photo'):
                # Create a unique filename for the photo
                filename = f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                # Download the media to the specified directory if it's a photo
                await client.download_media(message.media, media_path)
            
            # Write the channel title along with other data
            writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])
        print(f"Finished scraping {channel_username}.")
    except UserDeactivatedBanError:
        # Handle the case where the account has been banned or deactivated
        print(f"Error: The user for {channel_username} has been deactivated or banned. Skipping this channel.")
    except FloodWaitError as e:
        # Handle flood wait errors by pausing for the required time
        print(f"FloodWaitError: Waiting for {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        # Handle any other exceptions
        print(f"Error occurred while scraping {channel_username}: {e}")

# Initialize the client once
client = TelegramClient('scraping_session', api_id, api_hash)

# Main function to scrape channels sequentially
async def main():
    await client.start()
    
    # Create a directory for media files
    media_dir = 'photos'
    os.makedirs(media_dir, exist_ok=True)

    # Open the CSV file and prepare the writer
    with open('telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])  # Include channel title in the header
        
        # List of channels to scrape
        channels = [
            '@ethio_brand_collection',  # Existing channel
            '@samcomptech',
            '@phonehub27'
        ]
        
        # Iterate over channels and scrape data sequentially
        for channel in channels:
            print(f"Starting to scrape {channel}...")
            await scrape_channel(client, channel, writer, media_dir)
            delay = random.randint(*CHANNEL_DELAY_RANGE)
            print(f"Waiting for {delay} seconds before scraping the next channel...")
            await asyncio.sleep(delay)  # Random delay between channel scrapes

# Run the main function
with client:
    client.loop.run_until_complete(main())
