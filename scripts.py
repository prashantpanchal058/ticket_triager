import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection


def get_entries(id):

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM home_mymodel WHERE id = %s",
            (id,)
        )

        row = cursor.fetchone()

        print(row)


get_entries(1)