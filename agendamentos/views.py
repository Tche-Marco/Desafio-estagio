from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Horario, Usuario
from django.views.generic import FormView
from .forms import CriaHorarioForm, SolicitaHorarioForm, CriaUsuarioForm
from datetime import datetime, timedelta
from django.contrib.auth.models import User


def horarios(request):

  usuario = request.user
  hor_disp = []
  hor_agendados = []
  horarios = Horario.objects.order_by('dataInicio')

  if usuario.is_authenticated:  

    usuario = Usuario.objects.get(usuario=usuario)    

  for h in horarios:

    if not h.cliente:   
      if h.qtVagas >= 1:     
        hor_disp.append(h)  

    else:
      hor_agendados.append(h) 

  return render(request, 'agendamentos/horarios.html', {'horarios_agendados' : hor_agendados, 'horarios_disp' : hor_disp, 'usuario' : usuario})


def horario(request, pk):

  usuario = request.user
  horario = Horario.objects.get(id=pk)
  horarios_cod = Horario.objects.filter(cod=horario.cod)

  if usuario.is_authenticated:  

    usuario = Usuario.objects.get(usuario=usuario)  

    if usuario.tipo_usuario == 'C':

      if not horario.cliente:
        horario.cliente=usuario
        horario.save()
        for h in horarios_cod:
          h.qtVagas-=1
          h.save() 
        return HttpResponseRedirect(reverse('horarios_user'))

      else:
        horario.cliente=None  
        horario.save()
        for h in horarios_cod:
          h.qtVagas+=1
          h.save()   
        return HttpResponseRedirect(reverse('horarios'))

    elif usuario.tipo_usuario == 'O':      
      horario.delete()
      return HttpResponseRedirect(reverse('horarios'))


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


def horarios_user(request):

  usuario = request.user
  horarios_user = []
  horarios = Horario.objects.order_by('dataInicio')

  if usuario.is_authenticated:  

      usuario = Usuario.objects.get(usuario=usuario)  

      for h in horarios:

        if h.cliente == usuario:
          horarios_user.append(h)    

  return render(request, 'agendamentos/horarios_user.html', {'horarios_user' : horarios_user, 'usuario' : usuario})


class SolicitaHorarioView(FormView):

  template_name = 'agendamentos/data_solicitada.html'
  form_class = SolicitaHorarioForm

  def get(self, request):

    usuario = self.request.user

    if usuario.is_authenticated:
        usuario = Usuario.objects.get(usuario = usuario)
    return render (request, self.template_name, {'usuario' : usuario, 'form' : self.form_class })

  def form_valid(self, form):

    usuario = self.request.user  
    horarios = Horario.objects.order_by('dataInicio')
    solicitacoes = []
    sugestoes = []

    if usuario.is_authenticated:
      
      usuario = Usuario.objects.get(usuario = usuario)
      dados = form.clean()
      data_solicitada=dados['data_solicitada']
      sugestao = datetime(year=9999, month=1, day=1)

      for h in horarios:

        if h.dataInicio.date() == data_solicitada.date():
          solicitacoes.append(h)

        elif h.dataInicio.date() > data_solicitada.date():
          if h.dataInicio.date() <= sugestao.date():
            sugestao=h.dataInicio 
            sugestoes.append(h)            

    return render(self.request, 'agendamentos/retorno_solicitacao.html', {'usuario' : usuario, 'solicitacoes' : solicitacoes, 'sugestoes' : sugestoes })


class CriaUsuarioView(FormView):

  template_name = 'agendamentos/user_cadastro.html'
  form_class = CriaUsuarioForm

  def get(self, request):

    return render (request, self.template_name, {'form' : self.form_class})

  def form_valid(self, form):

    dados = form.clean()
    username=dados['username']
    nome = dados['nome']
    cpf = dados['cpf']
    tipo_usuario = dados['tipo_usuario']
    senha = dados['senha']
    
    user = User.objects.create_user(username, None, senha)
    user.save()
    usuario = Usuario(usuario = user, nome = nome, cpf = cpf, tipo_usuario = tipo_usuario)
    usuario.save()

    return super().form_valid(form)

  def get_success_url(self):
    return reverse('login')