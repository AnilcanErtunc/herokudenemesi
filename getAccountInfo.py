from flask import jsonify , json 
import psycopg2
import os



def accountInfoFunc(contactId , accountId):

   if not accountId or not contactId  :
      return jsonify(status = "error",errorMsg = "invalid input" ) 
   


 
   try:
      
      
      HOST = os.environ('HOST'))
   
   
      return "Test"
     

         
   except Exception as e :
      return jsonify(status = "error",
               errorMsg =  e                       
               ) # "Sistemsel bir problem oluştu. Lütfen Smartoffice ile iletişime geçiniz."

 



