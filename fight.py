

from typing import List
import logging

# Import necessary classes from new modules
from character_models import Character, Wizard, Archer

# Configure logging for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_simulation():
    """
    Executes a comprehensive simulation demonstrating character interactions,
    movement, spell casting, and robust error handling.

    This function initializes various character types (Character, Wizard, Archer),
    performs a sequence of actions such as attacks, spell casts, and movements,
    and showcases the protection and mana regeneration mechanics. It also
    includes tests for expected error conditions, logging all significant events
    and errors.
    """
    logging.info("Starting character simulation.")
    try:
        # Character Initialization
        logging.info("Initializing characters...")
        alice = Character(10, 10, 100)
        bob = Character(11, 10, 100)
        clare = Wizard(15, 10, 60, 50)
        dan = Archer(6, 10, 30)
        logging.info("Characters initialized successfully.")

        character_list: List[Character] = [alice, bob, clare, dan]

        for character in character_list:
            logging.info(f"Character created: {character.__dict__}")

        # --- Testing Basic Interactions ---
        logging.info("\n--- Testing Basic Interactions ---")
        logging.info(f"Alice HP: {alice.hit_points}, Bob HP: {bob.hit_points}")
        alice.attack(bob)
        logging.info(f"Alice attacked Bob. Alice HP: {alice.hit_points}, Bob HP: {bob.hit_points}")

        # --- Testing Wizard Spell Cast ---
        logging.info(f"\nClare Mana: {clare.mana}, Bob HP: {bob.hit_points}")
        clare.cast_spell(bob)
        logging.info(f"Clare cast spell on Bob. Clare Mana: {clare.mana}, Bob HP: {bob.hit_points}")

        # --- Testing Archer Range Attack ---
        logging.info(f"\nDan HP: {dan.hit_points}, Alice HP: {alice.hit_points}")
        dan.range_attack(alice)
        logging.info(f"Dan range attacked Alice. Dan HP: {dan.hit_points}, Alice HP: {alice.hit_points}")

        # --- Moving Dan closer and re-attacking ---
        logging.info("\n--- Moving Dan closer ---")
        dan.move('right')
        dan.move('right')
        dan.move('right')
        logging.info(f"Dan's new position: ({dan.x}, {dan.y})")
        dan.range_attack(alice)
        logging.info(f"Dan range attacked Alice again. Dan HP: {dan.hit_points}, Alice HP: {alice.hit_points}")

        # --- Testing Protection Mechanism ---
        logging.info("\n--- Testing Protection ---")
        bob.gain_protection()
        logging.info(f"Bob has protection: {bob.has_protection()}, Protection: {bob.protection}")
        alice.power_attack(bob)
        logging.info(f"Alice power attacked Bob. Bob has protection: {bob.has_protection()}, Protection: {bob.protection}, HP: {bob.hit_points}")

        # --- Testing Wizard Mana Regeneration on Move ---
        logging.info("\n--- Testing Wizard Mana Regen on Move ---")
        logging.info(f"Clare's initial mana: {clare.mana}")
        clare.move('up')
        logging.info(f"Clare's mana after move: {clare.mana}")

        # --- Testing Healing Spell ---
        logging.info("\n--- Testing Healing ---")
        logging.info(f"Alice HP before heal: {alice.hit_points}")
        clare.heal(alice)
        logging.info(f"Alice HP after heal: {alice.hit_points}")

        # --- Testing Invalid Operations (Error Handling) ---
        logging.info("\n--- Testing Invalid Operations (Error Handling) ---")
        try:
            # Attempt to create a character at an occupied position
            logging.info("Attempting to create character at an occupied position (expecting ValueError)...")
            invalid_char_pos = Character(10, 10, 50)
        except ValueError as e:
            logging.warning(f"Caught expected ValueError: {e}")

        try:
            # Attempt to create a character out of map bounds
            logging.info("Attempting to create character out of map bounds (expecting ValueError)...")
            invalid_char_bounds = Character(1000, 10, 50)
        except ValueError as e:
            logging.warning(f"Caught expected ValueError: {e}")

        try:
            # Attempt to move with an invalid direction
            logging.info("Attempting to move with an invalid direction (expecting ValueError)...")
            alice.move('sideways')
        except ValueError as e:
            logging.warning(f"Caught expected ValueError: {e}")

    except ValueError as e:
        # Catch specific ValueErrors that might occur during the simulation flow
        logging.error(f"A critical ValueError occurred during simulation: {e}", exc_info=True)
    except IndexError as e:
        # Catch specific IndexErrors, typically related to map boundary issues
        logging.error(f"A critical IndexError occurred during simulation (map access error): {e}", exc_info=True)
    except Exception as e:
        # Catch any other unexpected exceptions to prevent silent failures
        logging.critical(f"An unhandled critical error occurred during simulation: {e}", exc_info=True)

    logging.info("Simulation finished.")


if __name__ == "__main__":
    # Original print statement, kept for consistency with the initial script behavior
    print("".join(["testing: ", __file__]))
    # Call the refactored main simulation function
    run_simulation()
