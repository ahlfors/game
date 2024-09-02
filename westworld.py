import os
import random

class Player:
    def __init__(self, name, symbol, x, y):
        self.name = name
        self.symbol = symbol
        self.x = x
        self.y = y
        self.has_shot = False  # Track whether the player has shot

    def move(self, direction, max_x, max_y, walls, mines):
        new_x, new_y = self.x, self.y

        if direction == 'w':
            new_y -= 1
        elif direction == 's':
            new_y += 1
        elif direction == 'a':
            new_x -= 1
        elif direction == 'd':
            new_x += 1
        elif direction == 'i':
            new_y -= 1
        elif direction == 'k':
            new_y += 1
        elif direction == 'j':
            new_x -= 1
        elif direction == 'l':
            new_x += 1

        if 0 <= new_x < max_x and 0 <= new_y < max_y:
            if (new_x, new_y) not in walls:
                self.x, self.y = new_x, new_y
            else:
                return True, False  # Player self-destructs if hitting a wall
        else:
            return True, False  # Player self-destructs if moving out of bounds

        # Check if player stepped on a mine
        if (self.x, self.y) in mines:
            return False, True  # Player stepped on a mine

        return False, False  # Player didn't self-destruct and didn't hit a mine

    def can_shoot(self, other_player, walls):
        if self.x == other_player.x:
            if self.y < other_player.y:
                for y in range(self.y + 1, other_player.y):
                    if (self.x, y) in walls:
                        return False  # Wall blocks the shot
            else:
                for y in range(other_player.y + 1, self.y):
                    if (self.x, y) in walls:
                        return False  # Wall blocks the shot
            return True
        elif self.y == other_player.y:
            if self.x < other_player.x:
                for x in range(self.x + 1, other_player.x):
                    if (x, self.y) in walls:
                        return False  # Wall blocks the shot
            else:
                for x in range(other_player.x + 1, self.x):
                    if (x, self.y) in walls:
                        return False  # Wall blocks the shot
            return True
        return False

    def shoot(self, other_player, walls):
        if self.has_shot:
            return False  # Player has already shot
        if self.can_shoot(other_player, walls):
            self.has_shot = True
            return True
        return False

def print_board(player1, player2, max_x, max_y, walls, mines, revealed_mines):
    board = [['.' for _ in range(max_x)] for _ in range(max_y)]

    # Place walls
    for wall in walls:
        board[wall[1]][wall[0]] = '+'

    # Place revealed mines
    for mine in mines:
        if mine in revealed_mines:
            board[mine[1]][mine[0]] = '?'

    # Place players
    board[player1.y][player1.x] = '\033[91m●\033[0m'  # Player 1 represented by red ●
    board[player2.y][player2.x] = '\033[94m●\033[0m'  # Player 2 represented by blue ●

    # Print the board
    for row in board:
        print(' '.join(row))
    print()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_walls(max_x, max_y, num_walls):
    walls = set()
    while len(walls) < num_walls:
        wall_x = random.randint(0, max_x - 1)
        wall_y = random.randint(0, max_y - 1)
        # Ensure walls do not overlap with player starting positions
        if (wall_x, wall_y) not in walls:
            walls.add((wall_x, wall_y))
    return walls

def generate_mines(max_x, max_y, num_mines, walls, players):
    mines = set()
    while len(mines) < num_mines:
        mine_x = random.randint(0, max_x - 1)
        mine_y = random.randint(0, max_y - 1)
        if (mine_x, mine_y) not in mines and (mine_x, mine_y) not in walls and (mine_x, mine_y) not in [(player.x, player.y) for player in players]:
            mines.add((mine_x, mine_y))
    return mines

def reveal_mines_near_player(player, mines):
    revealed_mines = set()
    for mine in mines:
        if abs(mine[0] - player.x) <= 1 and abs(mine[1] - player.y) <= 1:
            revealed_mines.add(mine)
    return revealed_mines

