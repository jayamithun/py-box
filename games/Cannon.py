from flask import Flask, render_template, jsonify, request,redirect,flash, Markup,url_for, session
from models import *
from datetime import date

folder_name="static"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/inventoryDB"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b'hkahs3720/'
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/logout")
def logout():
    return render_template("index.html")    
    
@app.route("/dashboard", methods=["POST"])
def dashboard():
    unam = request.form.get("username")
    pwd = request.form.get("password")
    
    ulist=user_tbl.query.filter_by(userName=unam).first()
    session['username']= unam
    session['userid']= ulist.userID
    session['utype']= ulist.userType
    if ulist.pwd==pwd:
       # uid=ulist.userid
        return render_template("dashboard.html")
    else:  
        return render_template("index.html")
    

@app.route("/saveItemCategory", methods=["POST"])
def saveItemCategory():
    idesc = request.form.get("ItemCategoryDesc")
    ItemCategor = ItemCategory(ItemCatDesc=idesc)
    db.session.add(ItemCategor)  
    db.session.commit()
    text=idesc+'record Saved Successfully'
    return render_template("dashboard.html", text=text)  
    
@app.route("/ItemsCategory")    
def ItemsCategory():
    catList=ItemCategory.query.all()
    tabl='''<div class="form-group">
            <table class="table table-bordered border-success" ><TH>
            <TD>Item Category ID</TD>
            <TD>Item Category Name</TD></TH>'''  
    for itm in catList:
        tabl=tabl+"<TR ><td></td><TD>"+str(itm.ItemCatID)+"</TD><TD>"+itm.ItemCatDesc+"</TD></TR>"
    tabl=tabl+"</TABLE></div>"   
    strg='''<form action="/saveItemCategory" method="post">
    <div class="text-center"><h5>Add Item Category</h5></div><hr>
<div class="mb-3">
  <label for="ItemCategoryDesc" class="form-label">Item Category Description</label>
  <input type="text" class="form-control" name="ItemCategoryDesc" placeholder="Enter Item Category Name">
</div>
<div class="col-12">
    <button type="submit" class="btn  btn-success mb-3">Save Item Category</button>
</div>

</FORM>
<BR>
'''+tabl
    text= Markup(strg)
    return render_template("dashboard.html", text=text)   

@app.route("/saveItem", methods=["POST"])
def saveItem():
    icatID = int(request.form.get("ItemCatID"))
    itmNam = request.form.get("ItemName")
    AvAmt = int(request.form.get("AvailAmt"))
    ItemMas = ItemMaster(ItemCatID=icatID, ItemDesc=itmNam,AvailAmt=AvAmt )
    db.session.add(ItemMas)  
    db.session.commit()
    text=itmNam+' record Saved Successfully'
    return render_template("dashboard.html", text=text) 
    
@app.route("/Items")    
def Items():
    itmList= ItemMaster.query.all()
    tabl='''<div class="form-group">
            <table class="table table-bordered border-success" ><TH>
            <TD>Item ID</TD>
            <TD>Item Category</TD>
            <TD>Item Name</TD></TH>'''  
    for itm in itmList:
        tabl=tabl+"<TR ><td></td><TD>"+str(itm.ItemID)+"</TD><TD>"+itm.ItemDesc+"</TD><TD>"+itm.itemCat.ItemCatDesc+"</TD></TR>"
    tabl=tabl+"</TABLE></div>"  
    catList= ItemCategory.query.all()
    dd='''<div class="form-group">
            <select class="form-control" name="ItemCatID">'''
    for cat in catList:
        dd=dd+"<option value=\""+str(cat.ItemCatID)+"\">"+cat.ItemCatDesc +"</option>"
    dd=dd+  '''</select>
</div>'''  
    
    
    strg='''<form action="/saveItem" method="post">
<div class="text-center"><h5>Add Items</h5></div><hr>
<div class="mb-3">
  <label for="ItemCatID" class="form-label">Item Category </label>'''+dd+'''
  
</div>
<div class="mb-3">
  <label for="ItemName" class="form-label">Item Description</label>
  <input type="text" class="form-control" name="ItemName" placeholder="Enter Item Name">
</div>
<div class="mb-3">
  <label for="AvailAmt" class="form-label">Available Amount</label>
  <input type="text" class="form-control" name="AvailAmt" placeholder="How many Items available?">
</div>
<div class="col-12">
    <button type="submit" class="btn  btn-success mb-3">Save Item</button>
</div>
</FORM>
<BR>
'''+tabl
    
    text=Markup(strg)
    return render_template("dashboard.html", text=text)

