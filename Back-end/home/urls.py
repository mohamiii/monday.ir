from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
	path('', views.BoardListView.as_view(), name='home'),
	path('create/', views.BoardCreateView.as_view()),
	path('update/<int:pk>/', views.BoardUpdateView.as_view()),
	path('delete/<int:pk>/', views.BoardDeleteView.as_view()),
	path('project/<int:pk>/', views.ProjectListView.as_view()),
	path('project/create/', views.ProjectCreateView.as_view()),
	path('project/update/<int:pk>/', views.ProjectUpdateView.as_view()),
	path('project/delete/<int:pk>/', views.ProjectDeleteView.as_view()),
	path('list/<int:pk>/', views.TaskListListView.as_view()),
	path('list/create/', views.TaskListCreateView.as_view()),
	path('list/update/<int:pk>/', views.TaskListUpdateView.as_view()),
	path('list/delete/<int:pk>/', views.TaskListDeleteView.as_view()),
	path('task/<int:pk>/', views.TaskListView.as_view()),
	path('task/create/', views.TaskCreateView.as_view()),
	path('task/update/<int:pk>/', views.TaskUpdateView.as_view()),
	path('task/delete/<int:pk>/', views.TaskDeleteView.as_view()),
]
