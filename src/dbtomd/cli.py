#!/bin/

import sys
import os

DB_USR = os.environ["DB_USR"]
DB_PSW = os.environ["DB_PSW"]


def _mysql(db_name: str, out):
    import mysql.connector

    db = mysql.connector.connect(
        host="localhost",
        user=DB_USR,
        password=DB_PSW
    )

    cursor = db.cursor()

    cursor.execute(f"USE {db_name}")
    cursor.execute("SHOW TABLES")

    tables = [table_name for (table_name,) in cursor]

    for t in tables:
        out.write(f"# {t}\n\n")

        # -------------------------
        # Columns
        # -------------------------
        cursor.execute(f"DESCRIBE `{t}`")

        out.write("## Columns\n\n")
        out.write("| Name | Type | Null | Key | Default | Extra |\n")
        out.write("|------|------|------|-----|---------|-------|\n")

        for res in cursor:
            name, type_, null, key, default, extra = res
            out.write(
                f"| {name} | {type_} | {null} | {key or '/'} | {default} | {extra or '/'} |\n"
            )
        out.write("\n")

        # -------------------------
        # Foreign Keys
        # -------------------------
        cursor.execute("""
            SELECT
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA=%s
              AND TABLE_NAME=%s
              AND REFERENCED_TABLE_NAME IS NOT NULL
        """, (db_name, t))

        rows = cursor.fetchall()

        if rows:
            out.write("### Foreign Keys\n\n")

            for column, ref_table, ref_column in rows:
                out.write(
                    f"- **{column}** → {ref_table}({ref_column})\n"
                )

            out.write("\n")

        # -------------------------
        # Constraints
        # -------------------------
        cursor.execute("""
            SELECT
                CONSTRAINT_NAME,
                CONSTRAINT_TYPE
            FROM information_schema.TABLE_CONSTRAINTS
            WHERE TABLE_SCHEMA=%s
              AND TABLE_NAME=%s
        """, (db_name, t))

        rows = cursor.fetchall()

        if rows:
            out.write("### Constraints\n\n")

            out.write("| Name | Type |\n")
            out.write("|------|------|\n")

            for name, ctype in rows:
                out.write(f"| {name} | {ctype} |\n")

            out.write("\n")

        # -------------------------
        # Indexes
        # -------------------------
        cursor.execute("""
            SELECT
                INDEX_NAME,
                COLUMN_NAME,
                NON_UNIQUE
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA=%s
              AND TABLE_NAME=%s
            ORDER BY INDEX_NAME, SEQ_IN_INDEX
        """, (db_name, t))

        rows = cursor.fetchall()

        if rows:
            out.write("### Indexes\n\n")

            out.write("| Name | Column | Unique |\n")
            out.write("|------|--------|--------|\n")

            for name, column, non_unique in rows:
                unique = "Yes" if non_unique == 0 else "No"
                out.write(f"| {name} | {column} | {unique} |\n")

            out.write("\n")

        # -------------------------
        # Triggers
        # -------------------------
        cursor.execute("""
            SELECT
                TRIGGER_NAME,
                ACTION_TIMING,
                EVENT_MANIPULATION
            FROM information_schema.TRIGGERS
            WHERE TRIGGER_SCHEMA=%s
              AND EVENT_OBJECT_TABLE=%s
        """, (db_name, t))

        rows = cursor.fetchall()

        if rows:
            out.write("### Triggers\n\n")

            out.write("| Name | Timing | Event |\n")
            out.write("|------|--------|-------|\n")

            for name, timing, event in rows:
                out.write(f"| {name} | {timing} | {event} |\n")

        out.write("\n---\n")


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

    func = databases.get(db_type)
    if not func:
        exit(f"Error: DB type '{db_type}' not valid")

    out = open(file_name, 'w+')
    func(db_name, out)
