from pymongo.errors import WriteError

from db.db_config import db

diagrams_col = db.diagrams

def save_diagrams_as_code(diagrams_as_code):
    try:
        diagrams_col.insert_one(diagrams_as_code)
        return True
    except WriteError:
        return False

def load_all_diagrams_as_code():
    try:
        return diagrams_col.find({})
    except WriteError:
        return False

def load_diagrams_as_code_by_name(diagram_name):
    try:
        return diagrams_col.find_one({"name": diagram_name})
    except WriteError:
        return False
