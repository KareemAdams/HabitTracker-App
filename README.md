# Habit Tracker App

A simple and intuitive **Habit Tracker App** designed to help users build and maintain healthy habits. Track your progress, stay motivated, and achieve your goals!


## 🌟 Features

- **Daily Habit Tracking**: monitor habits with an easy-to-use interface.
- **Custom Habit Creation**: create and personalize habits to suit your lifestyle.
- **Preloaded Habit Creation**: preloads mixtures of daily and weekly habits with 1 month data.
- **Progress Visualization**: view streaks and progress through charts.
- **View Habit Analytics**: get timely reminders to stay on track.
- **JSON**: stores data using JSON file for simplicity, ensuring persistence across sessions.
- **Command Line Interface**: for intuitive interaction and management of habits and tasks.


## 🚀 Tech Stack

- **Frontend**: [Python](https://python.org), (requires version 3.8 and above)
- **Database**: [JSON](https://www.json.oorg)  
- **Test Unit**: [unittest](https://docs.python.org/3.11/library/unittest.html)  
- **Visualization Tools**: [Matplotlib](https://matplotlib.org), (requires version 3.7 and above)


## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KareemAdams/HabitTracker-App.git

2.	Navigate to the project directory:
    cd habit-tracker-app

3.	Install dependencies:

    - install Matplotlib
        pip install matplotlib
    
    - install Python unittest
        pip install unittest

4.	Start HabitTracker app:
    python main.py


## 📈 How It Works

1.	**Register User:** Create a new user with username and password.
2.	**Login:** Log in user to the app.
3.	**Load Predefined Habits:** Load 5 predefined habits with 2 weekly and 3 daily habits.
4.	**Add New Habit:** Add new habit by specifying name and frequency (daily or weekly).
5.	**Check-off Habits:** Mark habit by specifying it's name as completed.
6.	**Delete Habit:** Delete habit by specifying it's name.
7.	**View Daily Habits:** Display daily habits with their streaks with GUI.
8.	**View Weekly Habits:** Display weekly habits with their streaks with GUI.
9.	**View All Habits:** Display all habits including their creation date and thier number of streaks with GUI.
10.	**View Longest Habit Streak:** Display habit with the highest number streaks with GUI.
11.	**View Struggled Habits Last Month:** Display habit that user struggled with in the previous month with GUI.
12.	**Logout:** Log out current user from the app.
13.	**Exit App:** Exit Habit Tracker app.


## 🛠️ Tests

Unittest framework is used to test the Habit Tracker App crucial features. All the key features are put to test in test_habit_tracker.py.

    python -m unittest test_habit_tracker.py


## 📄 License

- This project is not undr any licensed.


## 👨‍💻 Authors

- Kareem Adams


## 🧾 Acknowledgments

- Icons by FontAwesome.
- Data visualization by Matplotlib.


## 📬 Feedback & Support

- Have feedback or need help? Feel free to open an issue or reach out at kareem@kerrysson.com.
