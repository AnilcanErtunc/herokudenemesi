from flask import jsonify
import psycopg2
import string , random
from dotenv import load_dotenv , find_dotenv
import os




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


   

