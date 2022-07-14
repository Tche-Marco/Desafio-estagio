from django import forms
from datetime import timedelta, datetime
from .models import Usuario

class CriaHorarioForm(forms.Form):

  dataInicio = forms.DateTimeField(label='Data inicial da agenda de atendimento', help_text='dia/mês/ano hora:minuto')
  dataFim = forms.DateTimeField(label='Data final da agenda de atendimento', help_text='dia/mês/ano hora:minuto')
  duracao = forms.IntegerField(label='Duração por atendimento', help_text='minutos')
  qtVagas = forms.IntegerField(label='Quantidade de vagas disponíveis por dia', min_value=1)

  def clean(self):

    dados = super().clean()
    dataInicio = dados.get('dataInicio')
    dataFim = dados.get('dataFim')
    duracao = dados.get('duracao')

    
    if dataFim <= dataInicio:
      self.add_error('dataFim', 'A data final deve ser maior que a inicial')
    elif dataFim < dataInicio+timedelta(minutes=duracao):
      self.add_error('dataFim', 'A data final deve ser maior que o fim do primeiro atendimento')

    if duracao < 1:
      self.add_error('duracao', 'Os atendimentos devem ter a duração maior que 1 minuto')

    return dados


class SolicitaHorarioForm(forms.Form):

  data_solicitada = forms.DateTimeField(label='Data que deseja marcar seu atendimento', help_text='dia/mês/ano hora:minuto')

  def clean(self):

    dados = super().clean()
    data = dados.get('data_solicitada')
    
    if data.date() < datetime.utcnow().date():
      self.add_error('data_solicitada', 'A data solicitada não pode ser anterior à hoje')

    return dados


class CriaUsuarioForm(forms.Form):

  tipos_usuario = (
    ('C', 'Cliente'),
    ('O', 'Operador'),
  )

  username = forms.CharField(label='Digite o nome de usuário.', help_text='150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.', max_length=150)
  nome = forms.CharField(label='Digite seu nome completo.', help_text='150 caracteres ou menos', max_length=150)
  cpf = forms.CharField(label="Digite seu CPF", help_text="Somente números", required=False)
  tipo_usuario = forms.ChoiceField(choices = tipos_usuario)
  senha = forms.CharField(label='Digite uma senha para o usuário.', help_text='Sua senha precisa conter pelo menos 8 caracteres e não pode ser inteiramente numérica.',max_length=30, min_length=8)
  confirmar_senha = forms.CharField(label='Cofirme sua senha.', help_text='Informe a mesma senha informada anteriormente, para verificação.',max_length=30, min_length=8)

  def clean(self):

    dados = super().clean()
    username = dados.get('username') 
    cpf = dados.get('cpf')
    senha = dados.get('senha')
    confirmar_senha = dados.get('confirmar_senha')

    for u in Usuario.objects.all():
      if u.usuario.username == username:
        self.add_error('username', 'Esse username já está em uso')   
      if u.cpf == cpf:
        self.add_error('cpf', 'Esse CPF já está em uso')     

    if not cpf.isalnum():    
      self.add_error('cpf', 'Digite apenas números')   
    
    lista=['@','.','+','-','_']
    for i in senha:
      if not i.isalnum():
        if i not in lista:
          self.add_error('senha', 'A senha pode conter apenas letras, números e @/./+/-/_')
        
    if senha != confirmar_senha:
      self.add_error('confirmar_senha', 'As senhas devem ser iguais')
      
    return dados