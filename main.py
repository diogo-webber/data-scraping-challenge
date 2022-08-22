#!/usr/bin/env python

import subprocess
from datetime import date
import os

from scripts.Printer import Printer
from scripts.strings_misc import INSERT_SQL

def check_modules():
    """Check if all required modules are present."""
    try:
        from scrapy import __name__
        from yaml import __name__
        from psycopg2 import __name__
        
    except ModuleNotFoundError as error:
        Printer.fatal_error("MODULE_MISSING", module=str(error).removeprefix("No module named "))

date = date.today()
output_path = f"data/{date}/books.csv"

spider_path = "books_scraper/books_spider.py"
log_mode = "WARNING"

scrapy_command = f"scrapy runspider {spider_path} -L {log_mode} -O {output_path}"

def import_to_db(db) -> None:
    Printer.output_message("IMPORT")
    
    with open(output_path, encoding="utf-8") as file:
        db.import_data(INSERT_SQL, file)
        
    Printer.success()

def run_scrapy() -> None:
    Printer.output_message("SCRAPY")
    print()
    
    subprocess.run(scrapy_command.split())
    
    Printer.success()

def main() -> None:
    Printer.output_message("START")
    
    check_modules()
    
    from scripts.PostgresDatabase import PostgresDatabase
    from scripts.dbCredentials import collect_db_credentials
    
    if os.path.exists(output_path):
        Printer.skip_operation("CSV_EXIST", date=date)
        Printer.output_message("END")
        return
    
    db_credentials = collect_db_credentials()

    with PostgresDatabase(db_credentials) as db:
        run_scrapy() # Run scrapper only if the database connection is successful.
        import_to_db(db)

    Printer.output_message("END")

if __name__ == '__main__':
    main()
