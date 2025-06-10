
from flask import Flask, render_template, request, jsonify, session, redirect
import random
import string

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Used Ai, This line sets a secret password for your app. It helps keep information safe when your app saves data for users (like login info).

#Used Ai to generate the Player name lists
legends = [
    "pele", "maradona", "beckenbauer", "zidane", "ronaldo",
    "baggio", "gerrard", "seedorf", "ronaldinho", "cafu",
    "rivaldo", "figo", "pirlo", "puskas", "cruyff",
    "zico", "kaka", "schweinsteiger", "robben", "henry"
]

current = [
    "messi", "neymar", "mbappe", "ronaldo", "debruyne",
    "modric", "hazard", "salah", "mane", "kante",
    "halland", "van dijk", "benzema", "pogba", "sterling",
    "david silva", "aguero", "alonso", "firmino", "griezmann"
]

combined = legends + current
#Used Ai to generate the hints for the players
hints = {
    "pele": "Brazilian legend who won 3 World Cups.",
    "maradona": "Argentine known for 'Hand of God'.",
    "beckenbauer": "German 'Der Kaiser' and sweeper.",
    "zidane": "French playmaker and headbutt icon.",
    "ronaldo": "Brazilian striker with 2002 WC win.",
    "baggio": "Italian who missed 1994 WC penalty.",
    "gerrard": "Liverpool captain and long-range shooter.",
    "seedorf": "Dutch midfielder who won UCL with 3 clubs.",
    "ronaldinho": "Famous Brazilian with magical skills.",
    "cafu": "Attacking right-back from Brazil.",
    "rivaldo": "Left-footed Brazilian attacker from late '90s.",
    "figo": "Portuguese winger who played for both Barça and Real.",
    "pirlo": "Italian maestro known for calm and free-kicks.",
    "puskas": "Hungarian legend with a FIFA award named after him.",
    "cruyff": "Dutch total football icon.",
    "zico": "Brazilian attacking midfielder from the 1980s.",
    "kaka": "Elegant Brazilian who won Ballon d’Or in 2007.",
    "schweinsteiger": "German midfielder, 2014 WC winner.",
    "robben": "Left-footed Dutch winger known for cutting in.",
    "henry": "French striker, Arsenal legend.",
    "messi": "Argentine GOAT, Barcelona icon.",
    "neymar": "Brazilian trickster who played for PSG.",
    "mbappe": "French star who won 2018 WC at age 19.",
    "debruyne": "Belgian playmaker at Manchester City.",
    "modric": "Croatian who won Ballon d’Or in 2018.",
    "hazard": "Belgian winger who starred for Chelsea.",
    "salah": "Egyptian winger for Liverpool.",
    "mane": "Senegalese speedster and former Liverpool star.",
    "kante": "French midfielder known for interceptions.",
    "halland": "Norwegian goal machine at Man City.",
    "van dijk": "Dutch defender and Liverpool leader.",
    "benzema": "French striker who won 2022 Ballon d’Or.",
    "pogba": "French midfielder with flashy style.",
    "sterling": "English winger with pace and flair.",
    "david silva": "Spanish magician at Manchester City.",
    "aguero": "Argentine striker and Man City icon.",
    "alonso": "Spanish deep-lying playmaker.",
    "firmino": "Brazilian forward with flair and teeth.",
    "griezmann": "French striker and Fortnite celebrator."
}

def scramble_word(word):
    word = word.replace(" ", "")
    word_letters = list(word)
    random.shuffle(word_letters)
    scrambled = "".join(word_letters)
    while scrambled == word:
        random.shuffle(word_letters)
        scrambled = "".join(word_letters)
    return scrambled

def get_word(category):
    previous_word = session.get("word", "")
    word_list = legends if category == "legends" else current if category == "current" else combined
    word = random.choice(word_list)
    while word == previous_word:
        word = random.choice(word_list)
    return word

@app.route("/", methods=["GET"])
def index():
    category = request.args.get("category", "combined")
    session["category"] = category
    session["score"] = 0
    session["wrong_attempts"] = 0
    word = get_word(category)
    session["word"] = word
    scrambled = scramble_word(word)
    return render_template("index.html", scrambled=scrambled, score=session["score"], category=category)

@app.route("/guess", methods=["POST"])
def guess():
    if "word" not in session or "score" not in session or "category" not in session:
        return jsonify({"error": "Game not started"}), 400

    data = request.get_json()
    guess = data.get("guess", "").lower().replace(" ", "")
    actual_word = session["word"].lower().replace(" ", "")
    score = session["score"]
    category = session["category"]

    if "wrong_attempts" not in session:
        session["wrong_attempts"] = 0

    if guess == actual_word:
        score += 1
        result = "Correct! 🎉"
        session["score"] = score
        session["wrong_attempts"] = 0
        new_word = get_word(category)
        session["word"] = new_word
        scrambled = scramble_word(new_word)
        return jsonify({
            "scrambled": scrambled,
            "score": score,
            "result": result,
            "hint": ""
        })
    else:
        session["wrong_attempts"] += 1
        if session["wrong_attempts"] == 1:
            hint = hints.get(session["word"].lower(), "No hint available.")
            result = "Wrong! Here's a hint: " + hint
            return jsonify({
                "scrambled": scramble_word(session["word"]),
                "score": score,
                "result": result,
                "hint": hint
            })
        else: #Used Ai to show the correct answer
            result = f"Wrong again! The correct word was '{session['word']}'."
            session["wrong_attempts"] = 0
            new_word = get_word(category)
            session["word"] = new_word
            scrambled = scramble_word(new_word)
            return jsonify({
                "scrambled": scrambled,
                "score": score,
                "result": result,
                "hint": ""
            })

@app.route("/timeout", methods=["POST"])
def timeout():
    if "word" not in session or "score" not in session or "category" not in session:
        return jsonify({"error": "Game not started"}), 400

    actual_word = session["word"]
    category = session["category"]
    session["wrong_attempts"] = 0

    new_word = get_word(category)
    session["word"] = new_word
    scrambled = scramble_word(new_word)

    return jsonify({
        "scrambled": scrambled,
        "score": session["score"],
        "result": f"Time's up! The correct word was '{actual_word}'.",
        "hint": ""
    })

if __name__ == "__main__":
    app.run(debug=True)
