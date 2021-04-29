from flask import Flask ,request, jsonify , json , make_response
import psycopg2  
import string , random
from dotenv import load_dotenv , find_dotenv
import os



app = Flask(__name__)




@app.route("/checkUser",methods = ["POST"])
def UrlCheckUser():
   if request.method == "POST":
 
      ParsedEmail = JsonParse()
      response = IsRegistered(ParsedEmail['email'])

      return make_response(response)


@app.route("/checkPassword",methods = ["POST"])
def UrlCheckPassword():
   if request.method == "POST":
      
      ParsedInfo = JsonParse()
      response = IsPasswordCorrect(ParsedInfo['email'] , ParsedInfo['password'] )

      return make_response(response) 




@app.route("/getAccountDetails",methods = ["POST"])
def UrlGetAccountDetails():
   if request.method == "POST":

      ParsedInfo = JsonParse()    
      response = accountInfoFunc(ParsedInfo['contactId'] , ParsedInfo['accountId'] )

      return make_response(response) 




@app.route("/hasDoorAccess",methods = ["POST"])
def UrlHasDoorAccess():
   if request.method == "POST":

      ParsedInfo = JsonParse()    
      response = doorAccessFunc(ParsedInfo['contactId'] , ParsedInfo['accountId'] ,ParsedInfo['doorId'] )

      return make_response(response) 


         


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










def doorAccessFunc(contactId , accountId , doorId):

   if not contactId or not accountId or not doorId :
      return jsonify(status = "error",errorMsg = "invalid input" ) 
   
   load_dotenv(find_dotenv())
   
   
   connection = psycopg2.connect(
   host=      os.environ.get("HOST") ,
   database=  os.environ.get("DATABASE")   ,
   user=      os.environ.get("USER")     ,
   password= os.environ.get("PASSWORD")
   )
   
 
   try:
      cursor = connection.cursor()

      #return   str(contactId +" "+ accountId +" " +doorId)
       
   
      cursor.execute("select P.NAME from salesforce.contractcontactrole ccr, salesforce.contract ctr,  salesforce.contract_products__c cp, salesforce.product2 p where ccr.contactId = %(contactId)s      and ctr.accountId = %(accountId)s and ccr.role like '%%Hizmet%%'   and ccr.contractId = ctr.sfid   and cp.contract__c = ctr.sfid    and cp.product__c  = p.sfid   and ctr.status in ('Activated', 'In Closing Process')    and p.Barcode__c = %(doorId)s        UNION select P.NAME from salesforce.Contract_Product_Roles__c cpr,      salesforce.contract_products__c cp, salesforce.contract ctr,    salesforce.product2 p where cpr.contact__c = %(contactId)s   and cpr.contract_product__c = cp.sfid  and cp.contract__c = ctr.sfid   and ctr.accountId = %(accountId)s    and ctr.status in ('Activated', 'In Closing Process')  and cp.product__c  = p.sfid  and p.Barcode__c = %(doorId)s   UNION  select r.name ||  ':   ' || rd.door_name__c  from salesforce.contractcontactrole ccr, salesforce.contract ctr,       salesforce.region__c r, salesforce.region_door__c rd  where ccr.contactId = %(contactId)s      and ctr.accountId = %(accountId)s      and ccr.contractId = ctr.sfid   and ctr.status in ('Activated', 'In Closing Process')     and ctr.region__c = r.name   and r.sfid = rd.region__c   and rd.barcode__c = %(doorId)s   UNION select r.name || ':   ' || rd.door_name__c  from salesforce.Contract_Product_Roles__c cpr,   salesforce.contract_products__c cp,   salesforce.contract ctr, salesforce.region__c r,  salesforce.region_door__c rd where cpr.contact__c = %(contactId)s  and cpr.contract_product__c = cp.sfid and cp.contract__c = ctr.sfid   and ctr.accountId = %(accountId)s   and ctr.status in ('Activated', 'In Closing Process')   and ctr.region__c = r.name and r.sfid = rd.region__c and rd.barcode__c = %(doorId)s   ", { 'accountId'  : accountId , 'doorId' : doorId , 'contactId': contactId})
  
     

      record = cursor.fetchall()

      count = len(record)

      if count > 0 :
         return jsonify(status = "success", hasAccess = True )
      else:
         return jsonify(status = "success", hasAccess = False )



 
       
   except Exception as e :
      return jsonify(status = "error",errorMsg = "Sistemsel bir problem oluştu. Lütfen Smartoffice ile iletişime geçiniz." )        #return jsonify(status = "error",errorMsg = str(e) ) 

   finally:
      if (connection):
         cursor.close()
         connection.close()


   














