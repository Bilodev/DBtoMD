import sqlite3
import re


def _sqlite(DB_USR, DB_PSW, db_name: str, out):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # -------------------------
    # Tables
    # -------------------------
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)

    tables = [row[0] for row in cursor.fetchall()]

    for t in tables:

        out.write(f"# {t}\n\n")

        # -------------------------
        # Columns
        # -------------------------
        cursor.execute(f"PRAGMA table_info('{t}')")

        out.write("## Columns\n\n")
        out.write("| Name | Type | Null | PK | Default |\n")
        out.write("|------|------|------|----|---------|\n")

        for cid, name, type_, notnull, default, pk in cursor.fetchall():
            out.write(
                f"| {name} | {type_} | {'NO' if notnull else 'YES'} | {'YES' if pk else '/'} | {default} |\n"
            )

        out.write("\n")

        # -------------------------
        # Foreign Keys
        # -------------------------
        cursor.execute(f"PRAGMA foreign_key_list('{t}')")
        fks = cursor.fetchall()

        if fks:
            out.write("### Foreign Keys\n\n")

            for _, _, ref_table, from_col, to_col, on_update, on_delete, _ in fks:
                out.write(
                    f"- **{from_col}** → {ref_table}({to_col}) "
                    f"(ON UPDATE {on_update}, ON DELETE {on_delete})\n"
                )

            out.write("\n")

        # -------------------------
        # Constraints
        # -------------------------
        cursor.execute("""
            SELECT sql
            FROM sqlite_master
            WHERE type='table'
            AND name=?
        """, (t,))

        row = cursor.fetchone()

        if row and row[0]:

            create_sql = row[0]

            constraints = []

            constraints += re.findall(
                r'CONSTRAINT\s+([^\s]+)',
                create_sql,
                re.IGNORECASE
            )

            if "PRIMARY KEY" in create_sql.upper():
                constraints.append("PRIMARY KEY")

            if "UNIQUE" in create_sql.upper():
                constraints.append("UNIQUE")

            if "CHECK" in create_sql.upper():
                constraints.append("CHECK")

            if "FOREIGN KEY" in create_sql.upper():
                constraints.append("FOREIGN KEY")

            if constraints:

                out.write("### Constraints\n\n")

                for c in sorted(set(constraints)):
                    out.write(f"- {c}\n")

                out.write("\n")

        # -------------------------
        # Indexes
        # -------------------------
        cursor.execute(f"PRAGMA index_list('{t}')")

        indexes = cursor.fetchall()

        if indexes:

            out.write("### Indexes\n\n")

            out.write("| Name | Columns | Unique |\n")
            out.write("|------|---------|--------|\n")

            for _, index_name, unique, *_ in indexes:

                cursor.execute(f"PRAGMA index_info('{index_name}')")

                cols = ", ".join(
                    col[2] for col in cursor.fetchall()
                )

                out.write(
                    f"| {index_name} | {cols} | {'Yes' if unique else 'No'} |\n"
                )

            out.write("\n")

        # -------------------------
        # Triggers
        # -------------------------
        cursor.execute("""
            SELECT name, sql
            FROM sqlite_master
            WHERE type='trigger'
            AND tbl_name=?
        """, (t,))

        triggers = cursor.fetchall()

        if triggers:

            out.write("### Triggers\n\n")

            out.write("| Name |\n")
            out.write("|------|\n")

            for name, _ in triggers:
                out.write(f"| {name} |\n")

            out.write("\n")

        out.write("\n---\n\n")

    conn.close()
