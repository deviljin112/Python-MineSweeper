import random
from prettytable import PrettyTable

combos = [
    [0, -1],
    [-1, 0],
    [0, 1],
    [1, 0],
    [-1, -1],
    [1, 1],
    [-1, 1],
    [1, -1],
]


difficulty = {"EASY": 10, "MEDIUM": 40, "EXPERT": 99}

board_size = {"EASY": [9, 9], "MEDIUM": [16, 16], "EXPERT": [30, 16]}


def generate_board(diff):
    size_y = board_size[diff][0]
    size_x = board_size[diff][1]

    board = [[0] * size_x for _ in range(size_y)]

    mines = difficulty[diff]

    added = 0
    while added < mines:
        first = random.randint(0, len(board) - 1)
        second = random.randint(0, len(board[0]) - 1)

        if board[first][second] == 0:
            board[first][second] = "X"
            added += 1

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "X":
                for x in combos:
                    if (
                        x[0] + i < len(board)
                        and x[0] + i >= 0
                        and x[1] + j < len(board[i])
                        and x[1] + j >= 0
                        and board[i + x[0]][j + x[1]] != "X"
                    ):
                        board[i + x[0]][j + x[1]] += 1
    return board


def reveal_empty(p_board, g_board, y, x):
    temp_y = y
    temp_x = x

    options = []
    while True:
        for var in combos:
            new_y = var[0] + temp_y
            new_x = var[1] + temp_x

            if (
                new_y < len(g_board)
                and new_y >= 0
                and new_x < len(g_board[0])
                and new_x >= 0
                and isinstance(g_board[new_y][new_x], int)
                and p_board[new_y][new_x] == "-"
            ):
                p_board[new_y][new_x] = g_board[new_y][new_x]

                if [new_y, new_x] not in options and g_board[new_y][new_x] == 0:
                    options.append([new_y, new_x])

        if len(options) != 0:
            choice = random.choice(options)
            temp_y = choice[0]
            temp_x = choice[1]
            options.remove(choice)
        else:
            break

    return p_board


def move(p_board, g_board, y, x):
    if g_board[y][x] == 0:
        p_board = reveal_empty(p_board, g_board, y, x)

    p_board[y][x] = g_board[y][x]
    return p_board


def board_print(board):
    table = PrettyTable()
    table.header = False
    table.field_names = [f"{i}" for i in range(len(board[0]))]
    for x in board:
        table.add_row(x)

    print(table)


def check_win(p_board, g_board):
    var = False
    win = False

    remaining = 0
    for i in p_board:
        for j in i:
            if j == "X":
                var = True
                win = False
            elif j == "-" and g_board[i][j] != "X":
                remaining += 1

    if remaining == 0:
        var = True
        win = True

    return var, win


def main():
    while True:
        print("Choose difficulty or just say 'exit'.")
        print("Easy / Medium / Expert.")
        choice = input("=> ")

        if choice.upper() in difficulty:
            hidden_board = generate_board(choice.upper())
            player_board = [
                ["-"] * (len(hidden_board[0])) for _ in range(len(hidden_board))
            ]

            board_print(hidden_board)
            board_print(player_board)

            playing = True
            while playing:
                print("Choose a position on the grid.")
                print("Or just say 'exit'.")
                print("Format 'y x'.")

                try:
                    p_choice = input("=> ")

                    move_choice = []
                    if p_choice.upper() == "EXIT":
                        break
                    else:
                        for i in p_choice:
                            if i != " ":
                                move_choice.append(i)

                    y = int(move_choice[0])
                    x = int(move_choice[1])
                except:
                    print("Please only use integers in the specified format!")
                else:
                    player_board = move(player_board, hidden_board, y, x)
                    board_print(player_board)
                    var, win = check_win(player_board, hidden_board)

                    if var and win:
                        print("You win!\nWell done!")
                        playing = False
                    elif var and not win:
                        print("Game over!\nYou lose!")
                        playing = False

            if not playing:
                break

        elif choice.upper() == "EXIT":
            break
        else:
            print("Wrong difficulty!")


if __name__ == "__main__":
    main()