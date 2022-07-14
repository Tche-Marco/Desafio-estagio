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

Instale as dependências do projeto
```console
  pip install -r requirements.txt
```

Definindo as variaveis no arquivo .env
```
  Copie o arquivo .env.example e renomei para .env
```

Configurando o banco de dados local
```
  O banco de dados está sendo hospedado localmente, para configurar os acessos, use o arquivo .env e insira as 
  informações de acesso do seu banco local.
```

Exemplo de Configuração
```
  SECRET_KEY=Sua chave do Django
  DEBUG=True
  DB_ENGINE=django.db.backends.postgresql
  DB_NAME=Nome do banco de dados
  DB_USER=Usuário do banco de ados
  DB_PASSWORD=Senha do banco de dados
  DB_HOST=Hospedagem do Banco
  DB_PORT=5432
```
## Uso

Rode o servidor:
```console
python manage.py runserver
```

O servidor estará disponível em: 
```console
http://127.0.0.1:8000/login/
```
