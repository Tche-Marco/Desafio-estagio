from django.urls import path
from .views import horarios, horario, CriaHorarioView, horarios_user

urlpatterns = [
    path('horarios/', horarios, name="horarios"),
    path('horario/<str:pk>', horario, name="horario"),
    path('cadastro/', CriaHorarioView.as_view(), name="cadastrar_horario"),
    path('horarios/user', horarios_user, name="horarios_user")
]
