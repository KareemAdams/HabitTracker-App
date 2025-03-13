from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
import os
from habit import Habit


def load_predefined_habits(habits: Dict[str, Habit]) -> Dict[str, Habit]:
    """
    Loads a set of predefined habits with example tracking data.

    Args:
        habits (Dict[str, Habit]): The current dictionary of habits.

    Returns:
        Dict[str, Habit]: Updated dictionary of habits with predefined habits added.
    """
    predefined_habits = [
        {"name": "Exercise", "periodicity": "daily"},
        {"name": "Shopping", "periodicity": "weekly"},
        {"name": "Meditate", "periodicity": "daily"},
        {"name": "Reading", "periodicity": "daily"},
        {"name": "Cleaning", "periodicity": "weekly"}
    ]

    today = datetime.now()

    for habit_data in predefined_habits:
        name = habit_data["name"]
        periodicity = habit_data["periodicity"]

        if name not in habits:
            habits[name] = Habit(name, periodicity)

        for week in range(4):
            if periodicity == "daily":
                for day in range(7):
                    completion_date = today - timedelta(days=(week * 7 + day))
                    habits[name].checkoffs.append(completion_date)
            elif periodicity == "weekly":
                completion_date = today - timedelta(weeks=week)
                habits[name].checkoffs.append(completion_date)

        habits[name].update_streak()

    print("Predefined habits with example tracking data loaded successfully.")
    return habits

def add_habit(habits: Dict[str, Habit], name: str, periodicity: str, data_file: str) -> Dict[str, Habit]:
    """
    Add a new habit with the specified name and periodicity.

    Args:
        habits (Dict[str, Habit]): The current dictionary of habits.
        name (str): The name of the new habit.
        periodicity (str): The frequency of the habit ('daily' or 'weekly').
        data_file (str): The file path for saving the data.

    Returns:
        Dict[str, Habit]: Updated dictionary of habits with the new habit added.
    """
    if periodicity not in ['daily', 'weekly']:
        print("Invalid periodicity. Please use 'daily' or 'weekly'.")
        return habits
    if name in habits:
        print(f"Habit \033[1m'{name}'\033[0m already exists.")
        return habits

    habits[name] = Habit(name, periodicity)
    save_data(habits, data_file)
    print(f"Added habit: \033[1m{name}\033[0m with periodicity: \033[1m{periodicity}\033[0m.")
    return habits

def delete_habit(habits: Dict[str, Habit], name: str, data_file: str) -> Dict[str, Habit]:
    """
    Delete a habit by its name.

    Args:
        habits (Dict[str, Habit]): The current dictionary of habits.
        name (str): The name of the habit to delete.
        data_file (str): The file path for saving the data.

    Returns:
        Dict[str, Habit]: Updated dictionary of habits with the habit removed.
    """
    if name in habits:
        del habits[name]
        save_data(habits, data_file)
        print(f"Habit \033[1m'{name}'\033[0m has been deleted.")
    else:
        print(f"Habit \033[1m'{name}'\033[0m not found.")
    return habits

def check_off_habit(habits: Dict[str, Habit], name: str, data_file: str) -> Dict[str, Habit]:
    """
    Mark the specified habit as completed for today.

    Args:
        habits (Dict[str, Habit]): The current dictionary of habits.
        name (str): The name of the habit to check off.
        data_file (str): The file path for saving the data.

    Returns:
        Dict[str, Habit]: Updated dictionary of habits with the habit checked off.
    """
    habit = habits.get(name)
    if habit:
        habit.check_off()
        save_data(habits, data_file)
    else:
        print(f"Habit \033[1m'{name}'\033[0m not found.")
    return habits

def longest_streak(habits: Dict[str, Habit]) -> List[Habit]:
    """
    Identify all habits with the longest streak.

    Args:
        habits (Dict[str, Habit]): The current dictionary of habits.

    Returns:
        List[Habit]: A list of habits with the longest current streak.
    """
    if not habits:
        print("No habits to analyze.")
        return []

    # Find the maximum streak value
    max_streak = max(habit.streak for habit in habits.values())

    # Find all habits with the maximum streak
    longest_habits = [habit for habit in habits.values() if habit.streak == max_streak]

    if longest_habits:
        print(f"\nLongest streak: \033[1m{max_streak}\033[0m periods.")
        habit_names = ", ".join([habit.name for habit in longest_habits])
        print(f"\nHabits with the longest streak: \033[1m{habit_names}\033[0m")
    else:
        print("\n\033[1mNo streaks found.\033[0m")

    return longest_habits

