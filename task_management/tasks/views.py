from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Task
from .serializers import CustomUserSerializer, TaskSerializer
from django.shortcuts import get_object_or_404
from django.db import DatabaseError


@api_view(['GET', 'POST'])
def user_list(request):
    try:
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

    except DatabaseError as e:
        return Response({
            "success": False,
            "message": f"Database error: {str(e)}",
            "data": None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Unexpected error: {str(e)}",
            "data": None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def user_detail(request, pk):
    try:
        user = get_object_or_404(CustomUser, pk=pk)

        if request.method == 'GET':
            serializer = CustomUserSerializer(user)
            return Response({
                "success": True,
                "message": "User retrieved successfully.",
                "data": serializer.data
            })

        elif request.method in ['PUT', 'PATCH']:
            serializer = CustomUserSerializer(user, data=request.data, partial=(request.method == 'PATCH'))
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

    except Exception as e:
        return Response({
            "success": False,
            "message": f"An error occurred: {str(e)}",
            "data": None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def task_list(request):
    try:
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

    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error: {str(e)}",
            "data": None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def task_detail(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)

        if request.method == 'GET':
            serializer = TaskSerializer(task)
            return Response({
                "success": True,
                "message": "Task retrieved successfully.",
                "data": serializer.data
            })

        elif request.method in ['PUT', 'PATCH']:
            serializer = TaskSerializer(task, data=request.data, partial=(request.method == 'PATCH'))
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

    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error: {str(e)}",
            "data": None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def tasks_assigned_to_user(request, user_id):
    try:
        tasks = Task.objects.filter(assigned_to=user_id)
        if not tasks.exists():
            return Response({
                "success": False,
                "message": f"No tasks found for user {user_id}.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(tasks, many=True)
        return Response({
            "success": True,
            "message": f"Tasks assigned to user {user_id} retrieved successfully.",
            "data": serializer.data
        })

    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error: {str(e)}",
            "data": None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
def assign_assignees_to_task(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)
        assignees_data = request.data.get('assigned_to')

        if not isinstance(assignees_data, list) or not assignees_data:
            return Response({
                "success": False,
                "message": "Invalid or empty 'assigned_to' list.",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        assignees = CustomUser.objects.filter(id__in=assignees_data)

        if not assignees.exists():
            return Response({
                "success": False,
                "message": "No valid assignees found for given IDs.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        task.assigned_to.set(assignees)
        task.save()
        serializer = TaskSerializer(task)
        return Response({
            "success": True,
            "message": "Assignees assigned successfully.",
            "data": serializer.data
        })

    except Exception as e:
        return Response({
            "success": False,
            "message": f"Failed to assign assignees: {str(e)}",
            "data": None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
