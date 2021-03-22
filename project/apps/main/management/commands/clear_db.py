from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    """Clears out all the db"""

    def handle(self, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute('show tables;')
        parts = ('DROP TABLE IF EXISTS %s;' % table for (table,) in cursor.fetchall())
        sql = 'SET FOREIGN_KEY_CHECKS = 0;\n' + '\n'.join(parts) + 'SET FOREIGN_KEY_CHECKS = 1;\n'
        connection.cursor().execute(sql)
