import random

# Game Constants
COLORS = ["Red", "Blue", "Yellow", "Green"]
GENRES = {
    "Red": "History",
    "Blue": "Science",
    "Yellow": "Pop Culture",
    "Green": "Geography"
}

class Player:
    def __init__(self, matrix_size):
        self.hearts = 3
        self.current_room = 1
        self.potion_guesses = 3
        self.matrix_size = matrix_size
        self.potion_grid = [["?" for _ in range(matrix_size)] for _ in range(matrix_size)]
        self.potion_x = random.randint(0, matrix_size - 1)
        self.potion_y = random.randint(0, matrix_size - 1)
        
        # TRACKER: Stores tuples of (room_number, color, set_number)
        self.used_questions = set()

def wizard_speak(message):
    print(f"\n✨ [Wizard]: {message}")

def display_stats(player):
    heart_display = "❤️ " * player.hearts
    empty_display = "🖤 " * (3 - player.hearts)
    print("\n" + "═" * 45)
    print(f"  LOCATION: Room {player.current_room}/8")
    print(f"  HEALTH:   {heart_display}{empty_display} ({player.hearts}/3)")
    print(f"  POTIONS:  {player.potion_guesses} guesses remaining")
    print("═" * 45)

def print_potion_grid(player):
    print("\n    " + " ".join([str(i+1) for i in range(player.matrix_size)]))
    print("    " + "--" * player.matrix_size)
    for idx, row in enumerate(player.potion_grid):
        print(f"{idx+1} | " + " ".join(row))

def play_potion_game(player):
    print("\n--- 🧪 THE ALCHEMIST'S MATRIX 🧪 ---")
    print_potion_grid(player)
    
    while True:
        try:
            gx = int(input(f"Enter Column (1-{player.matrix_size}): ")) - 1
            gy = int(input(f"Enter Row (1-{player.matrix_size}): ")) - 1
            if not (0 <= gx < player.matrix_size and 0 <= gy < player.matrix_size):
                print(f"❌ Coordinates outside the {player.matrix_size}x{player.matrix_size} matrix!")
                continue
            if player.potion_grid[gy][gx] == "X":
                print("❌ You've already searched there! Try again.")
                continue
            break
        except ValueError:
            print("❌ Please enter valid numbers.")

    if gx == player.potion_x and gy == player.potion_y:
        player.potion_grid[gy][gx] = "🧪"
        print_potion_grid(player)
        player.hearts += 1
        wizard_speak("GLORIOUS! You found the essence. (+1 Heart)")
        player.potion_x = random.randint(0, player.matrix_size - 1)
        player.potion_y = random.randint(0, player.matrix_size - 1)
    else:
        player.potion_grid[gy][gx] = "X"
        player.potion_guesses -= 1
        print_potion_grid(player)
        wizard_speak(f"Nothing... You have {player.potion_guesses} guesses left.")

def ask_question(player, level, color, is_ladder=False):
    """Selects an unused set (1, 2, or 3) for the given level and color."""
    genre = GENRES[color]
    difficulty_label = "HARD (LADDER)" if is_ladder else "NORMAL"
    
    # Define available sets
    all_sets = [1, 2, 3]
    
    # Filter out sets already used for THIS room and THIS color
    available_sets = [s for s in all_sets if (level, color, s) not in player.used_questions]
    
    # If the player is stuck and used all 3 sets, we clear history for this specific door to avoid a crash
    if not available_sets:
        wizard_speak("You've seen all my riddles for this door... I shall reuse one.")
        available_sets = [1, 2, 3]
    
    chosen_set = random.choice(available_sets)
    
    # Log this question as used
    player.used_questions.add((level, color, chosen_set))
    
    print(f"\n" + "─" * 30)
    print(f"📝 QUESTION CHALLENGE")
    print(f"   GENRE: {genre} ({color})")
    print(f"   LEVEL: {level}")
    print(f"   SET #: {chosen_set}")
    print(f"   DIFFICULTY: {difficulty_label}")
    print(f"─" * 30)
    
    wizard_speak(f"Answer this riddle from Set {chosen_set} of the {genre} archives!")
    print("(Type 'win' for correct, 'lose' for incorrect)")
    
    answer = input("Your Answer: ").lower()
    return answer == "win"

def check_room_features(player):
    if player.current_room in [2, 4, 6]:
        display_stats(player)
        wizard_speak(f"A shifting ladder appears in Room {player.current_room}!")
        
        even_room_map = {2: 4, 4: 6, 6: 8}
        target = even_room_map[player.current_room]
        
        choice = input(f"🪜 Risk a 'HARD' question to jump to Room {target}? (y/n): ").lower()
        if choice == 'y':
            # Ladders use 'Magic' as a generic color or you can pick one
            if ask_question(player, player.current_room, random.choice(COLORS), is_ladder=True):
                wizard_speak(f"Incredible! You teleport to Room {target}.")
                player.current_room = target
            else:
                wizard_speak("The ladder becomes a snake! You lose a heart and fall back.")
                player.hearts -= 1
                player.current_room -= 1
    return False

def main_game():
    wizard_speak("Welcome, traveler! Choose the size of the potion matrix.")
    print("EASY: 3x3 | MEDIUM: 4x4 | HARD: 5x5 (3 guesses total)")
    
    difficulty_choice = ""
    while difficulty_choice not in ["easy", "medium", "hard"]:
        difficulty_choice = input("\nDifficulty: ").lower()
    
    m_size = 3 if difficulty_choice == "easy" else 4 if difficulty_choice == "medium" else 5
    player = Player(m_size)

    while player.current_room <= 8 and player.hearts > 0:
        room_cleared = False
        
        while not room_cleared and player.hearts > 0:
            display_stats(player)
            
            if player.hearts < 3 and player.potion_guesses > 0:
                if input("Search the matrix for a potion? (y/n): ").lower() == 'y':
                    play_potion_game(player)
                    display_stats(player)

            if player.hearts <= 0: break

            portal_color = random.choice(COLORS)
            wizard_speak(f"The portal is {portal_color}. Roll the die!")
            input("Press Enter to roll...")
            roll = random.choice(COLORS)
            print(f"🎲 Roll: {roll}")

            if roll == portal_color:
                wizard_speak("Match! You move forward.")
                room_cleared = True
            else:
                decision = input(f"No match. (1) Roll again (Risk 1 Heart) or (2) Answer a {portal_color} question? ")
                
                if decision == "1":
                    roll = random.choice(COLORS)
                    print(f"🎲 Second roll: {roll}")
                    if roll == portal_color:
                        wizard_speak("Lucky! You pass.")
                        room_cleared = True
                    else:
                        player.hearts -= 1
                        wizard_speak("Failure! Heart lost. You must restart the challenge.")
                
                elif decision == "2":
                    # Pass the player object so we can track used questions
                    if ask_question(player, player.current_room, portal_color):
                        wizard_speak("Correct! You pass.")
                        room_cleared = True
                    else:
                        player.hearts -= 1
                        wizard_speak("INCORRECT! You lose a heart and remain here.")

        if player.hearts > 0:
            player.current_room += 1
            if player.current_room <= 8:
                check_room_features(player)

    if player.hearts <= 0:
        display_stats(player)
        wizard_speak("The darkness consumes you. GAME OVER.")
    else:
        wizard_speak("You have escaped the 8 Rooms! VICTORY!")

if __name__ == "__main__":
    main_game()