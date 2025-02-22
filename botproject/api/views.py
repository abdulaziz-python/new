from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.http import HttpResponse
import pandas as pd
import io
from .models import *
from .serializers import *

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_user(request):
    phone = request.data.get('phone')
    jshir = request.data.get('jshir')
    
    try:
        user = User.objects.get(phone_number=phone, jshir=jshir)
        return Response({
            'status': 'success',
            'user': {
                'id': user.id,
                'full_name': user.full_name,
                'job_title': user.job_title.title,
                'mahalla': user.mahalla.name,
                'is_admin': user.is_admin
            }
        })
    except User.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Foydalanuvchi topilmadi'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_info(request):
    telegram_id = request.GET.get('telegram_id')
    try:
        user = User.objects.get(telegram_id=telegram_id)
        serializer = UserSerializer(user)
        return Response({
            'status': 'success',
            'user': serializer.data
        })
    except User.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Foydalanuvchi topilmadi'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_active_tasks(request):
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(telegram_id=user_id)
        now = timezone.now()
        tasks = Task.objects.filter(
            mahallas=user.mahalla,
            job_titles=user.job_title,
            end_date__gte=now
        ).order_by('end_date')
        
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
        return Response({
            'status': 'success',
            'tasks': serializer.data
        })
    except User.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Foydalanuvchi topilmadi'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_progress(request):
    task_id = request.data.get('task_id')
    user_id = request.data.get('user_id')
    description = request.data.get('description')
    
    try:
        task = Task.objects.get(id=task_id)
        user = User.objects.get(telegram_id=user_id)
        
        progress = TaskProgress.objects.create(
            task=task,
            user=user,
            description=description,
            status='in_progress'
        )
        
        # Handle images
        images = request.FILES.getlist('images')
        for image in images:
            TaskProgressImage.objects.create(
                progress=progress,
                image=image
            )
        
        # Handle files
        files = request.FILES.getlist('files')
        for file in files:
            TaskProgressFile.objects.create(
                progress=progress,
                file=file
            )
        
        return Response({'status': 'success'})
    except (Task.DoesNotExist, User.DoesNotExist):
        return Response({
            'status': 'error',
            'message': 'Topshiriq yoki foydalanuvchi topilmadi'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_task_progress(request, task_id):
    try:
        progress = TaskProgress.objects.filter(task_id=task_id)
        serializer = TaskProgressSerializer(progress, many=True, context={'request': request})
        return Response({
            'status': 'success',
            'progress': serializer.data
        })
    except TaskProgress.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Topshiriq jarayoni topilmadi'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def mark_progress(request, progress_id):
    try:
        progress = TaskProgress.objects.get(id=progress_id)
        progress.admin_mark = request.data.get('mark')
        progress.admin_comment = request.data.get('comment')
        progress.status = 'completed' if progress.admin_mark >= 5 else 'failed'
        progress.save()
        
        return Response({'status': 'success'})
    except TaskProgress.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Topshiriq jarayoni topilmadi'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def export_users(request):
    users = User.objects.all()
    
    # Create DataFrame
    data = {
        'F.I.O': [user.full_name for user in users],
        'Telefon': [user.phone_number for user in users],
        'JSHIR': [user.jshir for user in users],
        'Lavozim': [user.job_title.title for user in users],
        'Mahalla': [user.mahalla.name for user in users],
        'Admin': [user.is_admin for user in users],
        'Yaratilgan sana': [user.created_at for user in users],
    }
    
    df = pd.DataFrame(data)
    
    # Create Excel file
    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)
    
    response = HttpResponse(
        excel_file.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=users.xlsx'
    
    return response