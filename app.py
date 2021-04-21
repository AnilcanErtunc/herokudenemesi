from flask import Flask ,request, jsonify , json



app = Flask(__name__)



@app.route("/")
def index():
   return '<h1>Hello html</h1>'
   


@app.route("/test",methods = ["GET","POST"])
def deneme():
   if request.method == "GET":

      return '<h1>Hello html again</h1>'
   
   elif request.method == "POST":

      data = request.get_json()    #request.get_data()  

      kur = data['kur']   #request.get_data()  

      return kur
         


if __name__=="__main__":
    app.run(debug = True)
