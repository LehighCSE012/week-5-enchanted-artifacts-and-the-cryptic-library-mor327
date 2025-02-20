import random

def acquire_item(inventory, item):
    """
    Add an item to the inventory.
    
    Args:
        inventory (list): Current inventory
        item (str): Item to add
        
    Returns:
        list: Updated inventory
    """
    if item:
        inventory.append(item)
        print(f"\nYou obtained: {item}")
    return inventory

def discover_artifact(player_stats, artifacts, artifact_name):
    """
    Handle the discovery and application of magical artifacts.
    
    Args:
        player_stats (dict): Player's current statistics
        artifacts (dict): Available artifacts in the game
        artifact_name (str): Name of the artifact to discover
    
    Returns:
        tuple: Updated player_stats and artifacts dictionaries
    """
    # Check if artifact exists using get() method
    artifact = artifacts.get(artifact_name)
    
    if artifact:
        print(f"\nYou found: {artifact['description']}")
        
        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
            print(f"Your health increased by {artifact['power']}!")
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
            print(f"Your attack power increased by {artifact['power']}!")
            
        print(f"Current stats - Health: {player_stats['health']}, Attack: {player_stats['attack']}")
        
        # Remove discovered artifact
        artifacts.pop(artifact_name)
    else:
        print("\nYou found nothing of interest.")
        
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """
    Add new clues to the player's collection if not already known.
    
    Args:
        clues (set): Current set of discovered clues
        new_clue (str): New clue to potentially add
        
    Returns:
        set: Updated clues set
    """
    if new_clue not in clues:  # Using 'in' operator for set membership check
        clues.add(new_clue)    # Using add() method for sets
        print(f"\nYou discovered a new clue: {new_clue}")
    else:
        print("\nYou already know this clue.")
    return clues

def combat_encounter(player_stats, monster_health, has_treasure):
    """
    Handle combat between player and monster.
    
    Args:
        player_stats (dict): Player's current statistics
        monster_health (int): Monster's health
        has_treasure (bool): Whether monster has treasure
        
    Returns:
        str or None: Treasure obtained, if any
    """
    print("\nA monster appears! Combat begins!")
    
    while monster_health > 0 and player_stats['health'] > 0:
        # Player attacks
        damage = player_stats['attack']
        monster_health -= damage
        print(f"\nYou deal {damage} damage. Monster health: {monster_health}")
        
        # Monster attacks if still alive
        if monster_health > 0:
            monster_damage = random.randint(5, 15)
            player_stats['health'] -= monster_damage
            print(f"Monster deals {monster_damage} damage. Your health: {player_stats['health']}")
    
    if player_stats['health'] <= 0:
        print("\nYou have been defeated!")
        return None
    else:
        print("\nYou defeated the monster!")
        if has_treasure:
            return "golden_key"
        return None

def display_player_status(player_stats):
    """Display current player statistics."""
    print(f"\nPlayer Status - Health: {player_stats['health']}, Attack: {player_stats['attack']}")

def display_inventory(inventory):
    """
    Display current inventory items.
    
    Args:
        inventory (list): List of items in inventory
    """
    if inventory:
        print("\nInventory:", ", ".join(inventory))
    else:
        print("\nInventory is empty")

def handle_path_choice(player_stats):
    """Handle player's choice of path."""
    print("\nYou see two paths ahead:")
    print("1. A well-lit path")
    print("2. A dark, mysterious path")
    
    choice = input("\nWhich path do you choose? (1/2): ")
    
    if choice == "2":
        damage = random.randint(5, 15)
        player_stats['health'] -= damage
        print(f"\nYou stumble in the dark and take {damage} damage!")
    else:
        print("\nYou proceed safely along the well-lit path.")
    
    return player_stats

def check_for_treasure(treasure):
    """Check if treasure was obtained."""
    if treasure:
        print(f"\nYou found a {treasure}!")
    else:
        print("\nNo treasure was found.")

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """
    Handle dungeon room exploration.
    
    Args:
        player_stats (dict): Player's current statistics
        inventory (list): Player's inventory
        dungeon_rooms (list): Available rooms
        clues (set): Discovered clues
        
    Returns:
        tuple: Updated player_stats, inventory, and clues
    """
    # Available clues for the Cryptic Library
    library_clues = [
        "The treasure is hidden where the dragon sleeps.",
        "The key lies with the gnome.",
        "Beware the shadows.",
        "The amulet unlocks the final door."
    ]

    for room in dungeon_rooms:
        room_name, item, challenge_type, challenge_outcome = room
        print(f"\nEntering: {room_name}")
        
        if challenge_type == "library":
            print(f"\n{room_name}: A vast library filled with ancient, cryptic texts.")
            
            # Select random clues using random.sample
            selected_clues = random.sample(library_clues, 2)
            for clue in selected_clues:
                clues = find_clue(clues, clue)
            
            # Check if player has staff of wisdom
            if "staff_of_wisdom" in inventory:
                print("\nYour staff of wisdom helps you understand the clues!")
                print("You can now bypass one puzzle challenge.")
                choice = input("Would you like to bypass a puzzle? (y/n): ")
                if choice.lower() == 'y':
                    print("\nYou use your knowledge to bypass the challenge!")
                    continue
        
        elif challenge_type == "puzzle" or challenge_type == "trap":
            success = random.choice([True, False])
            if success:
                print(challenge_outcome[0])  # Success message
                if item:
                    inventory = acquire_item(inventory, item)
            else:
                print(challenge_outcome[1])  # Failure message
                player_stats['health'] += challenge_outcome[3]  # Apply health change
        
        elif item:
            inventory = acquire_item(inventory, item)
        
        display_player_status(player_stats)
        if player_stats['health'] <= 0:
            print("\nGame Over!")
            break
    
    return player_stats, inventory, clues

def main():
    """Main game loop."""
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
            "description": "Glowing amulet, life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "Powerful ring, attack boost.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "Staff of wisdom, ancient.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }
    
    has_treasure = random.choice([True, False])
    
    print("Welcome to the Dungeon Adventure!")
    display_player_status(player_stats)
    player_stats = handle_path_choice(player_stats)
    
    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat is not None:
            check_for_treasure(treasure_obtained_in_combat)
            inventory = acquire_item(inventory, treasure_obtained_in_combat)
        
        # 30% chance to find an artifact after combat
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
            print("Final Inventory:")
            display_inventory(inventory)
            print("\nClues Discovered:")
            if clues:
                for clue in clues:
                    print(f"- {clue}")
            else:
                print("No clues discovered.")

if __name__ == "__main__":
    main()