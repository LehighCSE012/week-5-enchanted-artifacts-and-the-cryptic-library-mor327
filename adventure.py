import random

def discover_artifact(player_stats, artifacts, artifact_name):
    """
    Discovers an artifact and applies its effects to the player's stats.

    Parameters:
        player_stats (dict): Dictionary containing the player's health and attack stats.
        artifacts (dict): Dictionary containing artifact information.
        artifact_name (str): The name of the artifact to discover.

    Returns:
        tuple: Updated player_stats and artifacts dictionaries.
    """
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"You found an artifact: {artifact['description']}")

        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
            print(f"Your health increased by {artifact['power']}.")
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
            print(f"Your attack increased by {artifact['power']}.")

        # Remove the artifact from the dictionary
        artifacts.pop(artifact_name)
    else:
        print("You found nothing of interest.")

    return player_stats, artifacts

def find_clue(clues, new_clue):
    """
    Adds a unique clue to the player's clue set.

    Parameters:
        clues (set): Set of collected clues.
        new_clue (str): The clue to add.

    Returns:
        set: Updated set of clues.
    """
    if new_clue not in clues:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """
    Handles the player's interaction with dungeon rooms.

    Parameters:
        player_stats (dict): Player's stats (health and attack).
        inventory (list): Player's inventory.
        dungeon_rooms (list): List of dungeon rooms and their attributes.
        clues (set): Set of collected clues.

    Returns:
        tuple: Updated player_stats, inventory, and clues.
    """
    for room in dungeon_rooms:
        room_name, item, challenge_type, challenge_outcome = room
        print(f"You enter the {room_name}.")

        if room_name == "Cryptic Library":
            print("A vast library filled with ancient, cryptic texts.")
            possible_clues = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door."
            ]
            selected_clues = random.sample(possible_clues, 2)
            for clue in selected_clues:
                clues = find_clue(clues, clue)

            if "staff_of_wisdom" in inventory:
                print("Using the Staff of Wisdom, you understand the meaning of the clues.")
                print("You can bypass a puzzle challenge in another room.")
                # Logic to bypass a puzzle challenge can be added here.

        elif challenge_type == "puzzle":
            print(challenge_outcome[0] if random.choice([True, False]) else challenge_outcome[1])
            player_stats['health'] += challenge_outcome[2]

        elif challenge_type == "trap":
            print(challenge_outcome[0] if random.choice([True, False]) else challenge_outcome[1])
            player_stats['health'] += challenge_outcome[2]

        if item:
            inventory.append(item)
            print(f"You found a {item}!")

        print(f"Current Health: {player_stats['health']}")
        print("---")

    return player_stats, inventory, clues

def combat_encounter(player_stats, monster_health, has_treasure):
    """
    Simulates a combat encounter between the player and a monster.

    Parameters:
        player_stats (dict): Player's stats (health and attack).
        monster_health (int): Monster's health points.
        has_treasure (bool): Whether the monster guards a treasure.

    Returns:
        str: Treasure obtained if the player wins, otherwise None.
    """
    print("A monster attacks!")

    while player_stats['health'] > 0 and monster_health > 0:
        print(f"Player Health: {player_stats['health']}, Monster Health: {monster_health}")
        monster_health -= player_stats['attack']
        if monster_health > 0:
            player_stats['health'] -= 10

    if player_stats['health'] > 0:
        print("You defeated the monster!")
        return "treasure" if has_treasure else None
    else:
        print("You were defeated by the monster.")
        return None

def display_player_status(player_stats):
    """
    Displays the player's current health and attack stats.

    Parameters:
        player_stats (dict): Player's stats (health and attack).
    """
    print(f"Player Health: {player_stats['health']}, Player Attack: {player_stats['attack']}")

def main():
    """
    Main game loop.
    """
    dungeon_rooms = [
        ("Dusty library", "key", "puzzle", ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]

    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()

    artifacts = {
        "amulet_of_vitality": {
            "description": "A glowing amulet that enhances your life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "A powerful ring that boosts your attack damage.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "A staff imbued with ancient wisdom.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }

    has_treasure = random.choice([True, False])

    display_player_status(player_stats)

    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat:
            print(f"You obtained a {treasure_obtained_in_combat}!")

        if random.random() < 0.3:
            artifact_keys = list(artifacts.keys())
            if artifact_keys:
                artifact_name = random.choice(artifact_keys)
                player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
                display_player_status(player_stats)

        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues)
            print("\n--- Game End ---")
            display_player_status(player_stats)
            print("Final Inventory:", inventory)
            print("Clues:")
            if clues:
                for clue in clues:
                    print(f"- {clue}")
            else:
                print("No clues.")

if __name__ == "__main__":
    main()
