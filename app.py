from flask import Flask ,request



app = Flask(__name__)


@app.route("/")
def index():
   return "Hello World"
   


@app.route("/yorum",methods = ["GET","POST"])
def deneme():
   if request.method == "POST":
      return "Post yaptınız"
   
   else:
      return "Get yaptınız"  


if __name__=="__main__":
    app.run(debug = True)
