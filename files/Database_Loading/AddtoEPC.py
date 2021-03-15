import sys
sys.path.insert(0, '../..')

from app import EPC, db,ENUM_Nodes,IMS,NPS_Nodes


def AddtoEPC():


    file1 = open('../Config_Data_Files/lte_epc.cfg', 'r', encoding="utf8")
    list1 = []
    cleanList = []
    Lines = file1.readlines()

    for line in Lines:
        list1.append(line.strip().split())

    for i in list1:
        if len(i) == 2:
            if i[0] != "":
                cleanList.append(i)
        elif len(i) == 1:
            if i[0] != "":
                i.append("")
                cleanList.append(i)


    db.session.query(EPC).delete()
    db.session.commit()

    #print(cleanList)
    for i in cleanList:

        epcObj = None
        try:
            #print(i[0], i[1])
            epcObj = EPC(AttName=str(i[0]), AttValue=str(i[1]))
            db.session.add(epcObj)

        except Exception as e:
            print("Failed to add Attribute")
            print(e)

    db.session.commit()
    print("EPC Config file data added to DB Successfully")
