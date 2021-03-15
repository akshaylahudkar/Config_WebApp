import sys

sys.path.insert(0, '../..')

from app import EPCTypes, db
import pandas as pd

def Add_DataTypes():
    #df = pd.read_excel('../Config_Data_Files/AttributeTypeMapping.xls', usecols = "A,C")
    #print(df)

    #mapping file changed to CSV
    #Below code is to convert CSV file to data frame

    df = pd.DataFrame(pd.read_csv("MappingData.csv"))

    mappingList = df.values.tolist()
    print(mappingList)
    CleanMappingList = []
    for item in mappingList:
        if '####' in item[0] or '#End#' in item[0]:
            continue
        else:
            CleanMappingList.append(item)

    print(CleanMappingList)

    db.session.query(EPCTypes).delete()
    db.session.commit()
    for i in CleanMappingList:

        epctypesObj = None
        try:
            epctypesObj = EPCTypes(AttName=str(i[0]), AttType=str(i[1]))
            db.session.add(epctypesObj)
        except Exception as e:
            print("Failed to add AttributeTypes")
            print(e)

    db.session.commit()
    print("Attribute Types added to DB Successfully")


