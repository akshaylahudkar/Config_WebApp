import os
import shutil
import sys
from csv import writer
from flask import Flask
from flask import render_template,json, send_file
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr
from flask import flash
from switch import Validation

sys.path.insert(0, '../..')



APP_ROOT = os.path.dirname(os.path.abspath(__file__))  #to get current working directory path

DbObj = None
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "attribute_database.db"))

app = Flask(__name__)
toastr = Toastr(app)
#app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://blwznjoaexpigs:f5062347d05f6ce0bd9aa552f08c5ad32e159e6838c43f7e16e6ebddb9f884f0@ec2-52-6-178-202.compute-1.amazonaws.com:5432/ddfaffh9g9ntns'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)

'''
########################################### DB Table Class ####################################################
'''

class EPC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    AttName = db.Column(db.String(255), nullable=False)
    AttValue = db.Column(db.String(255),nullable=True)

    @property
    def first_item(self):
        # the problem is here:
        return self.id.order_by(id.asc()).first()

    def __repr__(self):
        return "<AttName: {},AttValue:{}>".format(self.AttName,self.AttValue)

class EPCTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    AttName = db.Column(db.String(255), nullable=False)
    AttType = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return "<Title: {},Value:{}>".format(self.AttName, self.AttType)
#DB for IMS Config file
class IMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    AttName = db.Column(db.String(255), nullable=False)
    AttValue = db.Column(db.String(255),nullable=True)

    @property
    def first_item(self):
        # the problem is here:
        return self.id.order_by(id.asc()).first()

    def __repr__(self):
        return "<AttName: {},AttValue:{}>".format(self.AttName,self.AttValue)

#DB for NPS_Nodes Config file
class NPS_Nodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    AttName = db.Column(db.String(255), nullable=False)
    AttValue = db.Column(db.String(255),nullable=True)

    @property
    def first_item(self):
        # the problem is here:
        return self.id.order_by(id.asc()).first()

    def __repr__(self):
        return "<AttName: {},AttValue:{}>".format(self.AttName,self.AttValue)

#DB for ENUM_Nodes Config file
class ENUM_Nodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    AttName = db.Column(db.String(255), nullable=False)
    AttValue = db.Column(db.String(255),nullable=True)

    @property
    def first_item(self):
        # the problem is here:
        return self.id.order_by(id.asc()).first()

    def __repr__(self):
        return "<AttName: {},AttValue:{}>".format(self.AttName,self.AttValue)

#DB for New File comparision
class EPCNewVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    AttName = db.Column(db.String(255), nullable=False)
    AttValue = db.Column(db.String(255),nullable=True)

    @property
    def first_item(self):
        # the problem is here:
        return self.id.order_by(id.asc()).first()

    def __repr__(self):
        return "<AttName: {},AttValue:{}>".format(self.AttName,self.AttValue)

'''
####################################### Flask Methods ###################################
'''
filetype = ""
filelist = []
newAttributeList = []
removedAttributeList = []
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  #set file max cache time to 0 sec -- Siddhant Jain

@app.after_request # processed after each request & data will not stored in cache -- Siddhant Jain
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/', methods=["GET", "POST"])
def getfiletype():
    filetype = request.form.get("filetype")

    print("filetype in getfilename ="+str(filetype))

    return render_template("home_2.html", filetype =filetype)

@app.route('/display', methods=["GET", "POST"])
def display():


    epc = None
    epcTypeObj = None
    if request.form:
        filetype = request.form.get("filetype")
        filelist.append(filetype)


    filetype = filelist[-1]
    print("filetype in display =" + str(filetype))

    if filetype == "epc":
        DbObj = EPC
    elif filetype == "ims":
        DbObj = IMS
    elif filetype == "nps":
        DbObj = NPS_Nodes
    elif filetype == "enum":
        DbObj = ENUM_Nodes

    epcs = DbObj.query.order_by(DbObj.id.asc()).all()
    epcType = EPCTypes.query.all()
    TypeList = []
    for i in epcType:
        if i.AttType not in TypeList:
            TypeList.append(i.AttType)
    print(TypeList)

    return render_template("home_2.html", epcs=epcs,epct=TypeList, filetype = filetype)

