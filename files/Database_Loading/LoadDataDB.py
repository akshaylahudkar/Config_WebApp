import sys
sys.path.insert(0, '../..')

from app import EPC, db,ENUM_Nodes,IMS,NPS_Nodes
from AddtoEPC import *
from AddToNPS import *
from AddToIMS import *
from AddToENUM import *
from AddtoEPCTypes import *

db.drop_all()
db.create_all()
try:
    AddtoEPC()
    AddtoEnum()
    AddtoNPS()
    AddtoIMS()
    Add_DataTypes()
except Exception as e:
    print("Error in DB Loading")
    print(e)

print("DB loaded successfully...!!!!!")