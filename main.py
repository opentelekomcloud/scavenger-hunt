from flask import Flask, request, render_template
import yaml


def qIndexFor(sec):
    fragen = config["fragen"]

    level = next((i for i, f in enumerate(fragen) if f["s"] == sec), -1)

    return level 
    

app = Flask(__name__)

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

@app.route("/", methods=["GET", "POST"])
def index():
    # find out which level we've been so far as documented by the hidden value
    if request.method == "GET":
        secret = ""
        levelByHidden  = -1
    else:
        secret = request.form["secret"].upper()
        try:
            levelByHidden = int(request.form["level"])
        except ValueError:
            levelByHidden = -1

    msg = ""
    if secret:
        msg = "The answer '%s' is unfortunately wrong. Try again:" % secret
        
    # find out which level we solved based on the answer:
    # -1 no answer at all
    # 0..n a right answer, but does it qualify?
    levelByAnswer = qIndexFor(secret)
    if levelByAnswer < 0:
        if levelByHidden < 0:
            newLevel = 0
        else:
            newLevel = levelByHidden
    else: # wir haben eine richtige antwort abgegeben, aber passt der letzte level auch dazu?
        if levelByAnswer == levelByHidden:
            newLevel = levelByAnswer + 1
            msg = "The answer '%s' is correct!" % secret
        else: # eine korrekte antwort, aber letzter level stimmt nicht? Gemogelt?
            newLevel = levelByHidden

    maxLevel = len(config["fragen"])
            
    debugmsg = list()
    if config["debug"]:
        debugmsg.append("Secret:        " + secret)
        debugmsg.append("levelByHidden: " + str(levelByHidden))
        debugmsg.append("levelByAnswer: " + str(levelByAnswer))
        debugmsg.append("newLevel:      " + str(newLevel))
        debugmsg.append("maxLevel:      " + str(maxLevel))
        
    if newLevel == maxLevel:
        return render_template("success.html",
                               secretkey="-".join(i["s"] for i in config["fragen"]),
                               solution=config["solution"])
    else:
        return render_template("index.html",
                               level=newLevel,
                               aufgabe=config["fragen"][newLevel]["q"],
                               answer=msg,
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
