#!/bin/

import sys
import os

DB_USR = os.environ["DB_USR"]
DB_PSW = os.environ["DB_PSW"]


def _mysql(db_name: str, out, MODE: int):
    import mysql.connector
    db = mysql.connector.connect(
        host="localhost",
        user=DB_USR,
        password=DB_PSW
    )

    cursor = db.cursor()

    cursor.execute(f"USE {db_name}")
    cursor.execute("SHOW TABLES")

    tables = [table_name for (table_name, ) in cursor]

    for t in tables:
        out.write(f"# {t}\n")
        cursor.execute(f"DESCRIBE {t}")
        if MODE == 1:
            out.write("| name | type | null | key | default | extra |\n")
            out.write("|------|------|------|-----|---------|-------|\n")

            for res in cursor:
                name, type, null, key, default, extra = res
                k = key if key else "/"
                ex = extra if extra else "/"

                out.write(
                    f"| {name} | {type} | {null} | {k} | {default} | {ex} |\n")
        elif MODE == 0:
            for res in cursor:
                name, type, null, key, default, extra = res
                out.write(f"##### {name}:\n")
                out.write(f"- **type**: {type}\n")
                out.write(f"- **null**: {null}\n")
                k = key if key else "/"
                out.write(f"- **key**: {k}\n")
                out.write(f"- **default**: {default}\n")
                ex = extra if extra else "/"
                out.write(f"- **extra**: {ex}\n")


databases = {
    "mysql": _mysql
}


def main():

    if len(sys.argv) < 2:
        exit("Error: DB type not specified")
    if len(sys.argv) < 3:
        exit("Error: DB name not specified")
    if len(sys.argv) < 4:
        exit("Error: output filename not specified")

    db_type = sys.argv[1]
    db_name = sys.argv[2]
    file_name = sys.argv[3]
    slices = file_name.split(".")
    if (slices[-1] != 'md'):
        file_name = file_name + ".md"
    MODE = 1
    if len(sys.argv) == 5:
        MODE = int(sys.argv[4])

    func = databases.get(db_type)
    if not func:
        exit(f"Error: DB type '{db_type}' not valid")
    
    out = open(file_name, 'w+')
    func(db_name, out, MODE)
