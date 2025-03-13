from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Habit:
    """
    Represents a habit to be tracked.

    Attributes:
        name (str): The name of the habit.
        periodicity (str): The frequency of the habit ('daily' or 'weekly').
        checkoffs (List[datetime]): Dates and times when the habit was checked off.
        streak (int): The current streak of consecutive completions.
        created_at (datetime): The date and time when the habit was created.
    """
    name: str
    periodicity: str  # 'daily' or 'weekly'
    checkoffs: List[datetime] = field(default_factory=list)
    streak: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def check_off(self) -> None:
        """
        Marks the habit as completed for the current date and time. Updates the streak if it's a new checkoff.
        """
        now = datetime.now()
        
        # Check if the habit has already been checked off today (for daily habits) or this week (for weekly habits)
        if self.periodicity == 'daily':
            already_checked = any(check.date() == now.date() for check in self.checkoffs)
        elif self.periodicity == 'weekly':
            already_checked = any((now - check).days < 7 for check in self.checkoffs)

        if not already_checked:
            self.checkoffs.append(now)
            self.update_streak()
            print(f"Habit '\033[1m{self.name}\033[0m' checked off at {now}.")
        else:
            print(f"Habit '\033[1m{self.name}\033[0m' is already checked off for the current {'day' if self.periodicity == 'daily' else 'week'}.")

    def update_streak(self) -> None:
        """
        Updates the streak based on the habit's checkoffs, accounting for periodicity.
        """
        if not self.checkoffs:
            self.streak = 0
            return

        # Sort checkoffs by date and time
        self.checkoffs.sort()
        current_streak = 1
        last_check = self.checkoffs[0]

        for check in self.checkoffs[1:]:
            if self.periodicity == 'daily' and (check.date() - last_check.date()).days == 1:
                current_streak += 1
            elif self.periodicity == 'weekly' and 0 < (check.date() - last_check.date()).days <= 7:
                current_streak += 1
            else:
                current_streak = 1
            last_check = check

        self.streak = max(self.streak, current_streak)

    def is_broken(self) -> bool:
        """
        Determines if the habit streak is broken.

        Returns:
            bool: True if the streak is broken, False otherwise.
        """
        if not self.checkoffs:
            return True

        last_check = self.checkoffs[-1]
        now = datetime.now()

        if self.periodicity == 'daily' and (now.date() - last_check.date()).days > 1:
            return True
        elif self.periodicity == 'weekly' and (now.date() - last_check.date()).days > 7:
            return True

        return False