@app.route("/addtoDB", methods=["GET","POST"])

def addAttribute():

    #filetype = request.form.get("filetype")
    filetype = filelist[-1]
    print("filetype in addAttribute =" + str(filetype))
    if filetype == "epc":
        DbObj = EPC
    elif filetype == "ims":
        DbObj = IMS
    elif filetype == "nps":
        DbObj = NPS_Nodes
    elif filetype == "enum":
        DbObj = ENUM_Nodes

    if request.form:

        try:
            AttName = request.form.get("AttName")
            AttValue = request.form.get("AttValue")
            AttType = request.form.get("newAttrType")

            epc = DbObj(AttName=AttName,AttValue=AttValue)
            epctobj = EPCTypes(AttName=AttName, AttType=AttType)
            db.session.add(epctobj)
            db.session.add(epc)
            db.session.commit()
            list_of_elem = [AttName, AttType]
            with open('../Final_ConfigFile/files/Database_Loading/MappingData.csv', 'a+', newline='') as write_obj:
                # Create a writer object from csv module
                csv_writer = writer(write_obj)
                # Add contents of list as last row in the csv file
                csv_writer.writerow(list_of_elem)
                print("AttrType added to CSV Successfully")

            flash("New Record {} added Successfully with value {}"
                  .format(request.form.get("AttName"),request.form.get("AttValue")), 'success')
        except Exception as e:
            print("Failed to add Attribute")
            flash("Invalid Record", 'error')
            print(e)

    return redirect('/display')




@app.route("/update", methods=["Get","POST"])

def update():

    #filetype = request.form.get("filetype")

    filetype = request.form.get("filetype")
    print("filetype in update =" + str(filetype))
    if filetype == "epc":
        DbObj = EPC
    elif filetype == "ims":
        DbObj = IMS
    elif filetype == "nps":
        DbObj = NPS_Nodes
    elif filetype == "enum":
        DbObj = ENUM_Nodes


    try:
        oldAttValue = request.form.get("oldAttValue")
        newAttValue = request.form.get("newAttValue")
        AttName = request.form.get("AttName")
        epcTypeObj = EPCTypes.query.filter_by(AttName=AttName).first()
        print('Attribute_type', epcTypeObj.AttType)

        #call validation
        ob = Validation()
        print('newAtt',newAttValue)

        if epcTypeObj.AttType == 'DATE':  # Date conversion to format dd-mm-yyyy
            if newAttValue[2] != '-':
                newDate = newAttValue.split('-')
                newDate = newDate[::-1]
                newAttValue = "-".join(newDate)

        #print(ob.ValidationFunction(newAttValue, epcTypeObj.AttType))

        if ob.ValidationFunction(newAttValue,epcTypeObj.AttType):
            print("successful switch")
            epc = DbObj.query.filter_by(AttValue=oldAttValue,AttName=AttName).first()
            epc.AttValue = newAttValue
            db.session.commit()
            print("Update Complete")
            flash("New Value {} Updated Successfully for {}".format(newAttValue, AttName), 'success')
        else:
            flash("Invalid {} for field {}".format(epcTypeObj.AttType, AttName), 'error')

    except Exception as e:
        print("Couldn't update Attribute")
        flash("Invalid Operation", 'error')
        print(e)

    return redirect("/display")

@app.route("/delete", methods=["POST"])
def delete():
    filetype = request.form.get("filetype")

    if filetype == "epc":
        DbObj = EPC
    elif filetype == "ims":
        DbObj = IMS
    elif filetype == "nps":
        DbObj = NPS_Nodes
    elif filetype == "enum":
        DbObj = ENUM_Nodes
    try:
        AttName = request.form.get("AttName")
        epc = DbObj.query.filter_by(AttName=AttName).first()
        db.session.delete(epc)
        db.session.commit()
        flash("Parameter {} deleted Successfully".format(AttName), 'success')
    except:
        print("Couldn't delete Attribute")
        flash("Delete failed for {}".format(AttName), 'error')

    return redirect("/display")


