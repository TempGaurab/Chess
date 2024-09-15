import chess
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext

def to_5bit_binary(value, offset):
    return format(value + offset, '06b')

def message_to_binary(message, binary_mapping):
    return ''.join(binary_mapping[char] for char in message)

def print_board_with_delay(moves_list, delay=2):
    board = chess.Board()
    for move in moves_list:
        board.push(move)
        time.sleep(delay)

def binary_to_chess_moves(binary_message):
    board = chess.Board()
    moves_list = []
    for bit in binary_message:
        legal_moves = list(board.legal_moves)
        if len(legal_moves) <= 1:
            board.reset()
        selected_move = legal_moves[0] if bit == '1' else legal_moves[-1]
        moves_list.append(selected_move)
        board.push(selected_move)
    return moves_list, board

def chess_moves_to_binary(moves_list):
    board = chess.Board()
    binary_message = ""
    for move in moves_list:
        legal_moves = list(board.legal_moves)
        if move == legal_moves[0]:
            binary_message += '1'
        elif move == legal_moves[-1]:
            binary_message += '0'
        else:
            raise ValueError(f"Move {move} is not encoded as either first or last move.")
        board.push(move)
    return binary_message

def encode_message_to_moves(message, binary_mapping):
    binary_message = message_to_binary(message, binary_mapping)
    moves_list, _ = binary_to_chess_moves(binary_message)
    return moves_list

def decode_moves_to_message(moves_list, binary_mapping):
    if isinstance(moves_list, str):
        moves_list = moves_list.split()  # Use the appropriate delimiter if needed
    binary_message = chess_moves_to_binary(moves_list)
    chunks = [binary_message[i:i+6] for i in range(0, len(binary_message), 6)]
    reverse_mapping = {v: k for k, v in binary_mapping.items()}
    decoded_message = ''.join([reverse_mapping[chunk] for chunk in chunks])
    return decoded_message

def uci_string_to_moves(uci_string):
    """
    Converts a string of UCI moves into a list of chess.Move objects.
    
    :param uci_string: String of UCI moves with possible spaces or newlines (e.g., 'a2a4 g8h6 b2b1n').
    :return: List of chess.Move objects.
    """
    # Remove any whitespace characters from the input string
    uci_string = uci_string.replace(' ', '').replace('\n', '')
    
    moves_list = []
    i = 0
    while i < len(uci_string):
        # Check if the next 5 characters can be a promotion move
        if i + 5 <= len(uci_string) and uci_string[i + 4] in 'nrq':
            move_str = uci_string[i:i + 5]
            move_len = 5
        # Otherwise, it must be a regular 4-character move
        elif i + 4 <= len(uci_string):
            move_str = uci_string[i:i + 4]
            move_len = 4
        else:
            raise ValueError(f"Invalid UCI move format: {uci_string[i:]}")
        
        try:
            move = chess.Move.from_uci(move_str)
        except Exception as e:
            raise ValueError(f"Invalid UCI move: {move_str}") from e
        
        moves_list.append(move)
        i += move_len
    
    return moves_list

def board_to_string(board):
    """
    Converts the chess board to a string representation.
    
    :param board: chess.Board object.
    :return: String representation of the board.
    """
    return str(board)

def on_encode():
    message = message_entry.get().strip().lower()
    if not all(char in binary_mapping for char in message):
        messagebox.showerror("Error", "Message contains invalid characters. Use only letters and digits.")
        return
    moves_list = encode_message_to_moves(message, binary_mapping)
    result_text = "\n".join(move.uci() for move in moves_list)
    encode_result_display.config(state=tk.NORMAL)
    encode_result_display.delete(1.0, tk.END)
    encode_result_display.insert(tk.END, result_text)
    encode_result_display.config(state=tk.DISABLED)

    # Update board display
    board = chess.Board()
    for move in moves_list:
        board.push(move)
    board_display.config(state=tk.NORMAL)
    board_display.delete(1.0, tk.END)
    board_display.insert(tk.END, board_to_string(board))
    board_display.config(state=tk.DISABLED)

def on_decode():
    move_input = move_entry.get().strip()
    try:
        moves_list = uci_string_to_moves(move_input)
        decoded_message = decode_moves_to_message(moves_list, binary_mapping)
        result_text = f"The decoded message is: {decoded_message}"
        decode_result_display.config(state=tk.NORMAL)
        decode_result_display.delete(1.0, tk.END)
        decode_result_display.insert(tk.END, result_text)
        decode_result_display.config(state=tk.DISABLED)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

    # Update board display
    board = chess.Board()
    for move in moves_list:
        board.push(move)
    board_display.config(state=tk.NORMAL)
    board_display.delete(1.0, tk.END)
    board_display.insert(tk.END, board_to_string(board))
    board_display.config(state=tk.DISABLED)

# Generate mappings
letter_offset = 0
digit_offset = 26
letter_mapping = {chr(i): to_5bit_binary(i - ord('a'), letter_offset) for i in range(ord('a'), ord('z') + 1)}
digit_mapping = {str(i): to_5bit_binary(i, digit_offset) for i in range(10)}
binary_mapping = {**letter_mapping, **digit_mapping}

# Set up GUI
root = tk.Tk()
root.title("Chess Message Encoder/Decoder")

# Frame for encoding part
encoding_frame = tk.Frame(root)
encoding_frame.pack(padx=10, pady=5)

# Input for encoding
tk.Label(encoding_frame, text="Enter message to encode (letters and digits only) below:").pack(padx=10, pady=5)
message_entry = tk.Entry(encoding_frame, width=70, font=('Arial', 14))
message_entry.pack(padx=10, pady=5)

encode_button = tk.Button(encoding_frame, text="Encode", command=on_encode, font=('Arial', 12))
encode_button.pack(padx=10, pady=5)

# Output for encoding
tk.Label(encoding_frame, text="Encoding Result:").pack(padx=10, pady=5)
encode_result_display = scrolledtext.ScrolledText(encoding_frame, width=80, height=10, wrap=tk.WORD, font=('Arial', 12))
encode_result_display.pack(padx=10, pady=5)

# Chess board display
tk.Label(encoding_frame, text="Chess Board:").pack(padx=10, pady=5)
board_display = scrolledtext.ScrolledText(encoding_frame, width=80, height=10, wrap=tk.WORD, font=('Arial', 12))
board_display.pack(padx=10, pady=5)

# Frame for decoding part with gray background
decoding_frame = tk.Frame(root, bg='gray')
decoding_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Input for decoding
tk.Label(decoding_frame, text="Enter chess moves in UCI format below:", bg='gray', fg='black').pack(padx=10, pady=5)
move_entry = tk.Entry(decoding_frame, width=70, font=('Arial', 14))
move_entry.pack(padx=10, pady=5)

decode_button = tk.Button(decoding_frame, text="Decode",bg='gray', command=on_decode, font=('Arial', 12))
decode_button.pack(padx=10, pady=5)

# Output for decoding
tk.Label(decoding_frame, text="Decoding Result:", bg='white', fg='black').pack(padx=10, pady=5)
decode_result_display = scrolledtext.ScrolledText(decoding_frame, width=80, height=10, wrap=tk.WORD, font=('Arial', 12), bg='white', fg='black')
decode_result_display.pack(padx=10, pady=5)

root.mainloop()
