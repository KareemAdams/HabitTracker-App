import os
from user_conn import UserConn
from habit_tracker import (
    add_habit,
    delete_habit,
    check_off_habit,
    longest_streak,
    current_daily_habits,
    current_weekly_habits,
    struggled_habits_last_month,
    view_all_habits,
)


def main():
    """
    The main function to run the Habit Tracker command-line interface.

    This function initializes a HabitTracker instance and provides a menu-driven interface
    for users to interact with the application. Users can perform the following actions:
    - Register a new account
    - Login to an existing account
    - Load predefined habits for quick setup
    - Add new custom habits
    - Mark habits as completed
    - View statistics such as longest habit streaks, current daily and weekly habits, and
      habits that were missed or struggled with in the last month
    - Delete habits from their list
    - Logout from the current session

    The interface continues to run until the user chooses to exit by pressing 'q'.
    """
        
    # Get the directory where main.py is located
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Initialize UserConn with the directory
    tracker = UserConn(data_directory=current_directory)

    while True:
        print("\033[1m+-------------------+\033[0m")
        print("\033[1m| HabitTracker Menu |\033[0m")
        print("\033[1m+-------------------+\033[0m")
        print("1. Register User")
        print("2. Login")
        print("3. Load 5 Predefined Habits")
        print("4. Add New Habit")
        print("5. Check Off Habit")
        print("6. View Longest Streak")
        print("7. View Daily Habits")
        print("8. View Weekly Habits")
        print("9. View Struggled Habits Last Month")
        print("10. View All Habits")
        print("11. Delete Habit")
        print("12. Logout")
        print("Press \033[1m'q'\033[0m to exit")

        choice = input("\n\033[1mChoose an option:\033[0m ")

        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            tracker.register_user(username, password)

        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            tracker.login_user(username, password)

        elif choice == '3':
            tracker.load_predefined_habits()

        elif choice == '4':
            if tracker.current_user:
                name = input("Enter habit name: ")
                periodicity = input("Enter periodicity ('daily' or 'weekly'): ")
                habits_file = os.path.join(current_directory, f"{tracker.current_user}_habits.json")
                tracker.habits = add_habit(tracker.habits, name, periodicity, habits_file)
            else:
                print("\n\033[1mPlease login to add a habit.\033[0m\n")

        elif choice == '5':
            if tracker.current_user:
                view_all_habits(tracker.habits)
                name = input("\nEnter habit name to check off: ")
                habits_file = os.path.join(current_directory, f"{tracker.current_user}_habits.json")
                tracker.habits = check_off_habit(tracker.habits, name, habits_file)
            else:
                print("\n\033[1mPlease login to check off a habit.\033[0m\n")

        elif choice == '6':
            if tracker.current_user:
                longest_streak(tracker.habits)
            else:
                print("\n\033[1mPlease login to check your longest streak.\033[0m\n")

        elif choice == '7':
            if tracker.current_user:
                current_daily_habits(tracker.habits)
            else:
                print("\n\033[1mPlease login to check your daily habits.\033[0m\n")

        elif choice == '8':
            if tracker.current_user:
                current_weekly_habits(tracker.habits)
            else:
                print("\n\033[1mPlease login to check your weekly habits.\033[0m\n")

        elif choice == '9':
            if tracker.current_user:
                struggled_habits_last_month(tracker.habits)
            else:
                print("\n\033[1mPlease login to check your struggled habits.\033[0m\n")

        elif choice == '10':
            if tracker.current_user:
                view_all_habits(tracker.habits)
            else:
                print("\n\033[1mPlease login to view all your habits.\033[0m\n")

        elif choice == '11':
            if tracker.current_user:
                name = input("Enter habit name to delete: ")
                habits_file = os.path.join(current_directory, f"{tracker.current_user}_habits.json")
                tracker.habits = delete_habit(tracker.habits, name, habits_file)
            else:
                print("\n\033[1mPlease login to delete a habit.\033[0m\n")

        elif choice == '12':
            tracker.logout()

        elif choice == 'q':
            print("\n\033[1mExiting HabitTracker ... Goodbye!\033[0m\n")
            break

        else:
            print("\n\033[1mInvalid choice. Try again.\033[0m\n")


if __name__ == "__main__":
    main()