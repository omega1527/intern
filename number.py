import random, time, json, os

STATS_FILE = 'game_stats.json'

def load_stats():
    return json.load(open(STATS_FILE)) if os.path.exists(STATS_FILE) else {}

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=4)

def get_difficulty():
    choices = {
        "easy": (1, 50, 10),
        "medium": (1, 100, 7),
        "hard": (1, 200, 5)
    }
    while True:
        level = input("Difficulty (easy/medium/hard/custom): ").strip().lower()
        if level in choices:
            return choices[level]
        if level == "custom":
            try:
                low = int(input("Lower bound: "))
                high = int(input("Upper bound: "))
                attempts = int(input("Attempts: "))
                if low < high and attempts > 0:
                    return low, high, attempts
            except:
                pass
            print("Invalid custom settings.")
        else:
            print("Choose a valid difficulty.")

def give_hint(guess, target):
    diff = abs(guess - target)
    base = "Too low!" if guess < target else "Too high!"
    if diff <= 5: return f"{base} Very close!"
    if diff <= 15: return f"{base} Warm."
    return f"{base} Cold."

def update_stats(stats, player, won, tries):
    p = stats.setdefault(player, {"played": 0, "won": 0, "total": 0, "best": None})
    p["played"] += 1
    p["total"] += tries
    if won:
        p["won"] += 1
        if not p["best"] or tries < p["best"]:
            p["best"] = tries

def show_stats(player, stats):
    if player not in stats:
        print("No data yet.")
        return
    s = stats[player]
    avg = s["total"] / s["played"]
    print(f"Stats for {player} - Played: {s['played']}, Won: {s['won']}, Best: {s['best'] or '-'}, Avg: {avg:.2f}")

def show_leaderboard(stats):
    top = sorted(stats.items(), key=lambda x: x[1].get("best") or float('inf'))[:5]
    print("\nLeaderboard:")
    for name, s in top:
        avg = s["total"] / s["played"]
        print(f"{name}: Won {s['won']} | Best {s.get('best', '-')}, Avg {avg:.2f}")
    print()

def play(player, stats):
    low, high, max_tries = get_difficulty()
    target = random.randint(low, high)
    tries = 0
    start = time.time()

    print(f"Guess a number between {low} and {high}. You have {max_tries} attempts.")

    while tries < max_tries:
        guess = input(f"Try {tries + 1}/{max_tries} (or 'quit'): ").strip()
        if guess.lower() == 'quit':
            print("Game exited.")
            return
        if not guess.isdigit() or not (low <= int(guess) <= high):
            print(f"Guess a number in range {low}-{high}.")
            continue
        guess = int(guess)
        tries += 1
        if guess == target:
            print(f"Correct! The number was {target}. Attempts: {tries}")
            update_stats(stats, player, True, tries)
            break
        else:
            print(give_hint(guess, target))
    else:
        print(f"No attempts left. The number was {target}.")
        update_stats(stats, player, False, tries)

    print(f"Time taken: {time.time() - start:.1f} seconds")

def main():
    stats = load_stats()
    print("Welcome to the Number Guessing Game!")
    player = input("Your name: ").strip() or "Player"

    while True:
        print("\n1. Play\n2. My Stats\n3. Leaderboard\n4. Exit")
        choice = input("Choose: ").strip()
        if choice == '1':
            play(player, stats)
            save_stats(stats)
        elif choice == '2':
            show_stats(player, stats)
        elif choice == '3':
            show_leaderboard(stats)
        elif choice == '4':
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
