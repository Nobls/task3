import hashlib
import hmac
import os
import random
import sys

class MoveResult:
    def __init__(self, move1, move2, result):
        self.move1 = move1
        self.move2 = move2
        self.result = result

class MoveTable:
    def __init__(self, moves):
        self.moves = moves
        self.results = self.generate_results()

    def generate_results(self):
        n = len(self.moves)
        results = [[None] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    results[i][j] = 'Draw'
                else:
                    diff = (j - i) % n
                    if 1 <= diff <= n // 2:
                        results[i][j] = 'Win'
                    else:
                        results[i][j] = 'Lose'
        return results

    def get_result(self, move1, move2):
        i = self.moves.index(move1)
        j = self.moves.index(move2)
        return self.results[i][j]

    def show(self):
        print("Results table:")
        header = [""] + self.moves
        print(" ".join(header))
        for i, row in enumerate(self.results):
            row_str = [self.moves[i]] + row
            print(" ".join(row_str))

class Game:
    def __init__(self, moves):
        self.moves = moves
        if len(self.moves) % 2 == 0:
            print('Invalid input. Please provide an odd number of unique moves.')
            sys.exit(1)
        self.hmac_key = self.generate_hmac_key()
        self.computer_move = self.get_computer_move()
        self.move_table = MoveTable(self.moves)

    def generate_hmac_key(self):
        return os.urandom(32)

    def get_computer_move(self):
        return random.choice(self.moves)

    def calculate_hmac(self, move):
        hm = hmac.new(self.hmac_key, move.encode(), hashlib.sha256)
        return hm.hexdigest()

    def play(self, user_move):
        if user_move == "0":
            sys.exit(0)
        elif user_move == "?":
            self.move_table.show()
            return

        user_move = user_move.strip().capitalize()
        try:
            user_move = int(user_move)
            if user_move < 1 or user_move > len(self.moves):
                raise ValueError
            user_move = self.moves[user_move - 1]
        except ValueError:
            print("Invalid move. Please try again.")
            return

        computer_move = self.computer_move
        result = self.move_table.get_result(user_move, computer_move)

        print(f'HMAC: {self.calculate_hmac(user_move)}')
        print(f'Computer move: {computer_move}')
        print(f'Your move: {user_move}')
        print(f'Result: {result}')

        print(f'HMAC key: {self.hmac_key.hex()}')

    def show_help(self):
        print("Available moves:")
        for i, move in enumerate(self.moves, start=1):
            print(f'{i} - {move}')
        print("0 - exit")
        print("? - help")

class MainGame:
    def __init__(self, moves):
        self.moves = moves
        self.game = Game(moves)

    def run(self):
        while True:
            print(f'Available moves: {", ".join(self.moves)}')
            print('Your move: Enter 0 to exit, ? for help')
            user_move = input()
            self.game.play(user_move)

if __name__ == '__main__':
    if len(sys.argv) < 4 or len(set(sys.argv[1:])) != len(sys.argv[1:]):
        print('Invalid input. Please provide an odd number of unique moves.')
        sys.exit(1)

    moves = sys.argv[1:]
    main_game = MainGame(moves)
    main_game.run()

