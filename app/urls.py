from django.urls import path
from .views import TaskView, LabelView

urlpatterns = [
    path("task/", TaskView.as_view()),
    path("task/<int:pk>", TaskView.as_view()),
    path("label/", LabelView.as_view()),
    path("label/<int:pk>", LabelView.as_view()),
]