@app.route("/UpdateItems", methods=["POST"])
def UpdateItems():
    iID = int(request.form.get("ItemID"))
    aDate = request.form.get("AddDate")
    aQty = int(request.form.get("AddQty"))
    vName = request.form.get("VendorName")
    aItems = AddItem(AddDate=aDate, AddQty=aQty,VendorName=vName, ItemID=iID)
    upVal = ItemMaster.query.filter_by(ItemID=iID).first()
    newUnits= upVal.AvailAmt
    upVal.AvailAmt = newUnits+aQty
    db.session.add(aItems)  
    db.session.commit()
    text=str(aQty)+' '+upVal.ItemDesc+' Added Successfully'
    return render_template("dashboard.html", text=text) 

@app.route("/AddItems")    
def AddItems():
    itmList= ItemMaster.query.all()
    tabl='''<div class="form-group">
            <table class="table table-bordered border-success" ><TH>
            <TD>Item ID</TD>
            <TD>Item Category</TD>
            <TD>Item Name</TD>
            <TD>Items Available</TD></TH>'''  
    for itm in itmList:
        tabl=tabl+"<TR ><td></td><TD>"+str(itm.ItemID)+"</TD><TD>"+itm.ItemDesc+"</TD><TD>"+itm.itemCat.ItemCatDesc+"</TD><TD>"+str(itm.AvailAmt)+"</TD></TR>"
    tabl=tabl+"</TABLE></div>"  
    dd='''<div class="form-group">
            <select class="form-control" name="ItemID">'''
    for itm in itmList:
        dd=dd+"<option value=\""+str(itm.ItemID)+"\">"+itm.ItemDesc +"</option>"
    dd=dd+  '''</select>
</div>''' 
    strg='''<form action="/UpdateItems" method="post">
<div class="text-center"><h5>Items Available</h5></div><hr>
<div class="mb-3">
  <label for="ItemID" class="form-label">Select Item </label>'''+dd+'''
</div>
<div class="mb-3">
  <label for="AddDate" class="form-label">Select Date</label>
  <input type="date" class="form-control" Name="AddDate" placeholder="Enter Date of Adding Items in Inventory">
</div>
<div class="mb-3">
  <label for="AddQty" class="form-label">Items Count</label>
  <input type="text" class="form-control" name="AddQty" placeholder="Items Count">
</div>
<div class="mb-3">
  <label for="VendorName" class="form-label">Vendor Name</label>
  <input type="text" class="form-control" name="VendorName" placeholder="Vendor Name">
</div>
<div class="col-12">
    <button type="submit" class="btn btn-success mb-3">Save Item</button>
</div>
</FORM><BR>
'''+tabl
    text=Markup(strg)
    return render_template("dashboard.html", text=text)  


@app.route("/issUpdt/<int:tid>")
def issUpdt(tid):
    
    ilist=request_tbl.query.filter_by(reqID=tid).first()
    upVal="I"
    ilist.Status=upVal
    ilist.issueDate= date.today()
    imlist=ItemMaster.query.filter_by(ItemID=ilist.ItemID).first()
    currCnt=imlist.AvailAmt
    imlist.AvailAmt=currCnt-ilist.ReqQty
    db.session.commit()
    text="Item Issued"
    return render_template("dashboard.html", text=text)

@app.route("/itemIssue")    
def itemIssue():
    itmList= request_tbl.query.filter_by(Status=None,)
    strg='''<Form><div class="form-group">
            <table class="table table-bordered border-success" ><TH>
            <TD>Item Name</TD>
            <TD>Date of Request</TD>
            <TD>Quantity Requested</TD>
            <TD>User Name</TD>
            <TD>Issue</TD></TH>'''  
    for itm in itmList:
        strg=strg+"<TR ><td></td><TD>"+str(itm.item.ItemDesc)+"</TD><TD>"+str(itm.ReqDate)+"</TD><TD>"+str(itm.ReqQty)+"</TD>"
        strg=strg+"<TD>"+str(itm.user.userName)+"</TD><TD>"
        strg=strg+"<div class=\"col-12\"><a href="+ url_for('issUpdt',tid=itm.reqID)+">Issue</a></div></TD></TR>"
    strg=strg+"</TABLE></div></FORM>"
    
    text=Markup(strg)
    return render_template("dashboard.html", text=text) 
  
