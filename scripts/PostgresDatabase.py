import psycopg2

from scripts.Printer import Printer


_str_db_offline = "Is the server running"
_str_db_loading = "server terminated abnormally"

def _handle_connection_error(error: Exception) -> None:
    """Handle exceptions by text, because the exception it's the same."""

    error_str = str(error)
    
    error_type = (
        _str_db_offline in error_str and "DB_OFFLINE" or
        _str_db_loading in error_str and "DB_LOADING" or 
        None
    )

    if error_type:
        return Printer.fatal_error(error_type)

    return Printer.fatal_error("DB_FAIL", error=error_str)

class PostgresDatabase():
    """
    Create a Postgres database connection.
    
    Parameters:
        `credentials_str`: str - a database credential dsn string.
    """
    
    def __init__(self, credentials_str) -> None:
        self.credentials_dsn = credentials_str
        
        self.conn = None
        self.cur = None
        
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def connect(self):
        """Create the connection with the database."""
        try:
            self.conn = psycopg2.connect(self.credentials_dsn)
            self.cur = self.conn.cursor()
        except Exception as e:
            _handle_connection_error(error=e)

    def import_data(self, sql, file):
        """Execute a SQL copy query.

        Parameters:
            `sql`: str - the SQL copy query.
            `file`: IO - the file-like object to copy to/from
        """
        
        try:
            self.cur.copy_expert(sql, file)
        except Exception as error:
            self.conn.rollback()
            self.close_connection()
            raise error
        else:
            self.conn.commit()

    def close_connection(self):
        """Close the connection with the database."""
        self.cur.close()
        self.conn.close()
