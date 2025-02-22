from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
import asyncio
import aiohttp
from django.conf import settings

@receiver(post_save, sender=Task)
def notify_users_about_task(sender, instance, created, **kwargs):
    if created:
        users = User.objects.filter(
            mahalla__in=instance.mahallas.all(),
            job_title__in=instance.job_titles.all()
        )
        
        text = (
            f"🆕 Yangi topshiriq!\n\n"
            f"📌 {instance.title}\n"
            f"📝 {instance.description}\n"
            f"🕒 Muddati: {instance.start_date.strftime('%d.%m.%Y %H:%M')} - "
            f"{instance.end_date.strftime('%d.%m.%Y %H:%M')}\n\n"
            f"Batafsil ma'lumot uchun /tasks buyrug'ini yuboring."
        )
        
        for user in users:
            if user.telegram_id:
                asyncio.run(send_telegram_message(user.telegram_id, text))

async def send_telegram_message(chat_id, text):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    async with aiohttp.ClientSession() as session:
        try:
            await session.post(url, json={
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'HTML'
            })
        except Exception as e:
            print(f"Error sending notification: {e}")