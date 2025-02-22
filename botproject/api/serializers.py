from rest_framework import serializers
from .models import *

class MahallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahalla
        fields = '__all__'

class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    mahalla_name = serializers.CharField(source='mahalla.name', read_only=True)
    job_title_name = serializers.CharField(source='job_title.title', read_only=True)

    class Meta:
        model = User
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    mahallas = MahallaSerializer(many=True, read_only=True)
    job_titles = JobTitleSerializer(many=True, read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_file_url(self, obj):
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None

class TaskProgressSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()

    class Meta:
        model = TaskProgress
        fields = '__all__'

    def get_images(self, obj):
        return [
            self.context['request'].build_absolute_uri(image.image.url)
            for image in obj.taskprogressimage_set.all()
        ]

    def get_files(self, obj):
        return [
            self.context['request'].build_absolute_uri(file.file.url)
            for file in obj.taskprogressfile_set.all()
        ]