from langchain_ollama.llms import OllamaLLM
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import matplotlib.gridspec as gridspec
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

llama_img = mpimg.imread("Xmeta.png")
gemma_img = mpimg.imread("Ogemma.png")

# Game constants
EMPTY = "-"
PLAYER_X = "X"  # LLM 1
PLAYER_O = "O"  # LLM 2

plt.ion()
fig = plt.figure(figsize=(10, 5), constrained_layout=True)
fig.canvas.manager.set_window_title("🤖 LLM Tic Tac Toe Battle")

# Maximize the window (platform-dependent)
mng = plt.get_current_fig_manager()
try:
    mng.window.state('zoomed')  # Windows (TkAgg)
except:
    try:
        mng.window.showMaximized()  # Linux / Mac (Qt)
    except:
        pass

# GridSpec with wider right panel
gs = gridspec.GridSpec(1, 2, width_ratios=[3.5, 1.5], figure=fig)

board_ax = fig.add_subplot(gs[0])
side_ax = fig.add_subplot(gs[1])

# 3x3 board
def new_board():
    return [EMPTY] * 9

def is_winner(board, player):
    win_patterns = [
        [0,1,2], [3,4,5], [6,7,8],   # rows
        [0,3,6], [1,4,7], [2,5,8],   # columns
        [0,4,8], [2,4,6]             # diagonals
    ]
    for pattern in win_patterns:
        if all(board[i] == player for i in pattern):
            return True, pattern
    return False, None

def is_full(board):
    return all(cell != EMPTY for cell in board)

def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == EMPTY]

def board_to_string(board):
    return "\n".join([" ".join(board[i:i+3]) for i in range(0, 9, 3)])

# Initialize local LLMs
llm_x = OllamaLLM(model="gemma3:1b")   # X
llm_o = OllamaLLM(model="llama3.2:1b")  # O

# Matplotlib visualization
def show_board(board, status_text="", model_x_label="Gemma3:1b (X)", model_o_label="LLaMA3.2:1b (O)", winning_pattern=None):
    board_ax.clear()
    side_ax.clear()

    board_ax.set_xlim(0, 3)
    board_ax.set_ylim(0, 3)
    board_ax.set_xticks([])
    board_ax.set_yticks([])

    for i in range(1, 3):
        board_ax.axhline(i, color="black", linewidth=2)
        board_ax.axvline(i, color="black", linewidth=2)

    for idx, cell in enumerate(board):
        row, col = divmod(idx, 3)
        if cell != EMPTY:
            icon = llama_img if cell == PLAYER_X else gemma_img
            imagebox = OffsetImage(icon, zoom=0.3)
            ab = AnnotationBbox(imagebox, (col + 0.5, 2.5 - row), frameon=False)
            board_ax.add_artist(ab)
                # else:
        #     board_ax.text(col + 0.5, 2.5 - row, str(idx),
        #                   fontsize=20, ha='center', va='center', color='gray')

    if status_text:
        board_ax.set_title(status_text, fontsize=14, color="darkgreen")

    side_ax.axis("off")
    side_ax.text(0.5, 0.9, model_x_label, fontsize=10, ha='center', va='center')
    side_ax.add_patch(plt.Rectangle((0.1, 0.7), 0.8, 0.15, fill=False, edgecolor='lightgray', linestyle='dashed'))

    side_ax.text(0.5, 0.5, model_o_label, fontsize=10, ha='center', va='center')
    side_ax.add_patch(plt.Rectangle((0.1, 0.3), 0.8, 0.15, fill=False, edgecolor='lightgray', linestyle='dashed'))

    # Draw winning line
    if winning_pattern:
        coords = [(i % 3 + 0.5, 2.5 - i // 3) for i in winning_pattern]
        x_vals, y_vals = zip(*coords)
        board_ax.plot(x_vals, y_vals, color="green", linewidth=4, linestyle='--')

    fig.subplots_adjust(wspace=0.3)
    fig.canvas.draw()
    plt.pause(0.5)

# Get move from LLM
def get_llm_move(llm, player, board, model_name):
    board_str = board_to_string(board)
    options = available_moves(board)
    options_str = ", ".join(map(str, options))

    prompt = f"""
You are a highly competitive AI named {model_name}, playing Tic Tac Toe as '{player}'.

Your goal is to win the game or block your opponent if they are about to win.

Here is the current board:
{board_str}

Available positions to play: {options_str}
Instructions:
1. Check if opponent is winning in the next round, if Yes block their move
2. If Opponent is not winning in the next round, Check If you are winning in the current round and play the move
3. If You are not winning in the current round, play a move, That gives you advantage for the next round

Choose ONE of the numbers from the available positions above. Only respond with that number and nothing else.
Think carefully. Respond with just the number.
"""
    response = llm.invoke(prompt)
    try:
        move = int(response.strip().split()[0])
        if move in options:
            return move
        else:
            print(f"Invalid move '{move}' by {player}, retrying...")
            return None
    except:
        print(f"Bad response from {player}: {response}")
        return None

# Game loop
def play_game():
    board = new_board()
    current_player = PLAYER_X
    llms = {PLAYER_X: llm_x, PLAYER_O: llm_o}

    print("🤖 Tic Tac Toe Battle: Llama3.2 (X) vs Gemma3 (O)\n")
    show_board(board)

    while not is_winner(board, PLAYER_X)[0] and not is_winner(board, PLAYER_O)[0] and not is_full(board):
        llm = llms[current_player]
        move = None

        for _ in range(3):
            model_name = "Gemma3" if current_player == PLAYER_X else "LLaMA3.2"
            move = get_llm_move(llm, current_player, board, model_name)
            if move is not None:
                break
            time.sleep(1)

        if move is None:
            print(f"{current_player} failed to make a move. Game aborted.")
            return

        board[move] = current_player
        print(f"{current_player} plays at position {move}")
        show_board(board)
        time.sleep(0.5)

        current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X

    is_x_win, x_pattern = is_winner(board, PLAYER_X)
    is_o_win, o_pattern = is_winner(board, PLAYER_O)

    if is_x_win:
        print("🏆 Player X (Llama3.2) wins!")
        show_board(board, status_text="Player X (Llama3.2) wins!", winning_pattern=x_pattern)
    elif is_o_win:
        print("🏆 Player O (Gemma3) wins!")
        show_board(board, status_text="Player O (Gemma3) wins!", winning_pattern=o_pattern)
    else:
        print("🤝 It's a draw!")
        show_board(board, status_text="It's a draw!")

    print("\nGame over. Close the plot window to exit.")
    plt.ioff()
    plt.show()

# Run the game
play_game()
