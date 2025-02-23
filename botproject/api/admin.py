from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(Mahalla)
class MahallaAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    ordering = ('title',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'jshir', 'get_job_title', 'get_mahalla', 'created_at')
    list_filter = ('job_title', 'mahalla')
    search_fields = ('full_name', 'phone_number', 'jshir', 'telegram_id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def get_job_title(self, obj):
        return obj.job_title.title if obj.job_title else '-'
    get_job_title.short_description = 'Lavozim'
    get_job_title.admin_order_field = 'job_title__title'

    def get_mahalla(self, obj):
        return obj.mahalla.name if obj.mahalla else '-'
    get_mahalla.short_description = 'Mahalla'
    get_mahalla.admin_order_field = 'mahalla__name'

class TaskProgressImageInline(admin.TabularInline):
    model = TaskProgressImage
    extra = 0
    readonly_fields = ('created_at',)

class TaskProgressFileInline(admin.TabularInline):
    model = TaskProgressFile
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'get_mahallas', 'get_job_titles', 'created_at')
    list_filter = ('mahallas', 'job_titles', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    filter_horizontal = ('mahallas', 'job_titles')
    readonly_fields = ('created_at',)

    def get_mahallas(self, obj):
        return ", ".join([m.name for m in obj.mahallas.all()])
    get_mahallas.short_description = 'Mahallalar'

    def get_job_titles(self, obj):
        return ", ".join([j.title for j in obj.job_titles.all()])
    get_job_titles.short_description = 'Lavozimlar'

@admin.register(TaskProgress)
class TaskProgressAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'status', 'admin_mark', 'created_at', 'updated_at')
    list_filter = ('status', 'task', 'user__mahalla')
    search_fields = ('task__title', 'user__full_name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TaskProgressImageInline, TaskProgressFileInline]

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('task', 'user', 'description', 'status')
        }),
        ('Admin baholash', {
            'fields': ('admin_mark', 'admin_comment')
        }),
        ('Vaqtlar', {
            'fields': ('created_at', 'updated_at')
        }),
    )