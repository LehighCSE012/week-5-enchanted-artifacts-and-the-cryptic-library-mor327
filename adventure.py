import random
from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Tuple, Any

@dataclass
class PlayerStats:
    health: int
    attack: int

@dataclass
class Artifact:
    description: str
    power: int
    effect: str

@dataclass
class Room:
    name: str
    item: Optional[str]
    challenge_type: str
    challenge_outcome: Optional[Tuple[str, str, int]]

    @classmethod
    def from_tuple(cls, room_tuple: Tuple[str, Optional[str], str, Optional[Tuple[str, str, int]]]) -> 'Room':
        """Creates a Room instance from a tuple, with validation."""
        if len(room_tuple) != 4:
            raise TypeError("Room tuple must have exactly 4 elements")
        
        name, item, challenge_type, challenge_outcome = room_tuple
        
        if not isinstance(name, str):
            raise TypeError("Room name must be a string")
        
        if item is not None and not isinstance(item, str):
            raise TypeError("Room item must be None or a string")
            
        if not isinstance(challenge_type, str):
            raise TypeError("Challenge type must be a string")
            
        if challenge_type in ["puzzle", "trap"]:
            if not (isinstance(challenge_outcome, tuple) and len(challenge_outcome) == 3):
                raise TypeError("Challenge outcome for puzzle/trap must be a tuple of (success_msg, fail_msg, health_change)")
        
        return cls(name, item, challenge_type, challenge_outcome)

class DungeonGame:
    VALID_CHALLENGE_TYPES = {"none", "puzzle", "trap", "library"}
    
    def __init__(self):
        self.player_stats = PlayerStats(health=100, attack=5)
        self.inventory: List[str] = []
        self.clues: Set[str] = set()
        self.artifacts: Dict[str, Artifact] = {
            "amulet_of_vitality": Artifact(
                "A glowing amulet that enhances your life force.",
                15,
                "increases health"
            ),
            "ring_of_strength": Artifact(
                "A powerful ring that boosts your attack damage.",
                10,
                "enhances attack"
            ),
            "staff_of_wisdom": Artifact(
                "A staff imbued with ancient wisdom.",
                5,
                "solves puzzles"
            )
        }

    def validate_dungeon_rooms(self, dungeon_rooms: List[Tuple[str, Optional[str], str, Any]]) -> List[Room]:
        """Validates dungeon rooms structure and converts to Room objects."""
        validated_rooms = []
        for room_tuple in dungeon_rooms:
            try:
                room = Room.from_tuple(room_tuple)
                if room.challenge_type not in self.VALID_CHALLENGE_TYPES:
                    raise ValueError(f"Invalid challenge type: {room.challenge_type}")
                validated_rooms.append(room)
            except (TypeError, ValueError) as e:
                raise TypeError(f"Invalid room structure: {e}")
        return validated_rooms

    def discover_artifact(self, artifact_name: str) -> None:
        """Discovers an artifact and applies its effects to the player's stats."""
        if artifact_name not in self.artifacts:
            print("You found nothing of interest.")
            return

        artifact = self.artifacts[artifact_name]
        print(f"You found an artifact: {artifact.description}")

        if artifact.effect == "increases health":
            self.player_stats.health += artifact.power
            print(f"Your health increased by {artifact.power}.")
        elif artifact.effect == "enhances attack":
            self.player_stats.attack += artifact.power
            print(f"Your attack increased by {artifact.power}.")

        self.artifacts.pop(artifact_name)

    def find_clue(self, new_clue: str) -> None:
        """Adds a unique clue to the player's clue set."""
        if new_clue not in self.clues:
            self.clues.add(new_clue)
            print(f"You discovered a new clue: {new_clue}")
        else:
            print("You already know this clue.")

    def handle_cryptic_library(self) -> None:
        """Handles the special Cryptic Library room."""
        print("A vast library filled with ancient, cryptic texts.")
        possible_clues = [
            "The treasure is hidden where the dragon sleeps.",
            "The key lies with the gnome.",
            "Beware the shadows.",
            "The amulet unlocks the final door."
        ]
        selected_clues = random.sample(possible_clues, 2)
        for clue in selected_clues:
            self.find_clue(clue)

        if "staff_of_wisdom" in self.inventory:
            print("Using the Staff of Wisdom, you understand the meaning of the clues.")
            print("You can bypass a puzzle challenge in another room.")

    def handle_challenge(self, room: Room) -> None:
        """Handles room challenges (puzzles and traps)."""
        if not room.challenge_outcome:
            return

        success = random.choice([True, False])
        outcome_message = room.challenge_outcome[0] if success else room.challenge_outcome[1]
        health_change = room.challenge_outcome[2]
        
        print(outcome_message)
        self.player_stats.health += health_change

    def enter_dungeon(self, dungeon_rooms: List[Tuple[str, Optional[str], str, Any]]) -> None:
        """Handles the player's interaction with dungeon rooms."""
        validated_rooms = self.validate_dungeon_rooms(dungeon_rooms)
        
        for room in validated_rooms:
            print(f"\nYou enter the {room.name}.")

            if room.name == "Cryptic Library":
                self.handle_cryptic_library()
            elif room.challenge_type in ["puzzle", "trap"]:
                self.handle_challenge(room)

            if room.item:
                self.inventory.append(room.item)
                print(f"You found a {room.item}!")

            print(f"Current Health: {self.player_stats.health}")
            print("---")

    def combat_encounter(self, monster_health: int, has_treasure: bool) -> Optional[str]:
        """Simulates a combat encounter between the player and a monster."""
        print("A monster attacks!")

        while self.player_stats.health > 0 and monster_health > 0:
            print(f"Player Health: {self.player_stats.health}, Monster Health: {monster_health}")
            monster_health -= self.player_stats.attack
            if monster_health > 0:
                self.player_stats.health -= 10

        if self.player_stats.health > 0:
            print("You defeated the monster!")
            return "treasure" if has_treasure else None
        else:
            print("You were defeated by the monster.")
            return None

    def display_status(self) -> None:
        """Displays the player's current status."""
        print(f"Player Health: {self.player_stats.health}, Player Attack: {self.player_stats.attack}")

    def display_game_end(self) -> None:
        """Displays the final game state."""
        print("\n--- Game End ---")
        self.display_status()
        print("Final Inventory:", self.inventory)
        print("Clues:")
        if self.clues:
            for clue in self.clues:
                print(f"- {clue}")
        else:
            print("No clues.")

# Function to match the test interface
def enter_dungeon(player_stats: Dict[str, int], inventory: List[str], 
                 dungeon_rooms: List[Tuple[str, Optional[str], str, Any]], 
                 clues: Set[str], artifacts: Dict[str, Any]) -> Tuple[Dict[str, int], List[str], Set[str]]:
    """
    Wrapper function to maintain compatibility with the test interface.
    """
    game = DungeonGame()
    game.player_stats = PlayerStats(**player_stats)
    game.inventory = inventory
    game.clues = clues
    game.artifacts = artifacts
    
    game.enter_dungeon(dungeon_rooms)
    
    return {'health': game.player_stats.health, 'attack': game.player_stats.attack}, game.inventory, game.clues

def main():
    game = DungeonGame()
    dungeon_rooms = [
        ("Dusty library", "key", "puzzle", ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]
    game.enter_dungeon(dungeon_rooms)

if __name__ == "__main__":
    main()