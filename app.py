from flask import Flask ,request, jsonify



app = Flask(__name__)


@app.route("/")
def index():
   return '<h1>Hello html</h1>'
   


@app.route("/yorum",methods = ["GET","POST"])
def deneme():
   if request.method == "GET":
      return '<h1>Hello html again</h1>'
   
   else:
      return jsonify({'Sonuc' : 'true'}) 


if __name__=="__main__":
    app.run(debug = True)
