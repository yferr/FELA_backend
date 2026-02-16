from django.db import connection
from core.commonLibs.pgOperations import PgConnection

def run(*args):
    oc=PgConnection(connection)
    print('Creando extensión postgis')
    oc.cursor.execute('CREATE extension postgis')
    oc.commit()