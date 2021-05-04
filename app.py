from flask import Flask ,request, jsonify , json , make_response
import psycopg2  
import checkEmail , checkPassword , getAccountInfo , hasDoorAccess


app = Flask(__name__)




@app.route("/checkUser",methods = ["POST"])
def UrlCheckUser():
   if request.method == "POST":
 
      ParsedEmail = JsonParse()
      response = checkEmail.IsRegistered(ParsedEmail['email'])

      return make_response(response)


@app.route("/checkPassword",methods = ["POST"])
def UrlCheckPassword():
   if request.method == "POST":
      
      ParsedInfo = JsonParse()
      response = checkPassword.IsPasswordCorrect(ParsedInfo['email'] , ParsedInfo['password'] )

      return make_response(response) 




@app.route("/getAccountDetails",methods = ["POST"])
def UrlGetAccountDetails():
   if request.method == "POST":     

      ParsedInfo = JsonParse()    
      response = getAccountInfo.accountInfoFunc(ParsedInfo['contactId'] , ParsedInfo['accountId'] )
      
      return "POST ISTEĞİ ALINDI"
   
      return make_response(response) 




@app.route("/hasDoorAccess",methods = ["POST"])
def UrlHasDoorAccess():
   if request.method == "POST":

      ParsedInfo = JsonParse()    
      response = hasDoorAccess.doorAccessFunc(ParsedInfo['contactId'] , ParsedInfo['accountId'] ,ParsedInfo['doorId'] )

      return make_response(response) 







@app.route("/test",methods = ["GET"])
def deneme():
   if request.method == "GET":

      return '<h1>Hello html again</h1>'
  

  
         


#Gelen isteklerin tümünün parse edilmesi işlemleri.

def JsonParse():
   data = request.get_json()

   if data.get('mailAddress') != None :
      userEmail = data['mailAddress']
   else :
      userEmail = None

   if data.get('password') != None :
      userPw = data['password']
   else:
      userPw = None

   if data.get('accountId') != None :
      accountId = data['accountId']
   else:
      accountId = None

   if data.get('contactId') != None :
      contactId = data['contactId']
   else:
      contactId = None

   if data.get('doorId') != None :
      doorId = data['doorId']
   else:
      doorId = None




   return {'email' : userEmail , 'password' : userPw , 'accountId' : accountId , 'contactId' : contactId , 'doorId' : doorId }





if __name__=="__main__":
    app.run(debug = False)




