import sqlite3

t = ['courier',
     'courier_region',
     'working_hours',
     'assigning',
     'delivery',
     'delivery_hours',
     'orders']

for table in t:
    with sqlite3.connect('api_database.db') as db:
        cursor = db.cursor()
        query = f"""
        DELETE FROM {table}
        """
        result = cursor.execute(query)
