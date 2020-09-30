from flask import Flask, request, render_template
import yaml

app = Flask(__name__)

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        secret = ""
        levelByInput  = 0
    else:
        secret = request.form["secret"]
        try:
            levelByInput = int(request.form["level"])
        except ValueError:
            levelByInput = 0

    fragen = config["fragen"]

    levelByAnswer = next((i for i, f in enumerate(fragen) if f["s"] == secret), 0)

    if levelByAnswer == levelByInput:
        thisLevel = levelByAnswer + 1
        wrong = None
    else:
        thisLevel = levelByAnswer
        wrong = secret
    
    debugmsg = ""
    if config["debug"]:
        debugmsg = "secret = '" + secret + "' fragen = " + str(fragen) + "frage #" + str(levelByAnswer)

    return render_template("index.html",
                           thislevel=thisLevel,
                           nextlevel=thisLevel + 1,
                           aufgabe=fragen[thisLevel]["q"],
                           wronganswer=wrong,
                           debug=debugmsg)


@app.route("/demosuccess")
def demosuccess():
    return render_template("success.html",
                           secretkey="-".join(i["s"] for i in config["fragen"]))


@app.route("/item")
def item():
    return render_template("item.html")
    
if __name__ == '__main__':
    app.run(port=config["port"],
            host=config["server"],
            debug=config["debug"],
            ssl_context=(config["tlscrt"], config["tlskey"]))
