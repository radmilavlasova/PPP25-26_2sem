#основной код + 5 и 6 доп задания
class Move: #ход
    def __init__(self, piece, start, end, captured_piece=None):
        self.piece = piece
        self.start = start
        self.end = end
        self.captured_piece = captured_piece 
    
    def __str__(self):
        start_notation = f"{chr(self.start[1] + 97)}{8 - self.start[0]}"
        end_notation = f"{chr(self.end[1] + 97)}{8 - self.end[0]}"
        if self.captured_piece:
            return f"{self.piece} {start_notation} x {end_notation} (взял {self.captured_piece})"
        return f"{self.piece} {start_notation} -> {end_notation}"

class Piece: #фигура
    def __init__(self, color):
        self.color = color
        self.symbol = "?"
        self.has_moved = False

    def get_moves(self, board, x, y):
        return []

    def is_valid(self, board, start, end):
        return end in self.get_moves(board, start[0], start[1])

    def __str__(self):
        return self.symbol if self.color == "white" else self.symbol.lower()

class Pawn(Piece): #пешка
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "P"

    def get_moves(self, board, x, y):
        moves = []
        d = -1 if self.color == "white" else 1

        if 0 <= x + d < 8 and board.get(x + d, y) is None:
            moves.append((x + d, y))
            
            if (self.color == "white" and x == 6) or (self.color == "black" and x == 1):
                if 0 <= x + 2*d < 8 and board.get(x + 2*d, y) is None:
                    moves.append((x + 2*d, y))
        
        for dy in [-1, 1]:
            nx, ny = x + d, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board.get(nx, ny)
                if target and target.color != self.color:
                    moves.append((nx, ny))
        
        return moves

class Rook(Piece): #ладья
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "R"

    def get_moves(self, board, x, y):
        moves = []

        for i in range(x+1, 8):
            if board.get(i, y) is None:
                moves.append((i, y))
            else:
                if board.get(i, y).color != self.color:
                    moves.append((i, y))
                break

        for i in range(x-1, -1, -1):
            if board.get(i, y) is None:
                moves.append((i, y))
            else:
                if board.get(i, y).color != self.color:
                    moves.append((i, y))
                break

        for j in range(y+1, 8):
            if board.get(x, j) is None:
                moves.append((x, j))
            else:
                if board.get(x, j).color != self.color:
                    moves.append((x, j))
                break

        for j in range(y-1, -1, -1):
            if board.get(x, j) is None:
                moves.append((x, j))
            else:
                if board.get(x, j).color != self.color:
                    moves.append((x, j))
                break
        return moves

class Knight(Piece): #конь
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "N"

    def get_moves(self, board, x, y):
        moves = []
        for dx, dy in [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board.get(nx, ny)
                if target is None or target.color != self.color:
                    moves.append((nx, ny))
        return moves

class Elephant(Piece): #слон
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "E"

    def get_moves(self, board, x, y):
        moves = []
        for dx, dy in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            for i in range(1, 8):
                nx, ny = x + dx*i, y + dy*i
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                target = board.get(nx, ny)
                if target is None:
                    moves.append((nx, ny))
                else:
                    if target.color != self.color:
                        moves.append((nx, ny))
                    break
        return moves

class Queen(Piece): #ферзь
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "Q"

    def get_moves(self, board, x, y):
        moves = []
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]:
            for i in range(1, 8):
                nx, ny = x + dx*i, y + dy*i
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                target = board.get(nx, ny)
                if target is None:
                    moves.append((nx, ny))
                else:
                    if target.color != self.color:
                        moves.append((nx, ny))
                    break
        return moves

class King(Piece): #король
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "K"

    def get_moves(self, board, x, y):
        moves = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board.get(nx, ny)
                    if target is None or target.color != self.color:
                        moves.append((nx, ny))
        return moves

