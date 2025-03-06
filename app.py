from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initial game state
game_state = {
    "board": [""] * 9,  # 3x3 grid as a flat list
    "current_player": "X",
    "winner": None,
    "game_over": False,
    "scores": {"X": 0, "O": 0}
}

# Winning combinations
WINNING_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
    (0, 4, 8), (2, 4, 6)              # Diagonals
]

def check_winner():
    for combo in WINNING_COMBOS:
        if game_state["board"][combo[0]] == game_state["board"][combo[1]] == game_state["board"][combo[2]] != "":
            return game_state["board"][combo[0]]
    if "" not in game_state["board"]:
        return "Draw"
    return None

@app.route("/")
def index():
    return render_template("index.html", board=game_state["board"], scores=game_state["scores"])

@app.route("/move", methods=["POST"])
def make_move():
    if game_state["game_over"]:
        return jsonify({"error": "Game is over"}), 400

    data = request.get_json()
    position = data["position"]

    if game_state["board"][position] == "":
        game_state["board"][position] = game_state["current_player"]
        winner = check_winner()

        if winner:
            game_state["game_over"] = True
            game_state["winner"] = winner
            if winner != "Draw":
                game_state["scores"][winner] += 1
        else:
            game_state["current_player"] = "O" if game_state["current_player"] == "X" else "X"

        return jsonify({
            "board": game_state["board"],
            "current_player": game_state["current_player"],
            "winner": game_state["winner"],
            "scores": game_state["scores"]
        })
    return jsonify({"error": "Invalid move"}), 400

@app.route("/reset", methods=["POST"])
def reset_game():
    game_state["board"] = [""] * 9
    game_state["current_player"] = "X"
    game_state["winner"] = None
    game_state["game_over"] = False
    return jsonify({
        "board": game_state["board"],
        "current_player": game_state["current_player"],
        "winner": None,
        "scores": game_state["scores"]
    })

if __name__ == "__main__":
    app.run(debug=True)