import time
import threading

user_steps = 0
bunny_steps = 0
race_length = 50
game_over = False
lock = threading.Lock()

def get_bunny_speed():
    print("Choose bunny difficulty:")
    print("1 - Easy (slow bunny)")
    print("2 - Medium (normal bunny)")
    print("3 - Hard (fast bunny)")
    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice == "1":
            return 1.0
        elif choice == "2":
            return 0.5
        elif choice == "3":
            return 0.25
        else:
            print("Invalid choice. Try again.")

def bunny_runner(bunny_speed):
    global bunny_steps, game_over
    while not game_over and bunny_steps < race_length:
        time.sleep(bunny_speed)
        with lock:  # lock the thread, can't allow both thread to update the same global variable
            bunny_steps += 1
            print(f"Bunny at {bunny_steps} steps")
            if bunny_steps >= race_length:
                game_over = True
                print("Bunny wins the race, you loose, try next time please!")

def user_runner():
    global user_steps, game_over
    last_input = None
    print("\n Start running! Press 1 and 2 alternately (like left and right foot)!\n")

    while not game_over and user_steps < race_length:
        user_input = input("Your move (1 or 2): ").strip()
        with lock: # lock the thread, can't allow both thread to update the same global variable
            if user_input =="1" or user_input=="2":
                if user_input != last_input:
                    user_steps += 1
                    last_input = user_input
                    print(f" You are at {user_steps} steps")
                else:
                    print(" Same foot twice! Keep alternating!")
            else:
                print(" Invalid input. Press only 1 or 2.")

            if user_steps >= race_length:
                game_over = True
                print(" You are faster than the bunny, good job!")

def reset_game_state():
    global user_steps, bunny_steps, game_over
    user_steps = 0
    bunny_steps = 0
    game_over = False

def main():
    reset_game_state()
    
    bunny_speed = get_bunny_speed() # get the bunny speed, it is the input from user
    bunny_thread = threading.Thread(target=bunny_runner, args=(bunny_speed,))
    bunny_thread.start() # bunny thread runs in the background
    user_runner() # user thread runs in the main function
    bunny_thread.join() # wait until bunny thread to finish to finish up the game


if __name__ == "__main__":
    main()