def accountInfoFunc(contactId , accountId):

   if not accountId or not contactId  :
      return jsonify(status = "error",errorMsg = "invalid input" ) 

   
   
   load_dotenv(find_dotenv())
   
   
   connection = psycopg2.connect(
   host=      os.environ.get("HOST") ,
   database=  os.environ.get("DATABASE")   ,
   user=      os.environ.get("USER")     ,
   password= os.environ.get("PASSWORD")
   )
   
 
   try:
      cursor = connection.cursor()   

  
      cursor.execute("select acc.sfid , acc.name  , acc.Vergi_No__c , acc.Vergi_Dairesi__c , acc.BillingStreet , acc.BillingPostalCode , acc.BillingCity, acc.BillingState , acc.BillingCountry , acc.ShippingStreet , acc.ShippingPostalCode , acc.ShippingCity , acc.ShippingState , acc.ShippingCountry , ccr.role from salesforce.contact co, salesforce.account acc, salesforce.contractcontactrole ccr, salesforce.contract ctr where ctr.accountId = acc.sfid   and co.sfid = ccr.contactid    and ccr.contractId = ctr.sfid   and ctr.status in ('Activated', 'In Closing Process')  and co.sfid = %(contactId)s and acc.sfid = %(accountId)s  ", { 'accountId' :  accountId , 'contactId' : contactId } )

      records = cursor.fetchall()

      count = len(records)

      if count == 0 :
         return jsonify(status = "error",errorMsg = "Kayıt bilgileriniz eksik. SmartOffice ile iletişime geçiniz." ) #Account ya da contractcontactrole tablosunda eksik vardır. ya da ac id yanlış.
      elif count > 1:
         return jsonify(status = "error",errorMsg = "Birden fazla rol kayıt bilgisi tespit edildi. SmartOffice ile iletişime geçiniz." ) #birden fazla contractcontactrole girilmiş.




      #sql sorgusunun sütunlara ayrılması


      AccountSfId = ''
      AccountName = ''
      TaxNumber = ''
      TaxOffice = ''
      BillingStreet = ''
      BillingPostalCode  = ''
      BillingCity = ''
      BillingState= ''
      BillingCountry = ''
      ShippingStreet = ''
      ShippingPostalCode = ''
      ShippingCity = ''
      ShippingState = ''
      ShippingCountry = ''
      AdministratorStatus = False
      


      for row in records:


         AccountSfId        = row[0]
         AccountName        = row[1]
         TaxNumber          = row[2]
         TaxOffice          = row[3]
         BillingStreet      = row[4]
         BillingPostalCode  = row[5]
         BillingCity        = row[6]
         BillingState       = row[7]
         BillingCountry     = row[8]
         ShippingStreet     = row[9]
         ShippingPostalCode = row[10]
         ShippingCity       = row[11]
         ShippingState      = row[12]
         ShippingCountry    = row[13]

         if row[14] == "Admin ve Hizmet Alan" or row[14] == "Admin":
            AdministratorStatus = True
         
   
         

         responseJson = {
                           "status"             : "success", 
                           "AccountSfId"        : AccountSfId,
                           "AccountName"        : AccountName,
                           "TaxNumber"          : TaxNumber,
                           "TaxOffice"          : TaxOffice,
                           "BillingStreet"      : BillingStreet,
                           "BillingPostalCode"  : BillingPostalCode,
                           "BillingCity"        : BillingCity,
                           "BillingState"       : BillingState,
                           "BillingCountry"     : BillingCountry,
                           "ShippingStreet"     : ShippingStreet,
                           "ShippingPostalCode" : ShippingPostalCode,
                           "ShippingCity"       : ShippingCity,
                           "ShippingState"      : ShippingState,
                           "ShippingCountry"    : ShippingCountry,
                           "IsAdmin"            : AdministratorStatus
                           } 



         return json.dumps(responseJson, indent=4, ensure_ascii=False)

     

         
   except:
      return jsonify(status = "error",
               errorMsg = "Sistemsel bir problem oluştu. Lütfen Smartoffice ile iletişime geçiniz."
               )

   finally:
      if (connection):
         cursor.close()
         connection.close()










