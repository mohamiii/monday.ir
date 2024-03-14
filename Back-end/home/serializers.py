from rest_framework import serializers
from .models import Board, Project, TaskList, Task


class BoardSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ("id", "title", "created", "projects")

    def get_projects(self, obj):
        result = obj.projects.values("id", "title", "created", "board")
        return result


class ProjectSerializer(serializers.ModelSerializer):
    lists = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ("id", "title", "created", "board", "lists")

    def get_lists(self, obj):
        result = obj.lists.all()
        return TaskListSerializer(instance=result, many=True).data


class TaskListSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = TaskList
        fields = ("id", "title", "created", "project", "tasks")

    def get_tasks(self, obj):
        result = obj.tasks.all()
        return TaskSerializer(instance=result, many=True).data


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("id", "title", "created", "list", "state")
