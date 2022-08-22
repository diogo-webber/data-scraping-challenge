
import yaml
from scripts.Printer import Printer

# Data from docker-compose.yml to connected to the database.

def collect_db_credentials():
    with open("docker-compose.yml", "r") as file:
        _yml = yaml.safe_load(file)
        
    try:
        service = list(_yml["services"])[0]
        db =  _yml["services"][service]
        environment = db["environment"]
        
        return (
            f' host=localhost'
            f' dbname={environment["POSTGRES_DB"]}'
            f' user={environment["POSTGRES_USER"]}'
            f' password={environment["POSTGRES_PASSWORD"]}'
            f' port={db["ports"][0].split(":")[0]}'
        )
    except:
        Printer.fatal_error("INVALID_YML")

