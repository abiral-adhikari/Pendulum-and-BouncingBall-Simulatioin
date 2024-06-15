from pendulumsimulation import pendulumsimulation
from ballbouncing import ballbouncingsimulation
import pygame
def main_menu():
    pygame.init()
    while True:
        print("\nMain Menu:")
        print("1. Pendulum simulation")
        print("2. Ball bouncing simulation")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            pendulumsimulation()
        elif choice == '2':
            ballbouncingsimulation()
        elif choice == '3':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    while True:
        print("\nWelcome to the Simulation Program!")
        print("1. Start Simulation")
        print("2. Exit")
        start_choice = input("Enter your choice: ").strip()

        if start_choice == '1':
            main_menu()
        elif start_choice == '2':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
