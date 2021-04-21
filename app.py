from flask import Flask ,request, jsonify , json
import psycopg2



app = Flask(__name__)



@app.route("/")
def index():

   connection = psycopg2.connect(
    host=      ${{ secrets.HOST_NAME}}  ,
    database=  ${{ secrets.DATABASE}}   ,
    user=      ${{ secrets.USER}}       ,
    password=  ${{ secrets.PASSWORD}})
    
    
   try:
      cursor = connection.cursor()
      # Print PostgreSQL details
      print("PostgreSQL server information")
      print(connection.get_dsn_parameters(), "\n")
      # Executing a SQL query
      cursor.execute("SELECT version();")
      # Fetch result
      record = cursor.fetchone()
      print("You are connected to - ", record, "\n")

   except (Exception, Error) as error:
      print("Error while connecting to PostgreSQL", error)
   finally:
      if (connection):
         cursor.close()
         connection.close()
         print("PostgreSQL connection is closed")


   return jsonify(Record = record)
   


@app.route("/test",methods = ["GET","POST"])
def deneme():
   if request.method == "GET":

      return '<h1>Hello html again</h1>'
   
   elif request.method == "POST":

      data = request.get_json()    

      kur = data['kur']   


      return kur
         


if __name__=="__main__":
    app.run(debug = True)
