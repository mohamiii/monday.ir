from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
	# path('', views.Home.as_view(), name='home'),
	path('board/', views.BoardListView.as_view()),
	path('board/create/', views.BoardCreateView.as_view()),
	path('board/update/<int:pk>/', views.BoardUpdateView.as_view()),
	path('board/delete/<int:pk>/', views.BoardDeleteView.as_view()),
	path('project/', views.ProjectListView.as_view()),
	path('project/create/', views.ProjectCreateView.as_view()),
	path('project/update/<int:pk>/', views.ProjectUpdateView.as_view()),
	path('project/delete/<int:pk>/', views.ProjectDeleteView.as_view()),
	path('list/', views.TaskListListView.as_view()),
	path('list/create/', views.TaskListCreateView.as_view()),
	path('list/update/<int:pk>/', views.TaskListUpdateView.as_view()),
	path('list/delete/<int:pk>/', views.TaskListDeleteView.as_view()),
	path('task/', views.TaskListView.as_view()),
	path('task/create/', views.TaskCreateView.as_view()),
	path('task/update/<int:pk>/', views.TaskUpdateView.as_view()),
	path('task/delete/<int:pk>/', views.TaskDeleteView.as_view()),
]
