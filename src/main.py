#!/bin/

import mysql.connector
import sys
import os

db = mysql.connector.connect(
    host="localhost",
    user=os.environ["SQLUSER"],
    password=os.environ["SQLPSW"]
)

if len(sys.argv) < 2:
    exit("Error: DB name not specified")
if len(sys.argv) < 3:
    exit("Error: output filename not specified")

db_name = sys.argv[1]
file_name = sys.argv[2]
slices = file_name.split(".")
if (slices[-1] != 'md'):
    file_name = file_name + ".md"
MODE = 0
if len(sys.argv) == 4:
    MODE = int(sys.argv[3])

out = open(file_name, 'w+')

cursor = db.cursor()

cursor.execute(f"USE {db_name}")
cursor.execute("SHOW TABLES")

tables = [table_name for (table_name, ) in cursor]


if MODE == 0:
    for t in tables:
        out.write(f"# {t}\n")
        cursor.execute(f"DESCRIBE {t}")
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

if MODE == 1:
    for t in tables:
        out.write(f"# {t}\n")
        cursor.execute(f"DESCRIBE {t}")
        out.write("| name | type | null | key | default | extra |\n")
        out.write("|------|------|------|-----|---------|-------|\n")

        for res in cursor:
            name, type, null, key, default, extra = res
            k = key if key else "/"
            ex = extra if extra else "/"

            out.write(
                f"| {name} | {type} | {null} | {k} | {default} | {ex} |\n")
