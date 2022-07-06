from django import forms
from datetime import timedelta

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
    if dataFim < dataInicio+timedelta(minutes=duracao):
      self.add_error('dataFim', 'A data final deve ser maior que o fim do primeiro atendimento')
    if duracao < 1:
      self.add_error('duracao', 'Os atendimentos devem ter a duração maior que 1 minuto')

    return dados