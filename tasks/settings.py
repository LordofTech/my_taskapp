import django_heroku
import dj_database_url

# Configure database settings using dj_database_url
DATABASES = {'default': dj_database_url.config(conn_max_age=600)}

# Activate Django-Heroku
django_heroku.settings(locals())