@app.route("/retUpdt/<int:tid>")
def retUpdt(tid):
    ilist=request_tbl.query.filter_by(reqID=tid).first()
    upVal="R"
    ilist.Status=upVal
    ilist.returnDate= date.today()
    imlist=ItemMaster.query.filter_by(ItemID=ilist.ItemID).first()
    currCnt=imlist.AvailAmt
    imlist.AvailAmt=currCnt+ilist.ReqQty
    db.session.commit()
    text="Item Returned"
    return render_template("dashboard.html", text=text)
    
@app.route("/itemReturn")    
def itemReturn():
    itmList= request_tbl.query.filter_by(Status="I",userID=session['userid'])
    strg='''<Form><div class="form-group">
            <table class="table table-bordered border-success" ><TH>
            <TD>Item Name</TD>
            <TD>Date of Issue</TD>
            <TD>Quantity Issued</TD>
            <TD>Return</TD></TH>'''  
    for itm in itmList:
        strg=strg+"<TR ><td></td><TD>"+str(itm.item.ItemDesc)+"</TD><TD>"+str(itm.issueDate)+"</TD><TD>"+str(itm.ReqQty)+"</TD>"
        strg=strg+"<TD><div class=\"col-12\"><a href="+ url_for('retUpdt',tid=itm.reqID)+">Return</a></div></TD></TR>"
    strg=strg+"</TABLE></div></FORM>"
    
    text=Markup(strg)
    return render_template("dashboard.html", text=text)      
    
@app.route("/saveRequest", methods=["POST"])
def saveRequest():
    iID = int(request.form.get("ItemID"))
    rDate = request.form.get("reqDate")
    rQty = request.form.get("reqQuantity")
    uid = session["userid"]
    dept = request.form.get("depttName")
    rItems = request_tbl(ReqDeptt=dept, ReqDate=rDate,ItemID=iID, ReqQty=rQty, userID=uid)
    db.session.add(rItems)  
    db.session.commit()
    text=str(iID)+' '+str(rQty)+' Requested Successfully'
    return render_template("dashboard.html", text=text) 


@app.route("/itemRequest")    
def itemRequest():
    itmList= ItemMaster.query.all()
    dd='''<div class="form-group">
            <select class="form-control" name="ItemID">'''
    for itm in itmList:
        dd=dd+"<option value=\""+str(itm.ItemID)+"\">"+itm.ItemDesc +"</option>"
    dd=dd+  '''</select>
</div>''' 

    itmList= request_tbl.query.filter_by(userID=session['userid'])
    tbl='''<DIV><table class="table table-bordered border-success" ><TH>
            <TD>Item Name</TD>
            <TD>Date of Request</TD>
            <TD>Date of Issue</TD>
            <TD>Quantity Issued</TD></TH>'''  
    for itm in itmList:
        tbl=tbl+"<TR ><td></td><TD>"+str(itm.item.ItemDesc)+"</TD><TD>"+str(itm.ReqDate)+"</TD><TD>"+str(itm.issueDate)+"</TD>"
        tbl=tbl+"<TD>"+str(itm.ReqQty)+"</TD></TR>"
    tbl=tbl+"</TABLE></div>"    
    strg='''<form action="/saveRequest" method="post">
<div class="text-center"><h5>Request Item</h5></div><hr>
<div class="mb-3">
  <label for="ItemID" class="form-label">Select Item </label>'''+dd+'''
</div>
<div class="mb-3">
  <label for="reqDate" class="form-label">Request Date</label>
  <input type="date" class="form-control" name="reqDate" placeholder="Select Request Date">
</div>
<div class="mb-3">
  <label for="reqQty" class="form-label">Request Quantity</label>
  <input type="number" class="form-control" name="reqQuantity" placeholder="Items Count">
</div>
<div class="mb-3">
  <label for="depttName" class="form-label">Department</label>
  <input type="text" class="form-control" name="depttName" placeholder="Department ">
</div>
<div class="col-12">
    <button type="submit" class="btn btn-success mb-3">Request Item</button>
</div>
</FORM><BR>
'''+tbl
    text=Markup(strg)
    return render_template("dashboard.html", text=text)  