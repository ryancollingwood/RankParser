import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, render_template
from interactive import RankParserCore
from solver import UnsolvableModelError
from solver.exceptions import IncompleteResultsError
from test_data import programmer_riddle, tea_steps

app = Flask(__name__)

core = RankParserCore(log_history=False)


def get_state():
    items = core.get_items()
    history = core.get_history()
    try:
        solutions = core.solve()
    except (IncompleteResultsError, Exception):
        solutions = []
    return {
        "items": list(items),
        "history": list(history),
        "solutions": [list(s) for s in solutions],
        "solution_count": len(solutions),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state", methods=["GET"])
def state():
    return jsonify(get_state())


@app.route("/api/parse", methods=["POST"])
def parse():
    data = request.get_json()
    text = (data or {}).get("text", "").strip()
    if not text:
        return jsonify({"error": "No input provided"}), 400

    try:
        result = core.do_parse(text)
        if result is None:
            return jsonify({"error": "Could not parse input"}), 422
        return jsonify(get_state())
    except UnsolvableModelError as e:
        return jsonify({"error": "Constraint makes the problem unsolvable", "detail": str(e)}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/undo", methods=["POST"])
def undo():
    removed = core.undo()
    state = get_state()
    state["removed"] = removed
    return jsonify(state)


@app.route("/api/reset", methods=["POST"])
def reset():
    global core
    core = RankParserCore(log_history=False)
    return jsonify(get_state())


@app.route("/api/load_challenge", methods=["POST"])
def load_challenge():
    data = request.get_json()
    challenge = (data or {}).get("challenge", "programmer")

    global core
    core = RankParserCore(log_history=False)

    statements = programmer_riddle if challenge == "programmer" else tea_steps
    errors = []
    for stmt in statements:
        try:
            core.do_parse(stmt)
        except Exception as e:
            errors.append(str(e))

    state = get_state()
    state["loaded"] = challenge
    if errors:
        state["errors"] = errors
    return jsonify(state)


@app.route("/api/stats", methods=["GET"])
def stats():
    result = core.get_stats()
    if result is None:
        return jsonify({"stats": {}})
    return jsonify({"stats": result})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
