# Local Database 
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cuappsite_db', 
        'USER': 'antonakakisj',
        'PASSWORD': 'antonakakisj',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# For local stuff 
DEBUG = True 
