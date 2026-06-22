import sys
import os
from providers.mysql import _mysql
from providers.sqlite import _sqlite

DB_USR = os.environ["DB_USR"]
DB_PSW = os.environ["DB_PSW"]


databases = {
    "mysql": _mysql,
    "sqlite": _sqlite
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
    func(DB_USR, DB_PSW, db_name, out)
