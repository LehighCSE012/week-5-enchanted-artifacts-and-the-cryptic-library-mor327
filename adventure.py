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

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts):
    """
    Simulates the player entering a dungeon and interacting with various rooms.

    Parameters:
        player_stats (dict): Player's stats, including health and attack.
        inventory (list): List of items the player is carrying.
        dungeon_rooms (list of tuples): Each tuple represents a room in the format
                                         (room_name, item, challenge_type, challenge_outcome).
        clues (set): A set of clues the player has discovered.
        artifacts (dict): A dictionary to store collected artifacts.

    Returns:
        None
    """
    for room in dungeon_rooms:
        try:
            room_name, item, challenge_type, challenge_outcome = room
        except ValueError:
            raise TypeError("Each room in dungeon_rooms must be a tuple with four elements.")

        print(f"Entering {room_name}...")
        
        # Add item to inventory if present
        if item:
            inventory.append(item)
            print(f"Collected item: {item}")

        # Handle challenges
        if challenge_type == "none":
            print("No challenge here. Proceeding to the next room.")
        elif challenge_type == "puzzle":
            if isinstance(challenge_outcome, tuple) and len(challenge_outcome) == 3:
                success_msg, fail_msg, health_penalty = challenge_outcome
                # Simulate puzzle success or failure (for simplicity, always success here)
                print(success_msg)
            else:
                raise TypeError("Puzzle challenge_outcome must be a tuple (success_msg, fail_msg, health_penalty).")
        elif challenge_type == "trap":
            if isinstance(challenge_outcome, tuple) and len(challenge_outcome) == 3:
                success_msg, fail_msg, health_penalty = challenge_outcome
                # Simulate trap failure (for simplicity, always fail here)
                player_stats["health"] -= health_penalty
                print(fail_msg)
                print(f"Health reduced by {health_penalty}. Current health: {player_stats['health']}")
            else:
                raise TypeError("Trap challenge_outcome must be a tuple (success_msg, fail_msg, health_penalty).")
        elif challenge_type == "library":
            print("Discovered a library. Found a new clue!")
            clues.add(f"Clue from {room_name}")
        else:
            raise ValueError(f"Unknown challenge type: {challenge_type}")

        # End dungeon if health drops to 0 or below
        if player_stats["health"] <= 0:
            print("Player has succumbed to their injuries. Game over!")
            break

    print("Dungeon exploration complete.")
    print(f"Final stats: {player_stats}")
    print(f"Inventory: {inventory}")
    print(f"Clues: {clues}")
    print(f"Artifacts: {artifacts}")


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
