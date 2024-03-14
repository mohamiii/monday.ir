from .models import Board, Project, TaskList, Task
from .serializers import BoardSerializer, ProjectSerializer, TaskListSerializer, TaskSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from permissions import IsOwnerOrReadOnly


class BoardListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        boards = Board.objects.filter(user=request.user)
        srz_data = BoardSerializer(instance=boards, many=True).data
        return Response(srz_data, status=status.HTTP_200_OK)


class BoardCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BoardSerializer

    def post(self, request):
        srz_data = BoardSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save(user=request.user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def put(self, request, pk):
        board = Board.objects.get(pk=pk)
        self.check_object_permissions(request, board)
        srz_data = BoardSerializer(instance=board, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def delete(self, request, pk):
        board = Board.objects.get(pk=pk)
        self.check_object_permissions(request, board)
        srz_data = BoardSerializer(instance=board, data=request.data)
        if srz_data.is_valid():
            board.delete()
            return Response({'message': 'Board deleted'}, status=status.HTTP_200_OK)


class ProjectListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        project = Project.objects.get(pk=pk, user=request.user)
        srz_data = ProjectSerializer(instance=project).data
        return Response(srz_data, status=status.HTTP_200_OK)


class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProjectSerializer

    def post(self, request):
        board_obj = Board.objects.filter(user=request.user)
        owned_boards = BoardSerializer(instance=board_obj, many=True).data
        if not int(request.data['board']) in [i['id'] for i in owned_boards]:
            return Response({"Access denied"}, status=status.HTTP_403_FORBIDDEN)
        srz_data = ProjectSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save(user=request.user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def put(self, request, pk):
        project = Project.objects.get(pk=pk)
        self.check_object_permissions(request, project)
        srz_data = ProjectSerializer(instance=project, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def delete(self, request, pk):
        project = Project.objects.get(pk=pk)
        self.check_object_permissions(request, project)
        srz_data = ProjectSerializer(instance=project, data=request.data)
        if srz_data.is_valid():
            project.delete()
            return Response({'message': 'Project deleted'}, status=status.HTTP_200_OK)


class TaskListListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        get_list = TaskList.objects.get(pk=pk, user=request.user)
        srz_data = TaskListSerializer(instance=get_list).data
        return Response(srz_data, status=status.HTTP_200_OK)


class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TaskListSerializer

    def post(self, request):
        project_obj = Project.objects.filter(user=request.user)
        owned_projects = ProjectSerializer(instance=project_obj, many=True).data
        if not int(request.data['project']) in [i['id'] for i in owned_projects]:
            return Response({"Access denied"}, status=status.HTTP_403_FORBIDDEN)
        srz_data = TaskListSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save(user=request.user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def put(self, request, pk):
        get_list = TaskList.objects.get(pk=pk)
        self.check_object_permissions(request, TaskList)
        srz_data = TaskListSerializer(instance=get_list, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def delete(self, request, pk):
        get_list = TaskList.objects.get(pk=pk)
        self.check_object_permissions(request, get_list)
        srz_data = TaskListSerializer(instance=get_list, data=request.data)
        if srz_data.is_valid():
            get_list.delete()
            return Response({'message': 'List deleted'}, status=status.HTTP_200_OK)


class TaskListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        task = Task.objects.get(pk=pk, user=request.user)
        srz_data = TaskSerializer(instance=task).data
        return Response(srz_data, status=status.HTTP_200_OK)


class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = TaskSerializer

    def post(self, request):
        list_obj = TaskList.objects.filter(user=request.user)
        owned_lists = TaskListSerializer(instance=list_obj, many=True).data
        if not int(request.data['list']) in [i['id'] for i in owned_lists]:
            return Response({"Access denied"}, status=status.HTTP_403_FORBIDDEN)
        srz_data = TaskSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save(user=request.user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def put(self, request, pk):
        task = Task.objects.get(pk=pk)
        self.check_object_permissions(request, task)
        srz_data = TaskSerializer(instance=task, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def delete(self, request, pk):
        task = Task.objects.get(pk=pk)
        self.check_object_permissions(request, task)
        srz_data = TaskSerializer(instance=task, data=request.data)
        if srz_data.is_valid():
            task.delete()
            return Response({'message': 'Task deleted'}, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