'''
@app.route("/downloadCFG")
def get_cfg():


    #db.session.commit()
    file_folder = project_dir + r"\iles"
    db.session.commit()
    epcs = 0
    epcs = EPC.query.order_by(EPC.id.asc()).all()
    exportCFG(epcs, file_folder)
    print('EPCS starts')
    for i in epcs:
        print(i.AttName,' ',i.AttValue)

    app.config['UPLOAD_FOLDER'] = file_folder

    filename=r"newfile.cfg"
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename, as_attachment=True)
'''

@app.route('/download_file', methods =["GET", "POST"])
def download_file():
    if request.form:
        filetype = request.form.get("filetype")
    else:
        filetype = filelist[-1]
    print("FileType in Download:- " + str(filetype))
    if filetype == "epc":
        DbObj = EPC
        newFile = "epc_config.cfg"
    elif filetype == "ims":
        DbObj = IMS
        newFile = "ims_config.cfg"
    elif filetype == "nps":
        DbObj = NPS_Nodes
        newFile = "nps_config.cfg"
    elif filetype == "enum":
        DbObj = ENUM_Nodes
        newFile = "enum_config.cfg"
    #print(APP_ROOT)
    path = os.path.join(APP_ROOT, 'User_Modified_File/')
    print("Path:-", path)
    if os.path.isdir(path):
        print("Inside Directory check>>>")
        shutil.rmtree(path)
    try:
        var = DbObj.query.order_by(DbObj.id.asc()).all()
        fileData = ''
        for i in var:

            first = str(i.AttName)
            if i.AttValue == None:
                second = ''
            else:
                if filetype == "enum" or filetype == "nps":
                    second = '=' + str(i.AttValue) + '\n'
                else:
                    second = ' ' + str(i.AttValue) + '\n'
            fileData += first+second
        #print(list1)
        target = os.path.join(APP_ROOT, 'User_Modified_File/')  # created target folder in current working
        print("Target=" + target)

        if not os.path.isdir(target):
            os.mkdir(target)
        destination = "/".join([target, newFile])
        print("Download Destination =", destination)
        f = open(destination, "w")
        f.write(fileData)
        f.close()
        #flash("{} File Downloaded Successfully..!!!".format(newFile), 'success')
    except Exception as e:
        flash("Unable to Download file..!!!", 'error')
        print(e)

    #Enable below code to download file from front end  -- Siddhant Jain #

    data=json.dumps(fileData)
    file_name = json.dumps(filetype)
    return render_template("gen_file.html", data=data, filename = file_name)


    # Below send_file method is for file dwnlod through backend
    #return send_file(destination, as_attachment=True, cache_timeout=0)


@app.route("/upload", methods = ['POST', 'GET'])
def fileupload():
    filetype = filelist[-1]
    return render_template("UploadFile.html", filetype = filetype)

@app.route("/savefile", methods = ['POST', 'GET'])
def savefile():
        if request.form:
            filetype = request.form.get("filetype")
        else:
            filetype = filelist[-1]
        target = os.path.join(APP_ROOT, 'User_Uploads/')
        print("Target="+ target)

        if not os.path.isdir(target):
            os.mkdir(target) #created target folder in current working
        for file in request.files.getlist("file"):
            print(file)
            filename = file.filename
            filenamesplit = filename.split('.')
            fileExtention = filenamesplit[-1]
            destination = "/".join([target, filename])
            print("Dest =" + destination)
            try:
                file.save(destination)
            except Exception as e:
                print("unable to save file")
                print(e)
        if fileExtention == 'cfg' or fileExtention == 'config':

            db.session.execute('DROP TABLE IF EXISTS epc_new_version')
            db.create_all()
            try:
                file1 = open(destination, 'r', encoding="utf8")
                list1 = []
                cleanList = []
                Lines = file1.readlines()

                for line in Lines:
                    if '=' in line:
                        list1.append(line.strip().split('='))
                    else:
                        list1.append(line.strip().split())
                file1.close()
                for i in list1:
                    if len(i) == 2:
                        if i[0] != "":
                            cleanList.append(i)
                    elif len(i) == 1:
                        if i[0] != "":
                            i.append("")
                            cleanList.append(i)

                for i in cleanList:
                    epcObj = None
                    try:

                        epcObj = EPCNewVersion(AttName=str(i[0]), AttValue=str(i[1]))
                        db.session.add(epcObj)

                    except Exception as e:
                        print("Failed to add Attribute")
                        print(e)
            except Exception as e:
                print(e)

            db.session.commit()
            try:
                os.remove(destination)
            except Exception as e:
                print("unable to remove file")
                print(e)
            return redirect("/displayCompare")
        else:
            shutil.rmtree(target)
            flash("Please upload a valid config file..!!!", 'error')
            return render_template("UploadFile.html", filetype = filetype)

