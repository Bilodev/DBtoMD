# Overview

This simple python script helps to create an agent friendly markdown file from a mysql local database

## Installation

`pip install git+https://github.com/TUO_USERNAME/dbtomd.git`

## Usage

```bash
export DB_USR="username"
export DB_PSW="password"
dbtomd db_type db_name output_file mode(default=1)
```

This tool supports:
- `db_type="mysql"`

## Output 
In the output file, for each table, there will be a "summary" like this: 

![alt text](table.png)