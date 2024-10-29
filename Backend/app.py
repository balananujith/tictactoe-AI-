from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Initial empty board
board = [' ' for _ in range(9)]

def check_winner(board, player):
    """Check for a winning configuration."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def minimax(board, depth, is_maximizing):
    """AI algorithm to choose the best move."""
    if check_winner(board, 'O'):
        return -1
    elif check_winner(board, 'X'):
        return 1
    elif ' ' not in board:
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

def best_move():
    """Determine the best move for the AI."""
    best_score = -float('inf')
    move = 0
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    board[data['index']] = 'O'
    if check_winner(board, 'O'):
        return jsonify({"winner": "User"})
    elif ' ' not in board:
        return jsonify({"winner": "Draw"})
    
    ai_move = best_move()
    board[ai_move] = 'X'
    if check_winner(board, 'X'):
        return jsonify({"winner": "AI", "index": ai_move})
    elif ' ' not in board:
        return jsonify({"winner": "Draw", "index": ai_move})
    
    return jsonify({"index": ai_move})

@app.route('/reset', methods=['POST'])
def reset():
    global board
    board = [' ' for _ in range(9)]
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
