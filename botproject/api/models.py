from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

def validate_jshir(value):
    if not value.isdigit() or len(value) != 14:
        raise ValidationError('JSHIR 14 ta raqamdan iborat bo\'lishi kerak')

class Mahalla(models.Model):
    name = models.CharField("Nomi", max_length=255, unique=True)
    created_at = models.DateTimeField("Yaratilgan vaqti", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Mahalla"
        verbose_name_plural = "Mahallalar"

class JobTitle(models.Model):
    title = models.CharField("Lavozim nomi", max_length=255, unique=True)
    created_at = models.DateTimeField("Yaratilgan vaqti", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Lavozim"
        verbose_name_plural = "Lavozimlar"

class User(models.Model):
    telegram_id = models.BigIntegerField("Telegram ID", unique=True, null=True, blank=True)
    username = models.CharField("Telegram username", max_length=255, null=True, blank=True)
    phone_number = models.CharField("Telefon raqami", max_length=15, unique=True)
    full_name = models.CharField("To'liq ismi", max_length=255)
    jshir = models.CharField("JSHIR", max_length=14, unique=True, validators=[validate_jshir])
    job_title = models.ForeignKey(JobTitle, verbose_name="Lavozimi", on_delete=models.PROTECT)
    mahalla = models.ForeignKey(Mahalla, verbose_name="Mahallasi", on_delete=models.PROTECT)
    is_admin = models.BooleanField("Admin huquqi", default=False)
    created_at = models.DateTimeField("Yaratilgan vaqti", auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.mahalla}"

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

class Task(models.Model):
    title = models.CharField("Sarlavha", max_length=255)
    description = models.TextField("Tavsif")
    file = models.FileField("Fayl", upload_to='tasks/files/', null=True, blank=True)
    start_date = models.DateTimeField("Boshlanish vaqti")
    end_date = models.DateTimeField("Tugash vaqti")
    mahallas = models.ManyToManyField(Mahalla, verbose_name="Mahallalar")
    job_titles = models.ManyToManyField(JobTitle, verbose_name="Lavozimlar")
    created_at = models.DateTimeField("Yaratilgan vaqti", auto_now_add=True)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Tugash vaqti boshlanish vaqtidan oldin bo'lishi mumkin emas")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Topshiriq"
        verbose_name_plural = "Topshiriqlar"

class TaskProgress(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('in_progress', 'Jarayonda'),
        ('completed', 'Bajarildi'),
        ('failed', 'Bajarilmadi'),
    ]

    task = models.ForeignKey(Task, verbose_name="Topshiriq", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Foydalanuvchi", on_delete=models.CASCADE)
    description = models.TextField("Izoh")
    status = models.CharField("Holat", max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_mark = models.IntegerField("Admin bahosi", null=True, blank=True)
    admin_comment = models.TextField("Admin izohi", null=True, blank=True)
    created_at = models.DateTimeField("Yaratilgan vaqti", auto_now_add=True)
    updated_at = models.DateTimeField("Yangilangan vaqti", auto_now=True)

    def __str__(self):
        return f"{self.task} - {self.user}"

    class Meta:
        verbose_name = "Topshiriq jarayoni"
        verbose_name_plural = "Topshiriq jarayonlari"

class TaskProgressImage(models.Model):
    progress = models.ForeignKey(TaskProgress, on_delete=models.CASCADE)
    image = models.ImageField("Rasm", upload_to='tasks/progress/')
    created_at = models.DateTimeField("Yuklangan vaqti", auto_now_add=True)

    class Meta:
        verbose_name = "Topshiriq rasmi"
        verbose_name_plural = "Topshiriq rasmlari"

class TaskProgressFile(models.Model):
    progress = models.ForeignKey(TaskProgress, on_delete=models.CASCADE)
    file = models.FileField("Fayl", upload_to='tasks/progress/files/')
    created_at = models.DateTimeField("Yuklangan vaqti", auto_now_add=True)

    class Meta:
        verbose_name = "Topshiriq fayli"
        verbose_name_plural = "Topshiriq fayllari"