def current_daily_habits(habits: Dict[str, Habit]) -> List[str]:
    """
    List all habits that have a 'daily' periodicity.

    Args:
        habits (Dict[str, Habit]): The current dictionary of habits.

    Returns:
        List[str]: A list of names of daily habits.
    """
    daily_habits = [habit.name for habit in habits.values() if habit.periodicity == 'daily']
    if daily_habits:
        print(f"\nCurrent daily habits: \033[1m{', '.join(daily_habits)}\033[0m\n")
    else:
        print("No daily habits found.")
    return daily_habits

def current_weekly_habits(habits: Dict[str, Habit]) -> List[str]:
    """
    List all habits that have a 'weekly' periodicity.

    Args:
        habits (Dict[str, Habit]): The current dictionary of habits.

    Returns:
        List[str]: A list of names of weekly habits.
    """
    weekly_habits = [habit.name for habit in habits.values() if habit.periodicity == 'weekly']
    if weekly_habits:
        print(f"\nCurrent weekly habits: \033[1m{', '.join(weekly_habits)}\033[0m\n")
    else:
        print("No weekly habits found.")
    return weekly_habits

def struggled_habits_last_month(habits: Dict[str, Habit]) -> List[str]:
    """
    Identify habits that were missed in the last 30 days, using the `is_broken` method.

    Args:
        habits (Dict[str, Habit]): The current dictionary of habits.

    Returns:
        List[str]: A list of habit names that were missed during the last month.
    """
    now = datetime.now()
    last_month = now - timedelta(days=30)
    struggled = []

    for habit in habits.values():
        # Skip if the habit was created after the last 30 days
        if habit.created_at > now:
            continue

        # Check if the habit is broken (missed checkoffs)
        if habit.is_broken():
            # Ensure the habit was active in the last 30 days
            if habit.created_at <= now and any(check >= last_month for check in habit.checkoffs):
                struggled.append(habit.name)

    if struggled:
        print(f"\nHabits struggled with last month: \033[1m{', '.join(struggled)}\033[0m\n")
    else:
        print("\n\033[1mNo struggled habits found last month!\033[0m\n")

    return struggled


def view_all_habits(habits: Dict[str, Habit]) -> None:
    """
    Display all the defined habits with their details.

    Args:
        habits (Dict[str, Habit]): The current dictionary of habits.
    """
    if not habits:
        print("No habits defined yet.")
        return
    
    print("\nAll Habits:")
    for habit in habits.values():
        last_checked = max(habit.checkoffs) if habit.checkoffs else "Never"
        if last_checked != "Never":
            last_checked = last_checked.strftime("%Y-%m-%d %H:%M:%S")
        print(
            f" - \033[1m{habit.name}\033[0m ({habit.periodicity}), "
            f"\033[1mStreak\033[0m: {habit.streak}, "
            f"\033[1mLast Checked Off\033[0m: {last_checked}, "
            f"\033[1mCreated At\033[0m: {habit.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )

def save_data(habits: Dict[str, Habit], data_file: str) -> None:
    """
    Save all habit data to a JSON file.

    Args:
        habits (Dict[str, Habit]): The dictionary of habits to save.
        data_file (str): The file path for saving the data.
    """
    data = {
        name: {
            'name': habit.name,
            'periodicity': habit.periodicity,
            'created_at': habit.created_at.isoformat(),
            'checkoffs': [check.isoformat() for check in habit.checkoffs],
            'streak': habit.streak
        } for name, habit in habits.items()
    }
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)
    print("\nData saved successfully.")

def load_data(data_file: str) -> Dict[str, Habit]:
    """
    Load habit data from a JSON file if it exists, or initialize a new tracker.

    Args:
        data_file (str): The file path for loading the data.

    Returns:
        Dict[str, Habit]: A dictionary of habits loaded from the file or an empty dictionary.
    """
    habits: Dict[str, Habit] = {}
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
                for habit_data in data.values():
                    habit = Habit(
                        name=habit_data['name'],
                        periodicity=habit_data['periodicity'],
                        created_at=datetime.fromisoformat(habit_data['created_at']),
                        checkoffs=[datetime.fromisoformat(date) for date in habit_data['checkoffs']],
                        streak=habit_data['streak']
                    )
                    habits[habit.name] = habit
            print("\n\033[1mData loaded successfully.\033[0m\n")
        except json.JSONDecodeError:
            print("\n\033[1mError loading data.\033[0m\n")
    return habits