class Board: #доска
    def __init__(self):
        self.grid = [[None]*8 for _ in range(8)]
        self.current_player = "white"
        self.move_history = [] 
        self.setup()

    def setup(self):
        for i in range(8):
            self.grid[6][i] = Pawn("white")
            self.grid[1][i] = Pawn("black")

        self.grid[7][0] = Rook("white")
        self.grid[7][1] = Knight("white")
        self.grid[7][2] = Elephant("white")
        self.grid[7][3] = Queen("white")
        self.grid[7][4] = King("white")
        self.grid[7][5] = Elephant("white")
        self.grid[7][6] = Knight("white")
        self.grid[7][7] = Rook("white")

        self.grid[0][0] = Rook("black")
        self.grid[0][1] = Knight("black")
        self.grid[0][2] = Elephant("black")
        self.grid[0][3] = Queen("black")
        self.grid[0][4] = King("black")
        self.grid[0][5] = Elephant("black")
        self.grid[0][6] = Knight("black")
        self.grid[0][7] = Rook("black")

    def get(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return self.grid[x][y]
        return None

    def parse_position(self, pos):
        if len(pos) != 2:
            return None
        
        col = pos[0].lower()
        row = pos[1]
        
        if col not in 'abcdefgh' or row not in '12345678':
            return None
        
        y = ord(col) - ord('a')
        x = 8 - int(row)
        
        return (x, y)

    def move(self, move):
        x1, y1 = move.start
        x2, y2 = move.end

        piece = self.grid[x1][y1]

        if piece and piece.color == self.current_player and piece.is_valid(self, move.start, move.end):
            captured = self.grid[x2][y2]
            move.captured_piece = captured
            
            self.grid[x2][y2] = piece
            self.grid[x1][y1] = None
            piece.has_moved = True

            self.move_history.append(move)
            self.current_player = "black" if self.current_player == "white" else "white"
            return True
        return False

    def undo_move(self):
        if not self.move_history:
            print("Нет ходов для отката")
            return False
        
        last_move = self.move_history.pop()
        
        x1, y1 = last_move.start
        x2, y2 = last_move.end
        
        piece = self.grid[x2][y2]
        self.grid[x1][y1] = piece
        self.grid[x2][y2] = last_move.captured_piece
        
        piece.has_moved = False
        
        self.current_player = piece.color
        
        print(f"Откат хода: {last_move}")
        return True

    def undo_multiple_moves(self, count):
        undone = 0
        for i in range(count):
            if self.undo_move():
                undone += 1
            else:
                break
        print(f"\nОткачено {undone} ходов")
        return undone

    def show_history(self):
        if not self.move_history:
            print("\nИстория ходов пуста")
            return
        
        print("\nИстория ходов")
        for i, move in enumerate(self.move_history, 1):
            player = "Белые" if (i % 2 == 1) else "Черные"
            print(f"{i}. {player}: {move}")

    def show(self):
        print("\n   a b c d e f g h")
        for i in range(8):
            print(f"{8 - i} ", end="")
            for j in range(8):
                piece = self.grid[i][j]
                if piece:
                    print(piece, end=" ")
                else:
                    print(".", end=" ")
            print(f"{8 - i}")
        print("   a b c d e f g h")
        print(f"\nХод: {'Белые' if self.current_player == 'white' else 'Черные'}")

class Game: #игра
    def __init__(self):
        self.board = Board()

    def show_piece_moves(self):
        print("\nПросмотр ходов фигуры")
        
        pos_input = input("Введите позицию фигуры (например, e2): ").strip().lower()
        
        if pos_input == '0':
            return False
        
        coords = self.board.parse_position(pos_input)
        if not coords:
            print("Ошибка: Неверный формат. Используйте буквы a-h и цифры 1-8")
            return True
        
        x, y = coords
        piece = self.board.get(x, y)
        
        if not piece:
            print(f"Ошибка: В клетке {pos_input} нет фигуры")
            return True
        
        if piece.color != self.board.current_player:
            print(f"Ошибка: Это {piece.color} фигура. Сейчас ход {self.board.current_player}ых")
            return True
        
        moves = piece.get_moves(self.board, x, y)
        
        if moves:
            print(f"\nВозможные ходы для {piece} на {pos_input}:")
            for move in moves:
                move_notation = f"{chr(move[1] + 97)}{8 - move[0]}"
                target = self.board.get(move[0], move[1])
                if target:
                    print(f"  -> {move_notation} (взять {target})")
                else:
                    print(f"  -> {move_notation}")
        else:
            print(f"\nУ фигуры {piece} на {pos_input} нет доступных ходов")
        
        return True

    def make_move(self):
        print("\nВвод хода")
        
        start_input = input("Откуда (например, e2): ").strip().lower()
        
        if start_input == '0':
            return False
        
        start_coords = self.board.parse_position(start_input)
        if not start_coords:
            print("Ошибка: Неверный формат. Используйте буквы a-h и цифры 1-8")
            return None
        
        x1, y1 = start_coords
        piece = self.board.get(x1, y1)
        
        if not piece:
            print(f"Ошибка: В клетке {start_input} нет фигуры")
            return None
        
        if piece.color != self.board.current_player:
            print(f"Ошибка: Это {piece.color} фигура. Сейчас ход {self.board.current_player}ых")
            return None
        
        print(f"\nВыбрана фигура: {piece} на {start_input}")
        moves = piece.get_moves(self.board, x1, y1)
        
        if not moves:
            print("У этой фигуры нет доступных ходов")
            return None
        
        print("Возможные ходы:")
        for move in moves:
            move_notation = f"{chr(move[1] + 97)}{8 - move[0]}"
            target = self.board.get(move[0], move[1])
            if target:
                print(f"  -> {move_notation} (взять {target})")
            else:
                print(f"  -> {move_notation}")
        
        end_input = input("\nКуда (например, e4): ").strip().lower()
        
        if end_input == '0':
            return False
        
        end_coords = self.board.parse_position(end_input)
        if not end_coords:
            print("Ошибка: Неверный формат")
            return None
        
        x2, y2 = end_coords
        move = Move(piece, (x1, y1), (x2, y2))
        
        if self.board.move(move):
            print(f"\nХод выполнен: {move}")
            return True
        else:
            print("Ошибка: Недопустимый ход")
            return None

    def undo_move(self):
        print("\nОткат хода")
        if self.board.undo_move():
            print("Ход успешно откачен")
            return True
        return False

    def undo_multiple_moves(self):
        print("\nОткат нескольких ходов")
        try:
            count = int(input("Сколько ходов откатить? "))
            if count <= 0:
                print("Введите положительное число")
                return False
            self.board.undo_multiple_moves(count)
            return True
        except ValueError:
            print("Ошибка: Введите число")
            return False

    def play(self):
        print("Добро пожаловать в шахматы!")
        print("\nКоманды:")
        print("  1 - сделать ход")
        print("  2 - показать возможные ходы фигуры")
        print("  3 - показать доску")
        print("  4 - откатить 1 ход")
        print("  5 - откатить несколько ходов")
        print("  6 - показать историю ходов")
        print("  0 - выйти из игры")
        
        while True:
            self.board.show()
            
            if self.is_game_over():
                break
            
            command = input("\nВыберите действие (0-6): ").strip()
            
            if command == '0':
                print("\nИгра завершена")
                break
            
            elif command == '1':
                result = self.make_move()
                if result is False:
                    break
            
            elif command == '2':
                if not self.show_piece_moves():
                    break
            
            elif command == '3':
                continue
            
            elif command == '4':
                self.undo_move()
            
            elif command == '5':
                self.undo_multiple_moves()
            
            elif command == '6':
                self.board.show_history()
            
            else:
                print("Неизвестная команда. Используйте 0-6")
        
        print("\nСпасибо за игру!")

    def is_game_over(self):
        for i in range(8):
            for j in range(8):
                piece = self.board.get(i, j)
                if piece and piece.color == self.board.current_player:
                    moves = piece.get_moves(self.board, i, j)
                    if moves:
                        return False
        print(f"\nИгра окончена! У {self.board.current_player}ых нет доступных ходов.")
        return True

if __name__ == "__main__":
    game = Game()
    game.play()
