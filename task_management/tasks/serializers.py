from rest_framework import serializers
from .models import CustomUser, Task

# Serializer for CustomUser with full CRUD
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

# Serializer for Task model
class TaskSerializer(serializers.ModelSerializer):
    # Represent the assigned users as a list of their IDs
    assigned_to = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUser.objects.all()
    )
    
    class Meta:
        model = Task
        fields = '__all__'
