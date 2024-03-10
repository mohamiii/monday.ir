from .models import Board, Project, TaskList, Task
from .serializers import BoardSerializer, ProjectSerializer, TaskListSerializer, TaskSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from permissions import IsOwnerOrReadOnly

# class Home(APIView):
"""If a user is logged in show profile else show homepage"""


#     permission_classes = [IsAuthenticated, ]
#
#     def get(self, request):
#         persons = Person.objects.all()
#         ser_data = PersonSerializer(instance=persons, many=True)
#         return Response(data=ser_data.data)
#


class BoardListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        boards = Board.objects.all()
        srz_data = BoardSerializer(instance=boards, many=True).data
        return Response(srz_data, status=status.HTTP_200_OK)


class BoardCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProjectSerializer

    def post(self, request):
        srz_data = BoardSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save(user=request.user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def put(self, request, pk):
        board = Board.objects.get(pk=pk)
        self.check_object_permissions(request, board)
        srz_data = BoardSerializer(instance=board, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def delete(self, request, pk):
        board = Board.objects.get(pk=pk)
        board.delete()
        return Response({'message': 'Board deleted'}, status=status.HTTP_200_OK)


class ProjectListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        projects = Project.objects.all()
        srz_data = ProjectSerializer(instance=projects, many=True).data
        return Response(srz_data, status=status.HTTP_200_OK)


class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProjectSerializer

    def post(self, request):
        srz_data = ProjectSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save(user=request.user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def put(self, request, pk):
        project = Project.objects.get(pk=pk)
        self.check_object_permissions(request, project)
        srz_data = BoardSerializer(instance=project, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def delete(self, request, pk):
        project = Project.objects.get(pk=pk)
        project.delete()
        return Response({'message': 'Project deleted'}, status=status.HTTP_200_OK)


class TaskListListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        get_list = TaskList.objects.all()
        srz_data = TaskListSerializer(instance=get_list, many=True).data
        return Response(srz_data, status=status.HTTP_200_OK)


class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TaskListSerializer

    def post(self, request):
        srz_data = TaskListSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save(user=request.user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def put(self, request, pk):
        get_list = TaskList.objects.get(pk=pk)
        self.check_object_permissions(request, TaskList)
        srz_data = TaskListSerializer(instance=get_list, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def delete(self, request, pk):
        get_list = TaskList.objects.get(pk=pk)
        get_list.delete()
        return Response({'message': 'List deleted'}, status=status.HTTP_200_OK)


class TaskListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        tasks = Task.objects.all()
        srz_data = TaskSerializer(instance=tasks, many=True).data
        return Response(srz_data, status=status.HTTP_200_OK)


class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TaskSerializer

    def post(self, request):
        srz_data = TaskSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save(user=request.user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def put(self, request, pk):
        tasks = Task.objects.get(pk=pk)
        self.check_object_permissions(request, tasks)
        srz_data = BoardSerializer(instance=tasks, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def delete(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response({'message': 'Task deleted'}, status=status.HTTP_200_OK)