def IsPasswordCorrect(userEmail , userPw ):

   if not userEmail  or not userPw :
      return jsonify(status = "error",errorMsg = "invalid input" ) 

   load_dotenv(find_dotenv())
   
   
   connection = psycopg2.connect(
   host=      os.environ.get("HOST") ,
   database=  os.environ.get("DATABASE")   ,
   user=      os.environ.get("USER")     ,
   password= os.environ.get("PASSWORD")
   )
   
 
   try:
      cursor = connection.cursor()     
           
      cursor.execute("SELECT sfid , mobile_verification_code__c FROM salesforce.contact WHERE email = %(userEmail)s  AND mobile_verification_code__c = %(otp)s " , { 'userEmail': userEmail , 'otp' : userPw})
      user = cursor.fetchall()

      count = len(user)

      #return str(count)

   

      if count != 1 :
         return jsonify(status = "error",
                        errorMsg = "Giriş bilgileriniz hatalıdır. Lütfen şifrenizi kontrol ediniz."
                       )
      
      else:


         cursor.execute("SELECT co.sfid, co.firstname, co.email, co.mobile_verification_code__c, acc.name, acc.sfid ,co.mobilephone , co.lastname ,co.sfid FROM salesforce.contact co , salesforce.account acc , salesforce.contractcontactrole ccr , salesforce.contract ctr WHERE co.email = %(userEmail)s AND ctr.accountId = acc.sfid AND co.sfid = ccr.contactid AND ccr.contractId = ctr.sfid AND ctr.status IN ('Activated', 'In Closing Process')" , { 'userEmail' :  userEmail } )
         records = cursor.fetchall()

         #return str(records)



         #sql sorgusunun sütunlara ayrılması

         accountList = []


         ContactFirstName = ''
         ContactLastName = ''
         ContactEmail = ''
         ContactId = ''
         ContactMobilePhone  = ''

         for row in records:

            acName = row[4]
            acId = row[5]

            tmpAccounts ={ "AccountName" : acName  ,  "AccountId" : acId } 
            
            

            
            ContactId = row[0]
            ContactFirstName = row[1]
            ContactEmail = row[2]
            ContactMobilePhone = row[6]
            ContactLastName = row[7]
            ContactId = row[8]

 
            accountList.append(tmpAccounts)
       
      
         

         responseJson = {
                           "status" : "success", 
                           "MobilePhone" : ContactMobilePhone,  
                           "FirstName" : ContactFirstName , 
                           "LastName" : ContactLastName,
                           "ContactId" : ContactId,
                           "Accounts" : accountList 
                           } 



         return json.dumps(responseJson, indent=4, ensure_ascii=False)

     

         
   except:
      return jsonify(status = "error",
               errorMsg = "Sistemsel bir problem oluştu. Lütfen Smartoffice ile iletişime geçiniz."
               )

   finally:
      if (connection):
         cursor.close()
         connection.close()








def IsRegistered(userEmail):

   if not userEmail:
      return jsonify(status = "error",errorMsg = "invalid input" ) 
   
   load_dotenv(find_dotenv())
   
   
   connection = psycopg2.connect(
   host=      os.environ.get("HOST") ,
   database=  os.environ.get("DATABASE")   ,
   user=      os.environ.get("USER")     ,
   password= os.environ.get("PASSWORD")
   )
   
 
   try:
      cursor = connection.cursor()     
      cursor.execute("SELECT id  FROM  salesforce.contact WHERE email = %(userEmail)s", {'userEmail': userEmail})       # + "LIMIT 1"
      record = cursor.fetchall()

      count = len(record)

      if count != 1 :
         return jsonify(status = "error",
                        errorMsg = "Giriş bilgileriniz hatalıdır. Lütfen Smartoffice ile iletişime geçiniz."
                      )

      elif count == 1 :

         letters = string.ascii_uppercase
         otp = ''.join(random.choice(letters) for i in range(6))

         test = cursor.execute("UPDATE salesforce.contact SET mobile_verification_code__c = %(otp)s WHERE email  = %(userEmail)s",{ 'otp' : otp , 'userEmail': userEmail } ) 
         connection.commit()
         
         return  jsonify(status = "success", IsValidUser = "true")
             
 
       
   except Exception as e :
      return jsonify(status = "error",errorMsg = "Sistemsel bir problem oluştu. Lütfen Smartoffice ile iletişime geçiniz." )        #return jsonify(status = "error",errorMsg = str(e) ) 

   finally:
      if (connection):
         cursor.close()
         connection.close()


   

 






if __name__=="__main__":
    app.run(debug = True)

