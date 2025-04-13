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
        return Response({
            "success": True,
            "message": "Users retrieved successfully.",
            "data": serializer.data
        })
    elif request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "User created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "User creation failed.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def user_detail(request, pk):
    """
    Retrieve, update, or delete a user.
    """
    user = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return Response({
            "success": True,
            "message": "User retrieved successfully.",
            "data": serializer.data
        })
    elif request.method in ['PUT', 'PATCH']:
        serializer = CustomUserSerializer(user, data=request.data, partial=(request.method=='PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "User updated successfully.",
                "data": serializer.data
            })
        return Response({
            "success": False,
            "message": "User update failed.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response({
            "success": True,
            "message": "User deleted successfully.",
            "data": None
        }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def task_list(request):
    """
    List all tasks or create a new task.
    """
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({
            "success": True,
            "message": "Tasks retrieved successfully.",
            "data": serializer.data
        })
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Task created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Task creation failed.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def task_detail(request, pk):
    """
    Retrieve, update, or delete a task.
    """
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response({
            "success": True,
            "message": "Task retrieved successfully.",
            "data": serializer.data
        })
    elif request.method in ['PUT', 'PATCH']:
        serializer = TaskSerializer(task, data=request.data, partial=(request.method=='PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Task updated successfully.",
                "data": serializer.data
            })
        return Response({
            "success": False,
            "message": "Task update failed.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        task.delete()
        return Response({
            "success": True,
            "message": "Task deleted successfully.",
            "data": None
        }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def tasks_assigned_to_user(request, user_id):
    """
    Retrieve all tasks assigned to a specific user.
    """
    tasks = Task.objects.filter(assigned_to=user_id)
    serializer = TaskSerializer(tasks, many=True)
    return Response({
        "success": True,
        "message": f"Tasks assigned to user {user_id} retrieved successfully.",
        "data": serializer.data
    })


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
        return Response({
            "success": True,
            "message": "Assignees assigned successfully.",
            "data": serializer.data
        })
    else:
        return Response({
            "success": False,
            "message": "No assignees provided.",
            "data": None
        }, status=status.HTTP_400_BAD_REQUEST)
