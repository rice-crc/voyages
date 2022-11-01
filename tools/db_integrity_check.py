# Code heavily inspired by
# https://stackoverflow.com/questions/12926878/checking-foreign-keys-in-mysql

from django.db import connection    
from voyages.settings import DATABASES

def check(print_queries=False):
    db = DATABASES.get('default')
    if db is None:
        raise Exception("No default db found in localsettings.py")
    db_name = db.get('NAME')
    if db_name is None:
        raise Exception("Db name not found in localsettings.py")
    cursor = connection.cursor()
    cursor.execute(f"SELECT DISTINCT KEY_COLUMN_USAGE.CONSTRAINT_NAME, KEY_COLUMN_USAGE.TABLE_NAME, KEY_COLUMN_USAGE.COLUMN_NAME, KEY_COLUMN_USAGE.REFERENCED_TABLE_NAME, KEY_COLUMN_USAGE.REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE ON TABLE_CONSTRAINTS.CONSTRAINT_NAME=KEY_COLUMN_USAGE.CONSTRAINT_NAME WHERE TABLE_CONSTRAINTS.CONSTRAINT_TYPE=\"FOREIGN KEY\" AND TABLE_CONSTRAINTS.CONSTRAINT_SCHEMA=\"{db_name}\"")
    all_fk_checks = list(cursor.fetchall())
    res = {}
    for row in all_fk_checks:
        query = f"SELECT {row[1]}.{row[2]} AS CHILD_ID, {row[3]}.{row[4]} AS PARENT_ID FROM {db_name}.{row[1]} LEFT JOIN {db_name}.{row[3]} ON {row[1]}.{row[2]}={row[3]}.{row[4]} WHERE {row[3]}.{row[4]} IS NULL AND {row[1]}.{row[2]} IS NOT NULL"
        cursor.execute(query)
        bad = cursor.fetchall()
        if len(bad) == 0:
            continue
        if print_queries:
            print(query)
        for entry in bad:
            failures = res.setdefault(row[1], [])
            failures.append({"CONSTRAINT_NAME": row[0], "COLUMN_NAME": row[2], "REFERENCED_TABLE_NAME": row[3], "REFERENCED_COLUMN_NAME": row[4], "CHILD_ID": entry[0], "PARENT_ID": entry[1]}) 
    return res

def show(res, max_display=3):
    if len(res) == 0:
        print("All good!")
        return
    for k, entries in res.items():
        print(f"{k} - has {len(entries)} missing FKs")
        for e in entries[:max_display]:
            print(f"\t{e}")
        if len(entries) > max_display:
            print("\t...")

# Usage:
# on the Django shell (python3 manage.py shell)
# from tools.db_integrity_check import check, show
# res = check()
# show(res)