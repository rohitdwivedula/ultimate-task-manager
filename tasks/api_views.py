from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView, Response
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
import math
import json

from authentication.models import User
from tasks.models import Label, Task, SubTask
from tasks.serializers import LabelSerializer, TaskSerializer, SubTaskSerializer
from tasks.submodels import TaskStatus, SubTaskStatus

class AllTasksView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        # get a task
        filters = {"user": request.user}
        for key in request.GET:
            if key != "page":
                filters[key] = request.GET[key]
        try:
            print(filters)
            tasks = Task.objects.filter(**filters).order_by("due_on")
            paginator = PageNumberPagination()
            paginator.page_size = 15
            result_page = paginator.paginate_queryset(tasks, request)
            serializer = TaskSerializer(result_page, many=True, context={"request": request})
            return Response({
                "current_page": request.GET['page'],
                "total_pages": math.ceil(len(tasks)/15),
                "count": len(result_page),
                "data": serializer.data
            })
        except KeyError:
            return Response(data={
                "message": "Bad request. The allowed fields are given in this response. You can use standard Django Queryset filters",
                "allowed_fields": "created_at, desc, due_on, labels, name, status, subtasks, user, user_id, uuid"
            }, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request):
        try:
            user = request.user
            payload = request.data
            print(payload)
            new_task = Task(user=user, name=payload['name'], desc=payload['desc'], due_on=payload['due_on'])
            if "priority" in payload:
                if payload["priority"] not in ['L', 'M', 'H']:
                    transaction.set_rollback(True)
                    message = {'error': 'priority must be L, M, H'}
                    return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
                new_task.priority = payload["priority"]
            if "status" in payload:
                if payload["priority"] not in ['N', 'IP', 'C']:
                    transaction.set_rollback(True)
                    message = {'error': 'status must be N, IP, C'}
                    return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
                new_task.status = payload["status"]
            new_task.save()
            if "labels" in payload:
                values = json.loads(payload['labels'])
                for label in values:
                    try:
                        label_obj = Label.objects.filter(uuid=label, user=user)
                        if not label_obj:
                            transaction.set_rollback(True)
                            message = {'error': 'label not found'}
                            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)    
                        new_task.labels.add(label_obj[0])
                    except (ValidationError, KeyError):
                        transaction.set_rollback(True)
                        message = {'error': 'label not found'}
                        return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            new_task.save()
            if "subtasks" in payload:
                for subtask in payload["subtasks"]:
                    try:
                        subtask_obj = SubTask(name=subtask, task=new_task)
                        subtask_obj.save()
                    except (ValidationError, KeyError):
                        transaction.set_rollback(True)
                        message = {}
                        message['error'] = 'Subtask validation failed. Subtask which caused this error provided below.'
                        message['subtask'] = subtask
                        return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            message = {
            	'success': 'Task created.',
            	'task_uuid': new_task.uuid
            }
            return Response(data=message, status=status.HTTP_200_OK)
        except IntegrityError:
            message = {'error': 'Internal Server Error. No edits made.'}
            return Response(data=message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TaskView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, task_uuid):
        user = request.user
        try:
            task = Task.objects.get(uuid=task_uuid, user=user)
            if not task:
                message = {'error': 'Task ID associated with signed in user does not exist.'}
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            serializer = TaskSerializer(task, many=False, context={"request": request})
            return Response(serializer.data)
        except Task.DoesNotExist:
            message = {'error': 'Task ID associated with signed in user does not exist.'}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_uuid):
        user = request.user
        try:
            task = Task.objects.get(uuid=task_uuid, user=user)
            if not task:
                message = {'error': 'Task ID associated with signed in user does not exist.'}
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            task.delete()
            message = {'success': 'Task deleted successfully.'}
            return Response(data=message, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            message = {'error': 'Task ID associated with signed in user does not exist.'}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, task_uuid):
        user = request.user
        payload = request.data
        try:
            task = Task.objects.get(uuid=task_uuid, user=user)
            if not task:
                message = {'error': 'Task ID associated with signed in user does not exist. No edits made'}
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            if "subtasks" in payload:
                transaction.set_rollback(True)
                message = {'error': 'Only name, desc, due_on, status, labels can be edited via this endpoint. No edits made'}
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            if "name" in payload:
                task.name = payload["name"]
            if "desc" in payload:
                task.desc = payload["desc"]
            if "due_on" in payload:
                task.due_on = payload["due_on"]
            if "status" in payload:
                if payload["status"] == 'N':
                    task.status = 'N'
                elif payload["status"] == 'IP':
                    task.status = 'IP'
                elif payload["status"] == 'C':
                    task.status = 'C'
                else:
                    transaction.set_rollback(True)
                    message = {'error': 'Acceptable task statuses are: N, IP, C only. No edits made'}
                    return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            if "priority" in payload:
                if payload["priority"] not in ['L', 'M', 'H']:
                    transaction.set_rollback(True)
                    message = {'error': 'priority must be L, M, H. No edits made'}
                    return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
                task.priority = payload["priority"]
            if "labels" in payload:
                for label in task.labels.all():
                    task.labels.remove(label)
                values = json.loads(payload["labels"])
                for label in values:
                    try:
                        label_obj = Label.objects.filter(uuid=label, user=user)
                        if not label_obj:
                            transaction.set_rollback(True)
                            message = {'error': 'label not found. No edits made'}
                            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)    
                        task.labels.add(label_obj[0])
                    except (ValidationError, KeyError):
                        transaction.set_rollback(True)
                        message = {'error': 'label not found. No edits made'}
                        return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            task.save()
            message = {'success': 'Task updated successfully.'}
            return Response(data=message, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            transaction.set_rollback(True)
            message = {'error': 'Task ID associated with signed in user does not exist.'}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            message = {'error': 'Internal Server Error. No edits made.'}
            return Response(data=message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AllLabelsView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        user = request.user
        labels = Label.objects.filter(user=user)
        serializer = LabelSerializer(labels, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            label = serializer.save(user=user)
            message = {'success': 'Label created.'}
            return Response(data=message, status=status.HTTP_200_OK)
        else:
            message = {'error': 'invalid schema'}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)    
        

class LabelView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, label_uuid):
        user = request.user
        try:
            label = Label.objects.get(uuid=label_uuid)
            if label.user != user:
                message = {'error': 'Label ID associated with signed in user does not exist.'}
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            serializer = LabelSerializer(label, many=False, context={"request": request})
            return Response(serializer.data)
        except Label.DoesNotExist:
            message = {'error': 'Label ID associated with signed in user does not exist.'}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, label_uuid):
        user = request.user
        try:
            label = Label.objects.get(uuid=label_uuid)
            if label.user != user:
                message = {'error': 'Label ID associated with signed in user does not exist.'}
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            label.delete()
            message = {'success': 'Label deleted successfully.'}
            return Response(data=message, status=status.HTTP_200_OK)
        except Label.DoesNotExist:
            message = {'error': 'Label ID associated with signed in user does not exist.'}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, label_uuid):
        user = request.user
        payload = request.data
        try:
            label = Label.objects.get(uuid=label_uuid)
            if label.user != user:
                message = {'error': 'Label ID associated with signed in user does not exist.'}
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            if "name" in payload:
                label.name = payload["name"]
            if "description" in payload:
                label.description = payload["description"]
            label.save()
            message = {'success': 'Label updated successfully.'}
            return Response(data=message, status=status.HTTP_200_OK)
        except Label.DoesNotExist:
            message = {'error': 'Label ID associated with signed in user does not exist.'}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class SubTaskView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, subtask_uuid):
        user = request.user
        try:
            subtask = SubTask.objects.get(uuid=subtask_uuid)
            if subtask.task.user != user:
                message = {'error': 'Subtask ID associated with signed in user does not exist.'}
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            serializer = SubTaskSerializer(subtask, many=False, context={"request": request})
            return Response(serializer.data)
        except SubTask.DoesNotExist:
            message = {'error': 'Subtask ID associated with signed in user does not exist.'}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subtask_uuid):
        user = request.user
        try:
            subtask = SubTask.objects.get(uuid=subtask_uuid)
            if subtask.task.user != user:
                message = {'error': 'Subtask ID associated with signed in user does not exist.'}
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            subtask.delete()
            message = {'success': 'Subtask deleted successfully.'}
            return Response(data=message, status=status.HTTP_200_OK)
        except SubTask.DoesNotExist:
            message = {'error': 'Subtask ID associated with signed in user does not exist.'}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, subtask_uuid):
        user = request.user
        payload = request.data
        try:
            subtask = SubTask.objects.get(uuid=subtask_uuid)
            if subtask.task.user != user:
                message = {'error': 'Subtask ID associated with signed in user does not exist.'}
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            if "name" in payload:
                subtask.name = payload["name"]
            if "status" in payload:
                if payload["status"] == "D":
                    subtask.status = SubTaskStatus.DONE
                elif payload["status"] == "ND":
                    subtask.status = SubTaskStatus.NOT_DONE
                else:
                    message = {'error': 'Subtask status must be D or ND for done or not done respectvely'}
                    return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            subtask.save()
            message = {'success': 'Subtask updated successfully.'}
            return Response(data=message, status=status.HTTP_200_OK)
        except SubTask.DoesNotExist:
            message = {'error': 'Subtask ID associated with signed in user does not exist.'}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class AllSubTaskView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, task_uuid):
        user = request.user
        try:
            task = Task.objects.get(uuid=task_uuid, user=user)
            subtasks = SubTask.objects.filter(task=task)
            serializer = SubTaskSerializer(subtasks, many=True, context={"request": request})
            return Response(serializer.data)
        except Task.DoesNotExist:
            message = {'error': 'Task ID associated with signed in user does not exist.'}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, task_uuid):
        user = request.user
        payload = request.data
        try:
            task = Task.objects.get(uuid=task_uuid, user=user)
            subtask = SubTask(name=payload["name"], task=task)
            subtask.save()
            message = {'success': 'Subtask created successfully'}
            return Response(data=message, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            message = {'error': 'Task ID associated with signed in user does not exist.'}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            message = {'error': 'Subtask must have a name attribute.'}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)