INSERT_SQL = (
    " COPY books(title, category, stars, price_in_pounds, in_stock)"
    " FROM STDIN"
    " WITH HEADER CSV"
    " DELIMITER '|'"
    " NULL ''"
)

class messages:
    ERRORS = {
        'DB_OFFLINE' : 'Could not connect to the database.\nIt looks like it\'s offline, use "docker-compose up -d" to run it.',
        'DB_LOADING' : 'The database is still starting, wait a few seconds and try again.',
        'DB_FAIL' : 'Could not connect to the database...\n\nException:\n{error}',
        'MODULE_MISSING' :  'Required module {module} not found.',
        'INVALID_YML' :  'Something is wrong in the "docker-compose.yml file:\n\n{error}',
    }

    SKIPS = {
        'CSV_EXIST' : 'Data for date {date} already exists!',
    }

    OUTPUTS = {
        'START' : "Starting Pipeline Execution...",
        'END' : "All operations finalized.",
        'SCRAPY' : "Initing scraping",
        'IMPORT' : "Loading CSV file into database",
        'CREATE_CSV' : 'Creating "{file}" file',
    }

# -------------------------------------------------------------------- #

import re, os

def _colour(code):
    return f'\u001b[{code}m'

_can_handle_colours = os.getenv("TERM") or os.getenv("TERM_PROGRAM")

# -------------------------------------------------------------------- #

# Used by Printer.py
class cc:
    """Console Colours"""
    RED = _colour('31')
    YELLOW = _colour('33;1')
    GREEN = _colour('38;5;40')
    RESET = _colour('0')

# Used in other files.
def tint_text(msg, colour: cc):
    return (_can_handle_colours and colour + str(msg) + cc.RESET) or msg

# -------------------------------------------------------------------- #

def _tint_sub(colour):
    return lambda match: tint_text(match.group(0), colour)

def _tint_msg(msg: str, colour_fn, only_quoted: bool):
    quoted = re.sub('"(.*?)"', colour_fn, msg, re.M) # Color all quoted strings.
    if only_quoted: return quoted
    return re.sub('{(.*?)}', colour_fn, quoted, re.M) # Color all special parameters.

def _tint_msgs_dict(group: dict, colour: cc, only_quoted: bool=None):
    for key, msg in group.items():
        group[key] = _tint_msg(str(msg), _tint_sub(colour), only_quoted)

_tint_msgs_dict(messages.ERRORS, cc.RED)
_tint_msgs_dict(messages.SKIPS, cc.YELLOW)
_tint_msgs_dict(messages.OUTPUTS, cc.YELLOW)
