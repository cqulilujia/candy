import random
board_bombs = []
board_display = []
opened = []
flags = []
for i in range(11):
    board_bombs.append([0] * 11)
    board_display.append([0] * 11)
    opened.append([False] * 11)
    flags.append([False] * 11)
def reveal(row, col):
    if row < 1 or row > 10 or col < 1 or col > 10:
        return
    if opened[row][col] or flags[row][col]:
        return
    opened[row][col] = True
    if board_display[row][col] != 0:
        return
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            reveal(row + i, col + j)
def show_board():
    for row in range(1, 11):
        for col in range(1, 11):
            if flags[row][col]:
                print('F', end=' ')
            elif opened[row][col]:
                print(board_display[row][col], end=' ')
            else:
                print('*', end=' ')
        print()
def show_all_board():
    for row in range(1, 11):
        for col in range(1, 11):
            if board_bombs[row][col] == 1:
                print('@', end=' ')
            else:
                print(board_display[row][col], end=' ')
        print()
def display_empty_board():
    for row in range(1, 11):
        for col in range(1, 11):
            print('*', end=' ')
        print()
def get_first_move():
    while True:
        cmd = input().strip()
        if cmd == 'q':
            return None
        if len(cmd) == 3 and cmd[0] == 'r':
            row_char = cmd[1]
            col_char = cmd[2]
            if ('1' <= row_char <= '9') and ('1' <= col_char <= '9'):
                row = int(row_char)
                col = int(col_char)
                return row, col
            else:
                print("坐标必须是1-9之间的数字，请重试")
        else:
            print("输入格式不正确")
def get_move():
    cmd = input().strip()
    if cmd == 'q':
        return 'q', 0, 0
    if len(cmd) == 3:
        action = cmd[0]
        row_char = cmd[1]
        col_char = cmd[2]
        if ('1' <= row_char <= '9') and ('1' <= col_char <= '9'):
            row = int(row_char)
            col = int(col_char)
            return action, row, col
        else:
            print("坐标必须是1-9之间的数字")
    else:
        print("输入格式不正确")
    return None, 0, 0

def place_bombs(first_row, first_col):
    i = 0
    while i < 10:
        x = random.randint(1, 9)
        y = random.randint(1, 9)
        if board_bombs[x][y] == 0 and (x, y) != (first_row, first_col):
            board_bombs[x][y] = 1
            i += 1
def calculate_adjacent_bombs():
    for row in range(1, 11):
        for col in range(1, 11):
            if board_bombs[row][col] == 1:
                board_display[row][col] = '@'
            else:
                count = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        new_row = row + i
                        new_col = col + j
                        if 0 <= new_row < 11 and 0 <= new_col < 11:
                            if board_bombs[new_row][new_col] == 1:
                                count += 1
                board_display[row][col] = count
def check_win():
    for row in range(1, 11):
        for col in range(1, 11):
            if board_bombs[row][col] == 0 and not opened[row][col]:
                return False
    return True
def handle_move(action, row, col):
    if action == 'f':
        flags[row][col] = not flags[row][col]
        return True
    elif action == 'r':
        if board_bombs[row][col] == 1:
            print("踩到炸弹了！游戏结束")
            for r in range(1, 11):
                for c in range(1, 11):
                    if board_bombs[r][c] == 1:
                        opened[r][c] = True
            show_all_board()
            return False
        reveal(row, col)
        return True
    return True
def main():
    print("欢迎玩扫雷游戏！")
    display_empty_board()
    print("输入操作: r行列(揭开) 或 f行列(插旗) 或 q(退出)")
    first_move = get_first_move()
    if first_move is None:
        return
    row, col = first_move
    place_bombs(row, col)
    calculate_adjacent_bombs()
    reveal(row, col)
    game_continue = True
    while game_continue:
        show_board()
        if check_win():
            print("你赢了！")
            break
        print("输入操作: r行列(揭开) 或 f行列(插旗) 或 q(退出)")
        action, row, col = get_move()
        if action == 'q':
            break
        elif action is None:
            continue
        game_continue = handle_move(action, row, col)
main()
