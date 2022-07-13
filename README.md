## Pré requisitos

```
Python == 3.10
```

Crie e habilite um ambiente python
```console
  python -m venv venv
```
```console
  venv\Scripts\activate | windows
  . venv/bin/activate | linux e macOs
```

Instale o Django
```console
  pip install django==3.2
```

Instale o aplicativo Django-crispy-forms
```console
  pip install django-crispy-forms
```
Instale a biblioteca psycopg2
```console
  pip install psycopg2 
```

## Uso

Rode o servidor:
```console
python manage.py runserver
```

O servidor estará disponível em: 
```console
http://localhost:8000/login/
```

## Exemplo de rota

http://localhost:8000/horarios/
