#not being used due to heroku restrictions


import sys
sys.path.insert(0, '..')



def exportCFG(epcs,path):
    outputpath=path+r"\newfile.cfg"
    file1 = open(outputpath, "w+")#append mode
    file1.seek(0)  # <- This is the missing piece
    file1.truncate()



    for i in epcs:
    #print(i.id, '  ', i.AttName, '  ', i.AttValue)
        first=str(i.AttName)
        if i.AttValue == None:
            second = ''
        else:
            second=' '+str(i.AttValue) +'\n'

        file1.writelines(first + second)

    print("config file generated.")
    file1.close()



