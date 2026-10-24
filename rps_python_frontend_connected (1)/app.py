from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import random
import uuid
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)  # Allows the GitHub Pages frontend to call this API.

ROUNDS = 25
games = {}

def new_game_state():
    return {
        "round_no": 0,
        "player_wins": 0,
        "computer_wins": 0,
        "ties": 0,
        "rock_count": 0,
        "paper_count": 0,
        "scissors_count": 0,
        "current_streak": 0,
        "longest_streak": 0,
        "history": [],
        "game_over": False,
    }

def public_state(game):
    rate = (game["player_wins"] / game["round_no"] * 100) if game["round_no"] else 0
    if game["round_no"] == 0:
        match_result = "Not started"
    elif game["round_no"] < ROUNDS:
        match_result = "Match in progress"
    elif game["player_wins"] > game["computer_wins"]:
        match_result = "Player wins the match"
    elif game["computer_wins"] > game["player_wins"]:
        match_result = "Computer wins the match"
    else:
        match_result = "Match draw"

    return {
        **game,
        "win_rate": round(rate, 2),
        "rounds": ROUNDS,
        "match_result": match_result,
    }

@app.get("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.get("/<path:path>")
def frontend_files(path):
    return send_from_directory(FRONTEND_DIR, path)

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "message": "Rock Paper Scissors API is running"})

@app.post("/api/new-game")
def create_game():
    game_id = str(uuid.uuid4())
    games[game_id] = new_game_state()
    return jsonify({"game_id": game_id, "game": public_state(games[game_id])})

@app.post("/api/play")
def play():
    data = request.get_json(silent=True) or {}
    game_id = data.get("game_id")
    player = data.get("player")

    if not game_id or game_id not in games:
        return jsonify({"error": "Game session not found. Start a new game."}), 404
    if player not in ("Rock", "Paper", "Scissors"):
        return jsonify({"error": "Choose Rock, Paper, or Scissors."}), 400

    game = games[game_id]
    if game["game_over"]:
        return jsonify({"error": "This match is complete. Start a new game."}), 409

    computer = random.choice(["Rock", "Paper", "Scissors"])
    game["round_no"] += 1

    if player == "Rock":
        game["rock_count"] += 1
    elif player == "Paper":
        game["paper_count"] += 1
    else:
        game["scissors_count"] += 1

    if player == computer:
        result = "Tie"
        game["ties"] += 1
        game["current_streak"] = 0
    elif (
        (player == "Rock" and computer == "Scissors")
        or (player == "Paper" and computer == "Rock")
        or (player == "Scissors" and computer == "Paper")
    ):
        result = "Player Wins"
        game["player_wins"] += 1
        game["current_streak"] += 1
        game["longest_streak"] = max(game["longest_streak"], game["current_streak"])
    else:
        result = "Computer Wins"
        game["computer_wins"] += 1
        game["current_streak"] = 0

    round_record = {
        "round": game["round_no"],
        "player": player,
        "computer": computer,
        "result": result,
    }
    game["history"].append(round_record)

    if game["round_no"] >= ROUNDS:
        game["game_over"] = True

    return jsonify({
        "round": round_record,
        "game": public_state(game),
        "game_over": game["game_over"],
    })

@app.get("/api/report/<game_id>")
def report(game_id):
    if game_id not in games:
        return jsonify({"error": "Game session not found."}), 404
    return jsonify(public_state(games[game_id]))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