@app.route("/displayCompare", methods=['POST', 'GET'])
def dispalyComparefile():
    try:
        if request.form:
            filetype = request.form.get('filetype')
            filelist.append(filetype)
        else:
            filetype = filelist[-1]
        if filetype == "epc":
            NewObj = EPC
            table_name = 'EPC'
        elif filetype == "ims":
            NewObj = IMS
            table_name = 'IMS'
        elif filetype == "nps":
            NewObj = NPS_Nodes
            table_name = 'NPS_Nodes'
        elif filetype == "enum":
            NewObj = ENUM_Nodes
            table_name = 'Enum_Nodes'

        epc = NewObj.query.all()

        newEPC = EPCNewVersion.query.all();

        # print('NewObj',NewObj)
        removed_elements = db.session.execute(
            'SELECT AttName FROM ' + str(table_name) + ' EXCEPT SELECT AttName FROM epc_new_version')
        added_elements = db.session.execute(
            'SELECT AttName FROM epc_new_version EXCEPT SELECT AttName FROM ' + str(table_name))


        print(filelist[-1])


        newAttributeList[:] = added_elements
        print("Added Attributes")
        print(newAttributeList)
        print('removed_elements')
        removedAttributeList[:] = removed_elements
        print(removedAttributeList)

        ae = []
        re = []
        for i in newAttributeList:
            ae.append(list(db.session.execute('SELECT AttName, AttValue FROM epc_new_version WHERE AttName = '+ "'" + str(i[0]) + "'")))

        for i in removedAttributeList:
            re.append(list(db.session.execute('SELECT AttName, AttValue FROM ' + str(table_name) + ' WHERE AttName = '+ "'" + str(i[0]) + "'")))
        print(re)
        print(ae)
        flash("File Uploaded & Compared with {} file Successfully".format(filetype), 'success')

    except Exception as e:
        flash("File Comparison failed..!!!", 'error')
        print(e)

    return render_template("UploadFile.html", msg = "file Uploaded Successfully", filetype = filetype, removed_elements = re, added_elements = ae, savefileFlag = "True")







'''
@app.route("/NewAddDelete", methods=["POST", "GET"])
def New_Add_Delete():
    try:
        if request.form:
            filetype = request.form.get('filetype')
            filelist.append(filetype)
        else:
            filetype = filelist[-1]
        if filetype == "epc":
            NewObj = EPC
            table_name = 'EPC'
        elif filetype == "ims":
            NewObj = IMS
            table_name = 'IMS'
        elif filetype == "nps":
            NewObj = NPS_Nodes
            table_name = 'NPS_Nodes'
        elif filetype == "enum":
            NewObj = ENUM_Nodes
            table_name = 'Enum_Nodes'

        epc = NewObj.query.all()

        newEPC = EPCNewVersion.query.all();

        # print('NewObj',NewObj)
        removed_elements = db.session.execute(
            'SELECT AttName FROM ' + str(table_name) + ' EXCEPT SELECT AttName FROM epc_new_version')
        added_elements = db.session.execute(
            'SELECT AttName FROM epc_new_version EXCEPT SELECT AttName FROM ' + str(table_name))

        for i in removed_elements:
            print(i[0])
            db.session.execute('DELETE FROM EPC WHERE AttName="' + str(i[0]) + '"')
            # db.session.commit()
        print('added_elements')
        for i in added_elements:
            # temp_value = db.session.execute('SELECT AttValue FROM epc_new_version WHERE AttName="'+str(i[0])+'"')
            epc = EPCNewVersion.query.filter_by(AttName=i[0]).first()
            epcObj = NewObj(AttName=epc.AttName, AttValue=epc.AttValue)
            db.session.add(epcObj)
            print(epc.AttName, epc.AttValue)

        db.session.commit()
        flash("File {} modified successfully w.r.t. comparison".format(filetype), 'success')


    except Exception as e:
        flash(" Unable to Modify {} file..!!!".format(filetype), 'error')
        print(e)
    return redirect('/display')

'''
    ########## End flask method here and pass removed elements and added_elements as parameter to render_temp#
