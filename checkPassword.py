from flask import jsonify , json 
import psycopg2
from dotenv import load_dotenv , find_dotenv
import os





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