def game():
    max_x, max_y = 10, 10  # Expanded map size
    num_walls = 20  # Number of walls to place on the map
    num_mines = 4  # Number of mines to place on the map

    walls = generate_walls(max_x, max_y, num_walls)

    # Initialize player positions
    player1 = Player('Player 1', '1', random.randint(0, max_x - 1), random.randint(0, max_y - 1))
    player2 = Player('Player 2', '2', random.randint(0, max_x - 1), random.randint(0, max_y - 1))

    # Ensure players do not start on the same position, row, or column
    while ((player1.x == player2.x) or (player1.y == player2.y) or
           (player1.x, player1.y) in walls or (player2.x, player2.y) in walls or
           (player1.x, player1.y) == (player2.x, player2.y)):
        player1 = Player('Player 1', '1', random.randint(0, max_x - 1), random.randint(0, max_y - 1))
        player2 = Player('Player 2', '2', random.randint(0, max_x - 1), random.randint(0, max_y - 1))

    # Generate mines
    mines = generate_mines(max_x, max_y, num_mines, walls, [player1, player2])
    revealed_mines = set()

    while True:
        clear_console()
        print_board(player1, player2, max_x, max_y, walls, mines, revealed_mines)

        while True:
            move1 = input("Player 1 Move (WASD) or Shoot (F): ").lower()
            if move1 in ['w', 'a', 's', 'd']:
                self_destruct, stepped_on_mine = player1.move(move1, max_x, max_y, walls, mines)
                if stepped_on_mine:
                    clear_console()
                    print_board(player1, player2, max_x, max_y, walls, mines, revealed_mines)
                    print("Player 1 stepped on a mine! Player 2 Wins!")
                    return
                if self_destruct:
                    clear_console()
                    print_board(player1, player2, max_x, max_y, walls, mines, revealed_mines)
                    print("Player 1 ran into a wall and self-destructed!")
                    print("Player 2 Wins!")
                    return
                # Reveal mines near Player 1
                revealed_mines.update(reveal_mines_near_player(player1, mines))
                clear_console()
                print_board(player1, player2, max_x, max_y, walls, mines, revealed_mines)
                break
            elif move1 == 'f':
                if player1.shoot(player2, walls):
                    clear_console()
                    print_board(player1, player2, max_x, max_y, walls, mines, revealed_mines)
                    print("Player 1 Wins!")
                    return
                else:
                    clear_console()
                    print_board(player1, player2, max_x, max_y, walls, mines, revealed_mines)
                    print("Player 1's shot was blocked by a wall or has already been used. Player 2 Wins!")
                    return
            else:
                print("Invalid input! Please use WASD for movement or F to shoot.")

        while True:
            move2 = input("Player 2 Move (IJKL) or Shoot (H): ").lower()
            if move2 in ['i', 'j', 'k', 'l']:
                self_destruct, stepped_on_mine = player2.move(move2, max_x, max_y, walls, mines)
                if stepped_on_mine:
                    clear_console()
                    print_board(player1, player2, max_x, max_y, walls, mines, revealed_mines)
                    print("Player 2 stepped on a mine! Player 1 Wins!")
                    return
                if self_destruct:
                    clear_console()
                    print_board(player1, player2, max_x, max_y, walls, mines, revealed_mines)
                    print("Player 2 ran into a wall and self-destructed!")
                    print("Player 1 Wins!")
                    return
                # Reveal mines near Player 2
                revealed_mines.update(reveal_mines_near_player(player2, mines))
                clear_console()
                print_board(player1, player2, max_x, max_y, walls, mines, revealed_mines)
                break
            elif move2 == 'h':
                if player2.shoot(player1, walls):
                    clear_console()
                    print_board(player1, player2, max_x, max_y, walls, mines, revealed_mines)
                    print("Player 2 Wins!")
                    return
                else:
                    clear_console()
                    print_board(player1, player2, max_x, max_y, walls, mines, revealed_mines)
                    print("Player 2's shot was blocked by a wall or has already been used. Player 1 Wins!")
                    return
            else:
                print("Invalid input! Please use IJKL for movement or H to shoot.")

if __name__ == "__main__":
    game()
