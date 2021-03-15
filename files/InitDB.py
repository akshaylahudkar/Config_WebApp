import sys
sys.path.insert(0, '..')

from app import db

db.drop_all()
db.create_all()