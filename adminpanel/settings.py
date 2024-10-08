import os

# Caminho do diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Chave secreta usada em produção
SECRET_KEY = 'sua-chave-secreta-aqui'

# Lista de hosts permitidos
ALLOWED_HOSTS = []

# Configurações do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bottelegram',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Adicione as suas aplicações aqui
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'adminpanelproject'
]

# Outras configurações...
