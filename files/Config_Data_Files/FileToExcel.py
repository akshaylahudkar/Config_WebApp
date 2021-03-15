import pandas as pd
file1 = open('nps_nodes.cfg', 'r', encoding="utf8")
list1 = []
cleanList = []
Lines = file1.readlines()

for line in Lines:
    if '=' in line:
        list1.append(line.strip().split('='))
    else:
        list1.append(line.strip().split())


print(list1)

for i in list1:
        if len(i) == 2:
            if i[0] != "":
                cleanList.append(i)
        elif len(i) == 1 and '#' not in i[0]:
            if i[0] != "":
                i.append("")
                cleanList.append(i)

df = pd.DataFrame(cleanList)
print(df)

#reader = pd.read_excel('AttributeTypeMapping.xlsx')
# write out the new sheet
writer = pd.ExcelWriter("Excel File Name", engine='openpyxl')

df.to_excel(writer, index=False)

writer.save()
#df.to_excel('AttributeTypeMapping.xlsx',index=False,header=False,startrow=len(reader)+1)
print('Data Added')