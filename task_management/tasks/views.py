from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Task
from .serializers import CustomUserSerializer, TaskSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
def user_list(request):
    """
    List all users or create a new user.
    """
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def user_detail(request, pk):
    """
    Retrieve, update, or delete a user.
    """
    user = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = CustomUserSerializer(user, data=request.data, partial=(request.method=='PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def task_list(request):
    """
    List all tasks or create a new task.
    """
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def task_detail(request, pk):
    """
    Retrieve, update, or delete a task.
    """
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = TaskSerializer(task, data=request.data, partial=(request.method=='PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def tasks_assigned_to_user(request, user_id):
    """
    Retrieve all tasks assigned to a specific user.
    """
    tasks = Task.objects.filter(assigned_to=user_id)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
def assign_assignees_to_task(request, pk):
    """
    Assign new assignees to a task.
    """
    task = get_object_or_404(Task, pk=pk)
    assignees_data = request.data.get('assigned_to', [])
    
    if assignees_data:
        assignees = CustomUser.objects.filter(id__in=assignees_data)
        task.assigned_to.set(assignees)
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "No assignees provided."}, status=status.HTTP_400_BAD_REQUEST)
