from flask import Flask, request, render_template
import yaml

app = Flask(__name__)

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        secret = ""
    else:
        secret = request.form["secret"]

    fragen = config["fragen"]

    frage = next((i for i, f in enumerate(fragen) if f["s"] == secret), 0)

    debugmsg = ""
    if config["debug"]:
        debugmsg = "secret = '" + secret + "' fragen = " + str(fragen) + "frage #" + str(frage)

    return render_template("index.html",
                           thislevel=frage,
                           nextlevel=frage + 1,
                           aufgabe=fragen[frage]["q"],
                           debug=debugmsg)

@app.route("/item")
def item():
    return render_template("item.html")
    
if __name__ == '__main__':
    app.run(port=config["port"],
            host=config["server"],
            debug=config["debug"])
