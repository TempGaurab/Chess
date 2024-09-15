import chess
import time

def to_5bit_binary(value, offset):
    return format(value + offset, '06b')

def message_to_binary(message, binary_mapping):
    # Convert each character in the message to its binary representation
    binary_message = ''.join(binary_mapping[char] for char in message)
    return binary_message

def print_board_with_delay(moves_list, delay=2):
    """
    Applies each move to the chess board and prints the board after each move with a delay.
    
    :param moves_list: List of chess moves (Move objects).
    :param delay: Time in seconds to wait between printing boards.
    """
    # Initialize a chess board
    board = chess.Board()
    print()
    # Apply each move, print the board, and wait for the given delay
    for move in moves_list:
        board.push(move)  # Apply the move to the board
        print(board)      # Print the current board state
        print(f"Move played: {move.uci()}\n")  # Print the move in UCI format
        time.sleep(delay)  # Pause for the specified delay (in seconds)
#hello: a2a4a7a5b2b4g8h6g1h3h8g8c2c4b7b5d2d4g8h8e2e4c7c5f2f4d7d5h3g5e7e5g5h7h8g8g2g4f7f5h7f8g7g5f8h7g8h8h2h4a5b4h7f8h8g8f8h7b4b3
def binary_to_chess_moves(binary_message):
    # Initialize a chess board
    board = chess.Board()

    # Create a list to store the moves
    moves_list = []
    for bit in binary_message:
        # Get the list of legal moves at the current board state
        legal_moves = list(board.legal_moves)
        if len(legal_moves) <= 1:
            board.reset()  # No more legal moves
        if bit == '1':
            selected_move = legal_moves[0]  # Pick the first move for '1'
        elif bit == '0':
            selected_move = legal_moves[-1]  # Pick the last move for '0'

        # Append the selected move to the list of moves
        moves_list.append(selected_move)

        # Apply the move to the board
        board.push(selected_move)

    return moves_list, board

def chess_moves_to_binary(moves_list):
    # Initialize a chess board
    board = chess.Board()
    
    # Initialize an empty string to store the binary message
    binary_message = ""

    # For each move in the moves list
    for move in moves_list:
        # Get the list of legal moves at the current board state
        legal_moves = list(board.legal_moves)

        # Check if the move is the first or last legal move
        if move == legal_moves[0]:
            binary_message += '1'  # First move corresponds to '1'
        elif move == legal_moves[-1]:
            binary_message += '0'  # Last move corresponds to '0'
        else:
            raise ValueError(f"Move {move} is not encoded as either first or last move.")

        # Apply the move to the board
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
    
    :param uci_string: String of UCI moves without spaces (e.g., 'a2a4g8h6').
    :return: List of chess.Move objects.
    """
    # Split the UCI string into 4-character chunks (each move in UCI format is 4 characters)
    uci_moves = [uci_string[i:i + 4] for i in range(0, len(uci_string), 4)]
    
    # Convert the UCI move strings into chess.Move objects
    moves_list = [chess.Move.from_uci(move) for move in uci_moves]
    return moves_list

def main():
    letter_offset = 0
    digit_offset = 26

    # Generate mappings for a-z (letters) with offset
    letter_mapping = {chr(i): to_5bit_binary(i - ord('a'), letter_offset) for i in range(ord('a'), ord('z') + 1)}
    
    # Generate mappings for 0-9 (digits) with offset
    digit_mapping = {str(i): to_5bit_binary(i, digit_offset) for i in range(10)}

    # Combine both mappings
    binary_mapping = {**letter_mapping, **digit_mapping}

    # Ask user for encoding or decoding
    user_choice = input("Do you want to encode (e) a message or decode (d) chess moves? ").strip().lower()

    if user_choice == 'e':
        message = input("Enter the message to encode (letters and digits only): ").strip().lower()
        moves_list = encode_message_to_moves(message, binary_mapping)
        print("The message was encoded into the following chess moves:")
        for move in moves_list:
            print(move.uci(), end = "")
        print_board_with_delay(moves_list, delay=2)

    elif user_choice == 'd':
        moves_list = []
        print("Enter the chess moves in UCI format (e.g., e2e4g1f3 wihtout any spaces).")
        move_input = input("Move: ").strip() 
        try:
            moves_list = uci_string_to_moves(move_input)
        except:
            print("Invalid move format, please try again.")

        decoded_message = decode_moves_to_message(moves_list, binary_mapping)
        print(f"The decoded message is: {decoded_message}")
    else:
        print("Invalid option. Please enter 'e' to encode or 'd' to decode.")

if __name__ == "__main__":
    main()
