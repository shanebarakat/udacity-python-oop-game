

import random
from typing import List, Tuple, Optional, Union

# Global instance of WorldMap. In a larger application, this might be passed as a dependency.
# For this scope, keeping it global as per original structure.
world: 'WorldMap'


class WorldMap:
    """
    Represents the game world map, managing its dimensions and occupied spaces.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initializes the WorldMap with specified width and height.

        Args:
            width: The width of the map.
            height: The height of the map.

        Raises:
            ValueError: If width or height are not positive integers.
        """
        if not isinstance(width, int) or width <= 0:
            raise ValueError("Map width must be a positive integer.")
        if not isinstance(height, int) or height <= 0:
            raise ValueError("Map height must be a positive integer.")

        self.width: int = width
        self.height: int = height
        # Line 8: Keeping as list comprehension for 2D list initialization.
        # A generator expression would yield a generator of generators, not a 2D list,
        # which is required for direct indexing (e.g., self.map[x][y]).
        self.map: List[List[Optional['Entity']]] = [[None for _ in range(self.width)] for _ in range(self.height)]

    def is_occupied(self, x: int, y: int) -> bool:
        """
        Checks if a given space on the map is occupied.

        Args:
            x: The x-coordinate to check.
            y: The y-coordinate to check.

        Returns:
            True if the space is occupied or out of bounds, False otherwise.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            # Coordinates are out of bounds, treat as occupied to prevent placement.
            return True
        try:
            return self.map[x][y] is not None
        except IndexError:
            # This should ideally not happen if the bounds check above is correct,
            # but added as a safeguard against unexpected state.
            return True


# Initialize the global world map after WorldMap class is defined.
world = WorldMap(100, 100)


class Entity:
    """
    Base class for all entities in the game world.
    Manages position and interaction with the WorldMap.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes an Entity at a specified position.

        Args:
            x: The initial x-coordinate of the entity.
            y: The initial y-coordinate of the entity.

        Raises:
            ValueError: If the initial position is invalid or occupied.
        """
        self.x: int = -1  # Initialize to invalid coordinates
        self.y: int = -1

        if not self._is_valid_position(x, y):
            print(f"Warning: Initial position ({x}, {y}) is out of map bounds. Entity not placed.")
            return

        if world.is_occupied(x, y):
            print(f"Warning: Position ({x}, {y}) is already occupied. Entity not placed.")
            return
        else:
            self.set_position(x, y)

    def _is_valid_position(self, x: int, y: int) -> bool:
        """
        Helper to check if coordinates are within world map bounds.
        """
        return 0 <= x < world.width and 0 <= y < world.height

    def set_position(self, x: int, y: int) -> None:
        """
        Sets the entity's position on the map.

        Args:
            x: The new x-coordinate.
            y: The new y-coordinate.

        Raises:
            ValueError: If coordinates are out of map bounds.
            IndexError: If an unexpected index error occurs during map assignment.
        """
        if not self._is_valid_position(x, y):
            print(f"Warning: Cannot set position to ({x}, {y}): out of map bounds. Position not changed.")
            return

        try:
            self.x = x
            self.y = y
            world.map[x][y] = self
        except IndexError as e:
            # This should be caught by _is_valid_position, but added as a safeguard.
            print(f"Warning: Error setting position at ({x}, {y}): {e}. Position not changed.")
            return

    def remove(self) -> None:
        """
        Removes the entity from its current position on the map.
        """
        if not self._is_valid_position(self.x, self.y):
            # Entity is already in an invalid or removed state.
            return

        try:
            world.map[self.x][self.y] = None
            self.x = -1  # Mark as removed/invalid position
            self.y = -1
        except IndexError as e:
            # This should not happen if entity's position is valid, but for robustness.
            raise IndexError(f"Error removing entity from ({self.x}, {self.y}): {e}")

    def distance(self, other: 'Entity') -> Tuple[int, int]:
        """
        Calculates the absolute distance between this entity and another.

        Args:
            other: The other entity to calculate distance to.

        Returns:
            A tuple containing the absolute difference in x and y coordinates.
        """
        return abs(other.x - self.x), abs(other.y - self.y)


class Character(Entity):
    """
    Represents a character in the game, inheriting from Entity.
    Includes health, items, protection, and combat capabilities.
    """

    def __init__(self, x: int, y: int, hit_points: int) -> None:
        """
        Initializes a Character.

        Args:
            x: The initial x-coordinate.
            y: The initial y-coordinate.
            hit_points: The character's initial health points.

        Raises:
            ValueError: If hit_points is not a non-negative integer.
        """
        super().__init__(x, y)
        if not isinstance(hit_points, int) or hit_points < 0:
            raise ValueError("Hit points must be a non-negative integer.")
        self.hit_points: int = hit_points
        self.items: List[str] = []  # Example: list of item names
        self.protection: int = 0

    def _get_move_delta(self, direction: str) -> Tuple[int, int]:
        """
        Helper method to get the x, y delta for a given direction.

        Args:
            direction: The direction string ('left', 'right', 'up', 'down').

        Returns:
            A tuple (dx, dy) representing the change in coordinates.

        Raises:
            ValueError: If an invalid direction is provided.
        """
        direction_map = {
            'left': (-1, 0),
            'right': (1, 0),
            'up': (0, 1),
            'down': (0, -1)
        }
        delta = direction_map.get(direction.lower())
        if delta is None:
            raise ValueError(
                "Invalid direction. Please use 'left', 'right', 'up', or 'down'."
            )
        return delta

    def move(self, direction: str) -> None:
        """
        Moves the character one space in a given direction.
        Allows wrapping of the world map.

        Args:
            direction: The direction to move ('left', 'right', 'up', or 'down').
        """
        try:
            dx, dy = self._get_move_delta(direction)
        except ValueError as e:
            print(f"Move failed: {e}")
            return

        new_x: int = (self.x + dx) % world.width
        new_y: int = (self.y + dy) % world.height

        if world.is_occupied(new_x, new_y):
            print(f"Position ({new_x}, {new_y}) is occupied, try another move.")
        else:
            self.remove()  # Remove from current position
            self.set_position(new_x, new_y)  # Set to new position
            self._on_move_complete()  # Call hook for subclasses

    def _on_move_complete(self) -> None:
        """
        Hook method called after a successful move.
        Can be overridden by subclasses for specific post-move logic.
        """
        pass  # Default: do nothing

    def _deal_damage(self, target: 'Character', base_damage: int) -> None:
        """
        Helper method to apply damage to a target, considering protection.

        Args:
            target: The character to deal damage to.
            base_damage: The base amount of damage to deal.
        """
        if not self.can_attack(target):
            print(f"{self.__class__.__name__} cannot attack {target.__class__.__name__} at this range.")
            return

        if not target.has_protection():
            target.lose_health(base_damage)
            print(f"{self.__class__.__name__} dealt {base_damage} damage to {target.__class__.__name__}.")
        else:
            target.lose_protection(base_damage)
            print(f"{self.__class__.__name__} dealt {base_damage} damage to {target.__class__.__name__}'s protection.")

    def attack(self, enemy: 'Character') -> None:
        """
        Performs a standard attack on an enemy.

        Args:
            enemy: The target character to attack.
        """
        self._deal_damage(enemy, 10)

    def power_attack(self, enemy: 'Character') -> None:
        """
        Performs a powerful attack on an enemy.

        Args:
            enemy: The target character to attack.
        """
        self._deal_damage(enemy, 20)

    def can_attack(self, enemy: 'Character') -> bool:
        """
        Checks if this character can attack a given enemy based on proximity.

        Args:
            enemy: The target character.

        Returns:
            True if the enemy is within attack range, False otherwise.
        """
        enemy_dx, enemy_dy = self.distance(enemy)
        return enemy_dx == 1 and enemy_dy == 0

    def gain_health(self, amount: int = 10) -> None:
        """
        Increases the character's health points.

        Args:
            amount: The amount of health to gain. Defaults to 10.

        Raises:
            ValueError: If amount is not a non-negative integer.
        """
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("Health gain amount must be a non-negative integer.")
        self.hit_points += amount
        print(f"{self.__class__.__name__} gained {amount} health. Current HP: {self.hit_points}")

    def lose_health(self, reduction: int) -> None:
        """
        Decreases the character's health points, ensuring it doesn't go below zero.
        If health drops to 0, the character is removed from the map.

        Args:
            reduction: The amount of health to lose.

        Raises:
            ValueError: If reduction is not a non-negative integer.
        """
        if not isinstance(reduction, int) or reduction < 0:
            raise ValueError("Health reduction amount must be a non-negative integer.")
        self.hit_points = max(self.hit_points - reduction, 0)
        print(f"{self.__class__.__name__} lost {reduction} health. Current HP: {self.hit_points}")
        if self.hit_points == 0:
            print(f"{self.__class__.__name__} has been defeated!")
            self.remove()  # Automatically remove defeated character from map

    def gain_protection(self, amount: int = 4) -> None:
        """
        Increases the character's protection points.

        Args:
            amount: The amount of protection to gain. Defaults to 4.

        Raises:
            ValueError: If amount is not a non-negative integer.
        """
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("Protection gain amount must be a non-negative integer.")
        self.protection += amount
        print(f"{self.__class__.__name__} gained {amount} protection. Current protection: {self.protection}")

    def lose_protection(self, reduction: int) -> None:
        """
        Decreases the character's protection points, ensuring it doesn't go below zero.

        Args:
            reduction: The amount of protection to lose.

        Raises:
            ValueError: If reduction is not a non-negative integer.
        """
        if not isinstance(reduction, int) or reduction < 0:
            raise ValueError("Protection reduction amount must be a non-negative integer.")
        self.protection = max(self.protection - reduction, 0)
        print(f"{self.__class__.__name__} lost {reduction} protection. Current protection: {self.protection}")

    def has_protection(self) -> bool:
        """
        Checks if the character currently has any protection.

        Returns:
            True if protection is greater than 0, False otherwise.
        """
        return self.protection > 0


class Enemy(Character):
    """
    Represents an enemy character in the game.
    """

    def __init__(self, x: int, y: int, hit_points: int) -> None:
        """
        Initializes an Enemy.

        Args:
            x: The initial x-coordinate.
            y: The initial y-coordinate.
            hit_points: The enemy's initial health points.
        """
        super().__init__(x, y, hit_points)

    def challenge(self, other: 'Character') -> None:
        """
        Initiates a challenge interaction with another character.

        Args:
            other: The character to challenge.
        """
        print(f"{self.__class__.__name__} challenges {other.__class__.__name__}: Let's fight!")


class Wizard(Character):
    """
    Represents a Wizard character, capable of casting spells and healing.
    """

    def __init__(self, x: int, y: int, hit_points: int, mana: int) -> None:
        """
        Initializes a Wizard.

        Args:
            x: The initial x-coordinate.
            y: The initial y-coordinate.
            hit_points: The wizard's initial health points.
            mana: The wizard's initial mana points.

        Raises:
            ValueError: If mana is not a non-negative integer.
        """
        super().__init__(x, y, hit_points)
        if not isinstance(mana, int) or mana < 0:
            raise ValueError("Mana must be a non-negative integer.")
        self.mana: int = mana

    def cast_spell(self, enemy: 'Character') -> None:
        """
        Casts a spell on an enemy, consuming mana and dealing multiple attacks.
        The number of attacks is determined by a pseudo-random generator.

        Args:
            enemy: The target character for the spell.
        """
        if self.mana < 5:
            print(f"{self.__class__.__name__} does not have enough mana to cast a spell (requires 5 mana).")
            return

        if not self.can_attack(enemy):
            print(f"{self.__class__.__name__} cannot cast spell on {enemy.__class__.__name__} at this range.")
            return

        self.mana -= 5
        print(f"{self.__class__.__name__} casts a spell! Mana remaining: {self.mana}")

        num_attacks: int = random.randint(1, 5)
        for _ in range(num_attacks):
            self.attack(enemy)  # Use the inherited attack method

    def heal(self, target_char: 'Character') -> None:
        """
        Heals a target character, consuming mana.

        Args:
            target_char: The character to heal.
        """
        if self.mana < 5:
            print(f"{self.__class__.__name__} does not have enough mana to heal (requires 5 mana).")
            return

        self.mana -= 5
        target_char.gain_health(15)
        print(f"{self.__class__.__name__} healed {target_char.__class__.__name__}. Mana remaining: {self.mana}")

    def _on_move_complete(self) -> None:
        """
        Overrides the Character's hook to regenerate mana after moving.
        """
        self.mana += 1
        print(f"{self.__class__.__name__} regenerated 1 mana after moving. Current mana: {self.mana}")


class Archer(Character):
    """
    Represents an Archer character, capable of ranged attacks.
    """

    def __init__(self, x: int, y: int, hit_points: int) -> None:
        """
        Initializes an Archer.

        Args:
            x: The initial x-coordinate.
            y: The initial y-coordinate.
            hit_points: The archer's initial health points.
        """
        super().__init__(x, y, hit_points)

    def range_attack(self, enemy: 'Character') -> None:
        """
        Performs a ranged attack on an enemy.

        Args:
            enemy: The target character for the ranged attack.
        """
        enemy_dx, enemy_dy = self.distance(enemy)
        if enemy_dx <= 5 and enemy_dy == 0:
            self._deal_damage(enemy, 5)  # Use the common damage dealing helper
        else:
            print(f"{self.__class__.__name__} cannot range attack {enemy.__class__.__name__} at this range.")


if __name__ == "__main__":
    # Line 147: Replace string concatenation with str.join()
    print("".join(["testing: ", __file__]))

    try:
        alice = Character(10, 10, 100)
        bob = Character(11, 10, 100)
        clare = Wizard(15, 10, 60, 50)
        dan = Archer(6, 10, 30)

        character_list: List[Character] = [alice, bob, clare, dan]

        # Loop at original line 128: Already uses direct iteration, which is Pythonic and efficient.
        # No change needed as it's already optimized for this use case.
        for character in character_list:
            print(character.__dict__)

        print("\n--- Testing Interactions ---")
        print(f"Alice HP: {alice.hit_points}, Bob HP: {bob.hit_points}")
        alice.attack(bob)
        print(f"Alice HP: {alice.hit_points}, Bob HP: {bob.hit_points}")

        print(f"\nClare Mana: {clare.mana}, Bob HP: {bob.hit_points}")
        clare.cast_spell(bob)
        print(f"Clare Mana: {clare.mana}, Bob HP: {bob.hit_points}")

        print(f"\nDan HP: {dan.hit_points}, Alice HP: {alice.hit_points}")
        dan.range_attack(alice)  # Should not hit, range is too far (10-6=4, but y is same)
        print(f"Dan HP: {dan.hit_points}, Alice HP: {alice.hit_points}")

        # Move Dan closer to Alice for range attack
        print("\n--- Moving Dan closer ---")
        dan.move('right')  # Dan moves from (6,10) to (7,10)
        dan.move('right')  # Dan moves from (7,10) to (8,10)
        dan.move('right')  # Dan moves from (8,10) to (9,10)
        print(f"Dan's new position: ({dan.x}, {dan.y})")
        dan.range_attack(alice)  # Should hit now (distance 1)
        print(f"Dan HP: {dan.hit_points}, Alice HP: {alice.hit_points}")

        print("\n--- Testing Protection ---")
        bob.gain_protection()
        print(f"Bob has protection: {bob.has_protection()}, Protection: {bob.protection}")
        alice.power_attack(bob)  # Should hit protection first
        print(f"Bob has protection: {bob.has_protection()}, Protection: {bob.protection}, HP: {bob.hit_points}")

        print("\n--- Testing Wizard Mana Regen on Move ---")
        print(f"Clare's initial mana: {clare.mana}")
        clare.move('up')  # Clare moves from (15,10) to (15,11)
        print(f"Clare's mana after move: {clare.mana}")

        print("\n--- Testing Healing ---")
        print(f"Alice HP before heal: {alice.hit_points}")
        clare.heal(alice)
        print(f"Alice HP after heal: {alice.hit_points}")

        print("\n--- Testing Invalid Operations (Error Handling) ---")
        try:
            # Attempt to create a character at an occupied position
            invalid_char_pos = Character(10, 10, 50)
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            # Attempt to create a character out of map bounds
            invalid_char_bounds = Character(1000, 10, 50)
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            # Attempt to move with an invalid direction
            alice.move('sideways')
        except ValueError as e:
            print(f"Caught expected error: {e}")

    except ValueError as e:
        print(f"An unexpected error occurred during initialization or interaction: {e}")
    except IndexError as e:
        print(f"An unexpected map access error occurred: {e}")

