import os
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaDocument

# دریافت اطلاعات از Secrets
API_ID = int(os.environ['TELEGRAM_API_ID'])
API_HASH = os.environ['TELEGRAM_API_HASH']
PHONE = os.environ['TELEGRAM_PHONE']
CHANNEL_USERNAME = 'Sickmall'

# محدوده پست‌ها
START_ID = 1
END_ID = 28

def main():
    # ساخت کلاینت و اتصال
    client = TelegramClient('session', API_ID, API_HASH)
    client.start(phone=PHONE)

    # دریافت موجودیت کانال
    channel = client.get_entity(CHANNEL_USERNAME)

    # حلقه روی شناسه پیام‌ها
    for msg_id in range(START_ID, END_ID + 1):
        try:
            message = client.get_messages(channel, ids=msg_id)
            if not message:
                print(f"⚠️ پیام {msg_id} یافت نشد.")
                continue

            # بررسی اینکه آیا پیام حاوی سند صوتی است
            if isinstance(message.media, MessageMediaDocument):
                doc = message.media.document
                # بررسی اینکه فایل mp3 است (بر اساس MIME type یا پسوند)
                if doc.mime_type == 'audio/mpeg' or (doc.attributes and any(getattr(attr, 'file_name', '').endswith('.mp3') for attr in doc.attributes)):
                    file_path = os.path.join(os.getcwd(), f"{msg_id}.mp3")
                    print(f"⬇️ در حال دانلود پیام {msg_id} ...")
                    message.download_media(file=file_path)
                    print(f"✅ ذخیره شد: {file_path}")
                else:
                    print(f"⏭️ پیام {msg_id} فایل MP3 نیست.")
            else:
                print(f"⏭️ پیام {msg_id} مدیا ندارد.")
        except Exception as e:
            print(f"❌ خطا در پردازش پیام {msg_id}: {e}")

    client.disconnect()

if __name__ == '__main__':
    main()