'''
    for i in removed_elements:
        print(i)
        db.session.execute('DELETE FROM EPC WHERE id=' + str(i.id))

    print('added_elements')
    for i in added_elements:
        epcObj = EPC(AttName=i.AttName, AttValue=i.AttValue)
        db.session.add(epcObj)
        print(i)
    db.session.commit()

    print('end of elements')
    os.remove(destination)

    return render_template("UploadFile.html", msg="file Uploaded Successfully")
'''
@app.route("/addtoDBCompare", methods=["GET","POST"])

def addAttribute_Compare():
    if request.form:
        filetype = request.form.get('filetype')
        filelist.append(filetype)
    else:
        filetype = filelist[-1]
    print("filetype in addAttribute =" + str(filetype))
    if filetype == "epc":
        DbObj = EPC
    elif filetype == "ims":
        DbObj = IMS
    elif filetype == "nps":
        DbObj = NPS_Nodes
    elif filetype == "enum":
        DbObj = ENUM_Nodes

    if request.form:

        try:
            AttName = request.form.get("AttName")
            AttValue = request.form.get("newAttValue")
            AttType = request.form.get("newAttrType")

            epc = DbObj(AttName=AttName,AttValue=AttValue)
            epctobj = EPCTypes(AttName=AttName, AttType=AttType)
            db.session.add(epctobj)
            db.session.add(epc)
            db.session.commit()

            list_of_elem = [AttName, AttType]
            with open('../Final_ConfigFile/files/Database_Loading/MappingData.csv', 'a+', newline='') as write_obj:
                # Create a writer object from csv module
                csv_writer = writer(write_obj)
                # Add contents of list as last row in the csv file
                csv_writer.writerow(list_of_elem)
                print("AttrType added to CSV Successfully")
            flash("New Record {} added Successfully with value {} to {} file"
                  .format(request.form.get("AttName"),request.form.get("newAttValue"), request.form.get("filetype")), 'success')
        except Exception as e:
            print("Failed to add Attribute")
            flash("Invalid Record", 'error')
            print(e)

    return redirect("/displayCompare")

@app.route("/delete_Compare", methods=["POST"])
def delete_Compare():

    if request.form:
        filetype = request.form.get('filetype')
        filelist.append(filetype)
    else:
        filetype = filelist[-1]

    if filetype == "epc":
        DbObj = EPC
    elif filetype == "ims":
        DbObj = IMS
    elif filetype == "nps":
        DbObj = NPS_Nodes
    elif filetype == "enum":
        DbObj = ENUM_Nodes
    try:
        AttName = request.form.get("AttName")
        epc = DbObj.query.filter_by(AttName=AttName).first()
        db.session.delete(epc)
        db.session.commit()
        flash("Parameter {} deleted Successfully from {} file.".format(AttName, filetype), 'success')
    except Exception as e:
        print("Couldn't delete Attribute")
        flash("Delete failed for {}".format(AttName), 'error')
        print(e)

    return redirect("/displayCompare")



if __name__ == "__main__":
    app.run(debug=True)