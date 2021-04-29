from flask import jsonify
import psycopg2
from dotenv import load_dotenv , find_dotenv
import os



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


   

