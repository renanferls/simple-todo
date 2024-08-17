from django.shortcuts import render
from rest_framework.views import APIView

from .serializers import LabelSerializer, TaskSerializer
from .models import Task, Label, LabelTask
from rest_framework.response import Response

from django.utils import timezone

# Create your views here.
class LabelView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                label = Label.objects.get(id=pk)
                serializer = LabelSerializer(label)
                return Response(serializer.data)
            except Label.DoesNotExist:
                return Response({"error": "Label not found"}, status=404)

        data = Label.objects.filter(deleted_at__isnull=True)
        serializer = LabelSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request, pk):
        try:
            label = Label.objects.get(id=pk)
            serializer = LabelSerializer(label, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Label.DoesNotExist:
            return Response({"error": "Label not found"}, status=404)
    
    def delete(self, request, pk):
        try:
            label = Label.objects.get(id=pk)
            label.deleted_at = timezone.now()
            return Response({"message": "Label deleted successfully"})
        except Label.DoesNotExist:
            return Response({"error": "Label not found"}, status=404)
    
class TaskView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                data = Task.objects.get(id=pk, deleted_at__isnull=True).order_by('-updated_at')
                serializer = TaskSerializer(data)
                return Response(serializer.data)
            except Task.DoesNotExist:
                return Response({"error": "Task not found"}, status=404)
            
        tasks = Task.objects.filter(deleted_at__isnull=True, is_archived = False)
        
        label_id = request.query_params.get('label_id', None)
        label_str = request.query_params.get('label_str', None)
        archived = request.query_params.get('archived', False)

        if label_id is not None:
            tasks = Task.objects.filter(labeltask__label_id=label_id)

        if label_str is not None:
            tasks = Task.objects.filter(labeltask__label__name__icontains=label_str)

        if archived:
            tasks = Task.objects.all(deleted_at__isnull=True, is_archived=True)

        serializer = TaskSerializer(tasks, many=True)        
        return Response(serializer.data)
        
    def post(self, request):
        print("🚀 ~ request.data:", request.data)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            record = serializer.save()
            if request.data.get('labels', []):
                label_records = Label.objects.filter(id__in=list(set(request.data.get('labels', []))), deleted_at__isnull=True)
                for i in label_records:
                    LabelTask.objects.create(label=i, task=record)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request, pk):
        try:
            task = Task.objects.get(id=pk)
            if task.current_state == 'TODO':
                task.current_state = 'INPROGRESS'
            
            elif task.current_state == 'INPROGRESS':
                task.current_state = 'DONE'

            task.save()
            serializer = TaskSerializer(task)
            return Response(serializer.data)
            # serializer = TaskSerializer(task, data=request.data, partial=True)
            # if serializer.is_valid():
            #     record = serializer.save()
            #     label_task_records = LabelTask.objects.filter(task=task)
            #     ids_to_delete = [label_id.id for label_id in label_task_records if label_id.label.id not in list(set(request.data.get('labels', [])))]
            #     ids_to_create = [label_id for label_id in list(set(request.data.get('labels', []))) if label_id not in [item.label.id for item in label_task_records]]
                
            #     LabelTask.objects.filter(id__in=ids_to_delete).update(deleted_at=timezone.now())
                
            #     label_records = Label.objects.filter(id__in=list(set(ids_to_create)))
            #     for i in label_records:
            #         LabelTask.objects.create(label=i, task=record)
            #     return Response(serializer.data)
            # return Response(serializer.errors, status=400)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)
    
    def delete(self, request, pk):
        try:
            task = Task.objects.get(id=pk)
            task.deleted_at = timezone.now()
            task.save()
            return Response({"message": "Task deleted successfully"})
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)