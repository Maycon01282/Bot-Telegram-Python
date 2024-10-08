import os
import django
from django.core.management import call_command

# Configura o Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adminpanel.settings")  # Ajuste conforme o nome do seu projeto
django.setup()

# Executa as migrações para criar as tabelas no banco de dados
call_command('makemigrations')
call_command('migrate')

# Importando o ORM e os modelos
from adminpanelproject.models import *  # Certifique-se de que todos os modelos estão corretamente importados

# Agora você pode usar os modelos do Django para interagir com o banco de dados