# Generated by Django 5.1.6 on 2025-02-22 19:11

import api.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Lavozim nomi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')),
            ],
            options={
                'verbose_name': 'Lavozim',
                'verbose_name_plural': 'Lavozimlar',
            },
        ),
        migrations.CreateModel(
            name='Mahalla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Nomi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')),
            ],
            options={
                'verbose_name': 'Mahalla',
                'verbose_name_plural': 'Mahallalar',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Sarlavha')),
                ('description', models.TextField(verbose_name='Tavsif')),
                ('file', models.FileField(blank=True, null=True, upload_to='tasks/files/', verbose_name='Fayl')),
                ('start_date', models.DateTimeField(verbose_name='Boshlanish vaqti')),
                ('end_date', models.DateTimeField(verbose_name='Tugash vaqti')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')),
                ('job_titles', models.ManyToManyField(to='api.jobtitle', verbose_name='Lavozimlar')),
                ('mahallas', models.ManyToManyField(to='api.mahalla', verbose_name='Mahallalar')),
            ],
            options={
                'verbose_name': 'Topshiriq',
                'verbose_name_plural': 'Topshiriqlar',
            },
        ),
        migrations.CreateModel(
            name='TaskProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Izoh')),
                ('status', models.CharField(choices=[('pending', 'Kutilmoqda'), ('in_progress', 'Jarayonda'), ('completed', 'Bajarildi'), ('failed', 'Bajarilmadi')], default='pending', max_length=20, verbose_name='Holat')),
                ('admin_mark', models.IntegerField(blank=True, null=True, verbose_name='Admin bahosi')),
                ('admin_comment', models.TextField(blank=True, null=True, verbose_name='Admin izohi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqti')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.task', verbose_name='Topshiriq')),
            ],
            options={
                'verbose_name': 'Topshiriq jarayoni',
                'verbose_name_plural': 'Topshiriq jarayonlari',
            },
        ),
        migrations.CreateModel(
            name='TaskProgressFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='tasks/progress/files/', verbose_name='Fayl')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yuklangan vaqti')),
                ('progress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.taskprogress')),
            ],
            options={
                'verbose_name': 'Topshiriq fayli',
                'verbose_name_plural': 'Topshiriq fayllari',
            },
        ),
        migrations.CreateModel(
            name='TaskProgressImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='tasks/progress/', verbose_name='Rasm')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yuklangan vaqti')),
                ('progress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.taskprogress')),
            ],
            options={
                'verbose_name': 'Topshiriq rasmi',
                'verbose_name_plural': 'Topshiriq rasmlari',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField(blank=True, null=True, unique=True, verbose_name='Telegram ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='Telegram username')),
                ('phone_number', models.CharField(max_length=15, unique=True, verbose_name='Telefon raqami')),
                ('full_name', models.CharField(max_length=255, verbose_name="To'liq ismi")),
                ('jshir', models.CharField(max_length=14, unique=True, validators=[api.models.validate_jshir], verbose_name='JSHIR')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Admin huquqi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')),
                ('job_title', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.jobtitle', verbose_name='Lavozimi')),
                ('mahalla', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.mahalla', verbose_name='Mahallasi')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi',
                'verbose_name_plural': 'Foydalanuvchilar',
            },
        ),
        migrations.DeleteModel(
            name='BotUser',
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
        migrations.AddField(
            model_name='taskprogress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user', verbose_name='Foydalanuvchi'),
        ),
    ]
