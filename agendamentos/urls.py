from django.urls import path
from .views import horarios, horario, CriaHorarioView

urlpatterns = [
    path('horarios/', horarios, name="horarios"),
    path('horario/<str:pk>', horario, name="horario"),
    path('cadastro/', CriaHorarioView.as_view(), name="cadastrar_horario"),
]
