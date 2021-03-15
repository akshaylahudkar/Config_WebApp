import sys
sys.path.insert(0, '../..')

from app import ENUM_Nodes, db
def AddtoEnum():
    file1 = open('../Config_Data_Files/enum_nodes.cfg', 'r', encoding="utf8")
    list1 = []
    cleanList = []
    Lines = file1.readlines()

    for line in Lines:
        list1.append(line.strip().split('='))

    for i in list1:
        if len(i) == 2:
            if i[0] != "":
                cleanList.append(i)
        elif len(i) == 1:
            if i[0] != "":
                i.append("")
                cleanList.append(i)

    print(cleanList)
    db.session.query(ENUM_Nodes).delete()
    db.session.commit()

    #print(cleanList)
    for i in cleanList:

        enumObj = None
        try:
            #print(i[0], i[1])
            enumObj = ENUM_Nodes(AttName=str(i[0]), AttValue=str(i[1]))
            db.session.add(enumObj)

        except Exception as e:
            print("Failed to add Attribute")
            print(e)

    db.session.commit()
    print("ENUM Config file data added to DB Successfully")

