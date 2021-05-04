from flask import jsonify , json 
import psycopg2
import os



def accountInfoFunc(contactId , accountId):

   if not accountId or not contactId  :
      return jsonify(status = "error",errorMsg = "invalid input" ) 

   return "Host degeri :" + os.environ('HOST')
   
   
   
   connection = psycopg2.connect(
   host=      os.environ('HOST') ,
   database=  os.environ('DATABASE')   ,
   user=      os.environ('USER')     ,
   password= os.environ('PASSWORD')
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



