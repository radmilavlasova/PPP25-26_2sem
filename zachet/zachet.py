def create_board(size):
    return [[' ' for _ in range(size)] for _ in range(size)]

def print_board(board):
    size = len(board)
    print("\n   " + "   ".join(str(i + 1) for i in range(size)))
    print("  " + "-" * (size * 4 + 1))
    for i, row in enumerate(board):
        print(f"{i + 1} | " + " | ".join(row) + " |")
        print("  " + "-" * (size * 4 + 1))
    print()

def check_win(board, player):
    size = len(board)
    
    for row in board:
        if all(cell == player for cell in row):
            return True
        
    for col in range(size):
        if all(board[row][col] == player for row in range(size)):
            return True
            
    if all(board[i][i] == player for i in range(size)):
        return True

    if all(board[i][size - 1 - i] == player for i in range(size)):
        return True
        
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    print("Список доступных команд:")
    print("start - начать игру")
    print("row col - сделать ход (например: 1 2)")
    print("restart - начать игру заново")
    print("exit - выйти из игры\n")

    game_active = False
    board = []
    size = 0
    current_player = 'X'

    while True:
        try:
            user_input = input("Введите команду: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход из игры.")
            break

        if user_input == 'exit':
            print("Выход из игры.")
            break
            
        elif user_input == 'start' or user_input == 'restart':
            while True:
                size_input = input("Выберите размер поля (3 или 4): ").strip()
                if size_input in ['3', '4']:
                    size = int(size_input)
                    break
                else:
                    print("Ошибка: неверный размер! Пожалуйста, введите 3 или 4.")
            
            board = create_board(size)
            current_player = 'X'
            game_active = True
            print("\nИгра началась!")
            print_board(board)
            print(f"Ход игрока {current_player}")
            
        elif game_active:
            parts = user_input.split()
            if len(parts) == 2:
                try:
                    r, c = int(parts[0]) - 1, int(parts[1]) - 1
                    
                    if 0 <= r < size and 0 <= c < size:
                        if board[r][c] == ' ':
                            board[r][c] = current_player
                            print_board(board)

                            if check_win(board, current_player):
                                print(f"Победа! Игрок {current_player} выиграл!")
                                game_active = False
                                print("Введите 'start' или 'restart' для новой игры.")
                            elif check_draw(board):
                                print("Ничья! Свободных клеток больше нет.")
                                game_active = False
                                print("Введите 'start' или 'restart' для новой игры.")
                            else:
                                current_player = 'O' if current_player == 'X' else 'X'
                                print(f"Ход игрока {current_player}")
                        else:
                            print("Ошибка: эта клетка уже занята!")
                    else:
                        print(f"Ошибка: координаты должны быть в пределах от 1 до {size}.")
                except ValueError:
                    print("Ошибка: координаты должны быть числами. Используйте формат: <строка> <столбец> (например, 1 2).")
            else:
                print("Ошибка: неизвестная команда или неверный формат хода. Доступные команды: start, restart, exit, <row> <col>.")
        else:
            print("Игра не запущена. Введите 'start', чтобы начать новую игру.")

if __name__ == "__main__":
    main()
