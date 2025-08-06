def is_winner(board, player):
    # Check if the player has won horizontally, vertically, or diagonally
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    return all(board[i][j] != '' for i in range(3) for j in range(3))

def count_valid_states(board, player):
    if is_winner(board, 'X') or is_winner(board, 'O') or is_board_full(board):
        return 1
    
    count = 0
    next_player = 'X' if player == 'O' else 'O'
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = player
                count += count_valid_states(board, next_player)
                board[i][j] = ''  # Reset the cell to its empty state after checking
        
    return count

if __name__ == "__main__":
    # Initialize an empty 3x3 board
    board = [['' for _ in range(3)] for _ in range(3)]

    # Start counting valid states with the first player as 'X'
    total_valid_states = count_valid_states(board, 'X')
    print("Total number of valid states in Tic-Tac-Toe:", total_valid_states)
