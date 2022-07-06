import code
from django.shortcuts import render
from django.urls import reverse
from .models import Horario, Usuario
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from .forms import CriaHorarioForm
from datetime import datetime, timedelta


def horarios(request):
  usuario = request.user
  hor_disp = []
  hor_agendados = []
  horarios = Horario.objects.all()

  if usuario.is_authenticated:            
      usuario = Usuario.objects.get(usuario=usuario)  

  for h in horarios:
    if not h.cliente:
      hor_disp.append(h)    
    else:
      hor_agendados.append(h) 

  return render(request, 'agendamentos/horarios.html', {'horarios_agendados' : hor_agendados,'horarios_disp' : hor_disp, 'usuario' : usuario})


def horario(request, pk):
  usuario = request.user
  horario = Horario.objects.get(id=pk)

  if usuario.is_authenticated:            
      usuario = Usuario.objects.get(usuario=usuario)  
      
  return render(request, 'agendamentos/horario.html', {'horario' : horario, 'usuario' : usuario})

'''class HorarioCreate(CreateView):
  model = Horario
  fields = ['dataInicio', 'dataFim', 'duracao', 'qtVagas']
  template_name = 'agendamentos/cadastro.html'
  success_url = reverse_lazy('horarios')'''

class CriaHorarioView(FormView):

  template_name = 'agendamentos/cadastro.html'
  form_class = CriaHorarioForm

  def get(self, request):

          usuario = self.request.user
          if usuario.is_authenticated:
              usuario = Usuario.objects.get(usuario = usuario)
          return render (request, self.template_name, {'usuario' : usuario, 'form' : self.form_class })

  def form_valid(self, form):

    usuario = self.request.user  

    if usuario.is_authenticated:

            usuario = Usuario.objects.get(usuario = usuario)
            dados = form.clean()

            dataInicio=dados['dataInicio']
            dataFim=dados['dataFim']
            duracao=dados['duracao']
            qtVagas=dados['qtVagas']
            dataI=dataInicio
            dataF=dataInicio+timedelta(minutes=duracao)
            cod=int(datetime.utcnow().timestamp())

            while dataF<=dataFim:
              horario = Horario(criador=usuario, dataInicio=dataI, dataFim=dataF, duracao=duracao, qtVagas=qtVagas, cod=cod)
              horario.save()
              dataI=dataF
              dataF=dataI+timedelta(minutes=duracao)
         
            return super().form_valid(form)

  def get_success_url(self):
        return reverse('horarios')