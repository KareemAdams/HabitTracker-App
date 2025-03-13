import os
import json
from typing import Dict, Optional
from habit_tracker import load_data, save_data, load_predefined_habits, view_all_habits


class UserConn:
    """
    A class to manage user connections, including registration and login functionalities.

    Methods:
    -------
    register_user(username: str, password: str) -> None
        Registers a new user with the given username and password.
    login_user(username: str, password: str) -> bool
        Logs in a user if the username and password are correct.
    user_exists(username: str) -> bool
        Check if user exists in the users.json file.
    save_user(username: str, password: str) -> None
        Save user credentials to the users.json file.
    load_users() -> None
        Load user login data from users.json file.
    logout() -> None
        Logs out the current user.
    load_predefined_habits() -> None
        Load predefined habits for the current user.
    """
    def __init__(self, users_file: str = None, data_directory: str = None) -> None:
        """
        Initializes the UserConn object and loads existing users from the specified file.

        Parameters:
        ----------
        users_file : str, optional
            The file path where user data is stored.
        data_directory : str, optional
            The directory where habit files will be stored.
        """
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.users_file = users_file or os.path.join(self.current_directory, "users.json")
        self.data_directory = data_directory or self.current_directory
        self.current_user: Optional[str] = None
        self.habits: Dict[str, Dict] = {}
        self.load_users()

    def register_user(self, username: str, password: str) -> None:
        """
        Registers a new user with the provided username and password.
        If the username already exists, it prompts the user to choose a different username.

        Parameters:
        ----------
        username : str
            The desired username for the new user.
        password : str
            The password for the new user.
        """        
        if not username or not username.strip():
            print("\033[1mUsername cannot be blank. Please provide a valid username.\033[0m")
            return
        if not password or not password.strip():
            print("\033[1mPassword cannot be blank. Please provide a valid password.\033[0m")
            return
    
        if self.user_exists(username):
            print("\033[1mUser already exists. Please choose a different username.\033[0m")
            return

        self.save_user_credentials(username, password)

        habits_file = os.path.join(self.data_directory, f"{username}_habits.json")
        with open(habits_file, 'w') as f:
            json.dump({}, f)

        print(f"User \033[1m'{username}'\033[0m registered successfully.\033[0m")

    def login_user(self, username: str, password: str) -> bool:
        """
        Logs in a user if the username exists and the provided password matches.
        If the login is successful, sets the current_user attribute to the username.

        Parameters:
        ----------
        username : str
            The username of the user attempting to log in.
        password : str
            The password associated with the username.

        Returns:
        -------
        bool
            True if the login is successful, False otherwise.
        """
        if not self.user_exists(username):
            print("\n\033[1mUser does not exist. Please register first.\033[0m\n")
            return False

        with open(self.users_file, 'r') as f:
            users = json.load(f)
            if users.get(username) == password:
                self.current_user = username
                habits_file = os.path.join(self.data_directory, f"{username}_habits.json")
                self.habits = load_data(habits_file)
                print(f"Welcome, \033[1m{username}!\033[0m")
                return True
            else:
                print("\033[1mIncorrect password.\033[0m")
                return False

    def user_exists(self, username: str) -> bool:
        """
        Check if a user exists in the JSON file.

        Args:
            username (str): The username to check for existence.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
                return username in users
        except FileNotFoundError:
            return False

    def save_user_credentials(self, username: str, password: str) -> None:
        """
        Save user credentials to the users file.

        Args:
            username (str): The username to save.
            password (str): The password to save.
        """
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {}

        users[username] = password

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)

    def load_users(self) -> None:
        """
        Load user login data from a JSON file.

        This method attempts to read user login data from a JSON file. If the file is not found,
        it initializes an empty user data store.
        """
        try:
            with open(self.users_file, 'r') as f:
                json.load(f)  # Check if the file is readable
        except FileNotFoundError:
            print("\n\033[1mNo saved user data found, starting fresh.\033[0m")

    def load_predefined_habits(self) -> None:
        """
        Load predefined habits for the current user.
        """
        if self.current_user:
            self.habits = load_predefined_habits(self.habits)
            habits_file = os.path.join(self.data_directory, f"{self.current_user}_habits.json")
            save_data(self.habits, habits_file)
            view_all_habits(self.habits)
        else:
            print("\n\033[1mPlease login to load predefined habits.\033[0m\n")

    def logout(self) -> None:
        """
        Log out the current user.

        This method logs out the currently logged-in user, if there is one. If no user 
        is logged in, it will inform the user.
        """
        if self.current_user:
            # Save habits before logging out
            habits_file = os.path.join(self.data_directory, f"{self.current_user}_habits.json")
            save_data(self.habits, habits_file)
            print(f"\nUser \033[1m'{self.current_user}'\033[0m logged out.\n")
            self.current_user = None
            self.habits = {}
        else:
            print("\n\033[1mNo user is currently logged in.\033[0m")
