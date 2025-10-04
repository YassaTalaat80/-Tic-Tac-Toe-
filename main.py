class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self, existing_names=[]):
        while True:
            try:
                name = input('Enter your name (letters only): ')
                if name.isalpha():
                    if name in existing_names:
                        print('This name is already taken. Please choose a different name.')
                    else:
                        self.name = name
                        break
                else:
                    print('Invalid name. Please use letters only.')
            except KeyboardInterrupt:
                print("\nGame interrupted by user.")
                return False
        return True

    def choose_symbol(self, existing_symbols=[]):
        while True:
            try:
                if not existing_symbols:
                    symbol = input(f"{self.name}, choose your symbol (X or O): ").upper()
                    if symbol in ['X', 'O']:
                        self.symbol = symbol
                        break
                    else:
                        print('Invalid symbol. Please choose X or O only.')
                else:
                    remaining_symbol = 'O' if existing_symbols[0] == 'X' else 'X'
                    self.symbol = remaining_symbol
                    print(f"{self.name}, your symbol is {remaining_symbol} (automatically assigned)")
                    break
            except KeyboardInterrupt:
                print("\nGame interrupted by user.")
                return False
        return True


class Board:
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]

    def display_board(self):
        for i in range(0, 9, 3):
            print("|".join(self.board[i:i + 3]))
            if i < 6:
                print("-" * 5)

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice - 1] = symbol
            return True
        return False

    def is_valid_move(self, choice):
        return self.board[choice - 1].isdigit()

    def reset_board(self):
        self.board = [str(i) for i in range(1, 10)]


class Menu:
    def display_main_menu(self):
        print("Welcome to my X-O game!")
        print("1. Start Game")
        print("2. Quit Game")

        while True:
            try:
                choice = input("Enter your choice (1 or 2): ")
                if choice in ['1', '2']:
                    return choice
                print("Invalid choice. Please enter 1 or 2.")
            except KeyboardInterrupt:
                print("\nGame interrupted by user.")
                return "2"

    def display_endgame_menu(self):
        menu_text = """Game Over!
1. Restart Game
2. Quit Game
Enter your choice (1 or 2): """

        while True:
            try:
                choice = input(menu_text)
                if choice in ['1', '2']:
                    return choice
                print("Invalid choice. Please enter 1 or 2.")
            except KeyboardInterrupt:
                print("\nGame interrupted by user.")
                return "2"


class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == "1":
            if self.setup_players():
                self.play_game()
        else:
            self.quit_game()

    def setup_players(self):
        existing_names = []
        existing_symbols = []

        for number, player in enumerate(self.players, start=1):
            print(f"Player {number}, enter your details:")

            if not player.choose_name(existing_names):
                return False
            existing_names.append(player.name)

            if not player.choose_symbol(existing_symbols):
                return False
            existing_symbols.append(player.symbol)

            print(f"Player {number} - Name: {player.name}, Symbol: {player.symbol}\n")

        return True

    def play_game(self):
        while True:
            self.play_turn()
            if self.check_win():
                self.board.display_board()
                winner_index = 1 - self.current_player_index
                print(f"{self.players[winner_index].name} wins!")
                choice = self.menu.display_endgame_menu()
                if choice == "1":
                    self.restart_game()
                else:
                    self.quit_game()
                    break
            elif self.check_draw():
                self.board.display_board()
                print("It's a draw!")
                choice = self.menu.display_endgame_menu()
                if choice == "1":
                    self.restart_game()
                else:
                    self.quit_game()
                    break

    def restart_game(self):
        self.board.reset_board()
        self.current_player_index = 0
        print("\n" + "=" * 40)
        print("Game Restarted!")
        print("=" * 40 + "\n")

    def check_win(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for combo in win_combinations:
            if (self.board.board[combo[0]] == self.board.board[combo[1]] ==
                    self.board.board[combo[2]]):
                return True
        return False

    def check_draw(self):
        return all(not cell.isdigit() for cell in self.board.board)

    def play_turn(self):
        player = self.players[self.current_player_index]
        self.board.display_board()
        print(f"{player.name}'s turn ({player.symbol})")

        while True:
            try:
                cell_choice = int(input("Choose a cell (1-9): "))
                if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice, player.symbol):
                    break
                else:
                    print("Invalid move, try again.")
            except (ValueError, KeyboardInterrupt):
                print("Please enter a number between 1 and 9.")

        self.switch_player()

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def quit_game(self):
        print("Thank you for Playing!")


if __name__ == "__main__":
    game = Game()
    game.start_game()