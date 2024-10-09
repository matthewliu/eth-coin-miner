import argparse
import asyncio
from util import telegram_wrapper
from config import constants

async def send_telegram_message(message_type, content, chat_id=None, caption=None, parse_mode=None):
    if chat_id is None:
        chat_id = constants.TELEGRAM_ADMIN_CHAT_ID

    if message_type == 'text':
        await telegram_wrapper.send_text(chat_id, content, parse_mode=parse_mode)
    elif message_type == 'photo':
        await telegram_wrapper.send_photo(chat_id, content, caption=caption)
    elif message_type == 'document':
        await telegram_wrapper.send_document(chat_id, content, caption=caption)
    elif message_type == 'sticker':
        await telegram_wrapper.send_sticker(chat_id, content)
    else:
        print(f"Unsupported message type: {message_type}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send a Telegram message for testing purposes.')
    parser.add_argument('message_type', choices=['text', 'photo', 'document', 'sticker'], help='Type of message to send')
    parser.add_argument('content', help='Content of the message (text, file path, or sticker ID)')
    parser.add_argument('--chat_id', help='Chat ID to send the message to (default: TELEGRAM_ADMIN_CHAT_ID)')
    parser.add_argument('--caption', help='Caption for photo or document')
    parser.add_argument('--parse_mode', choices=['HTML', 'Markdown'], help='Parse mode for text messages')

    args = parser.parse_args()

    asyncio.run(send_telegram_message(
        args.message_type,
        args.content,
        chat_id=args.chat_id,
        caption=args.caption,
        parse_mode=args.parse_mode
    ))
