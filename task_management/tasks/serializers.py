from rest_framework import serializers
from .models import CustomUser, Task

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'username', 'mobile', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUser.objects.all()
    )
    
    class Meta:
        model = Task
        fields = '__all__'
