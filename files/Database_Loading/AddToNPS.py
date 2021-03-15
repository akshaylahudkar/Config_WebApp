import sys
sys.path.insert(0, '../..')

from app import NPS_Nodes, db
def AddtoNPS():
    file1 = open('../Config_Data_Files/nps_nodes.cfg', 'r', encoding="utf8")
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


    db.session.query(NPS_Nodes).delete()
    db.session.commit()

    #print(cleanList)
    for i in cleanList:

        npsObj = None
        try:
            #print(i[0], i[1])
            npsObj = NPS_Nodes(AttName=str(i[0]), AttValue=str(i[1]))
            db.session.add(npsObj)

        except Exception as e:
            print("Failed to add Attribute")
            print(e)

    db.session.commit()
    print("NPS Config file data added to DB Successfully")

