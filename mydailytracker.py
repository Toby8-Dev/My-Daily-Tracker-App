import json
from datetime import date

FILENAME = "data.json"
today = str(date.today())

def load_data():
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    
def save_data(data):
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)
    
def add_habit(data):
    habit = input("Enter the name of your habit: ")
    if "habit_list" not in data:
        data["habit_list"] = []
    data["habit_list"].append(habit)
    print(f"Habit '{habit}' added.")
    save_data(data)

def add_mood(data):
    mood = input("Enter the name of your mood: ")
    if "mood_list" not in data:
        data["mood_list"] = []
    data["mood_list"].append(mood)
    print(f"Mood '{mood}' added.")
    save_data(data)

def log_day(data):
    print(f"Today is {today}.")
    if "habit_list" not in data:
        print("You have no habits yet! Add some first.")
        return
    for i, habit in enumerate(data["habit_list"]):
        print(f"{i}. {habit}")
    print("Which habits did you complete today? (Type numbers separated by space, e.g., 0 2 3)")
    print("If none, just press Enter.")
    done_input = input("> ")
    done_indices = [int(x) for x in done_input.split() if x.isdigit()]
    if "days" not in data:
        data["days"] = {}
    if today not in data["days"]:
        data["days"][today] = {"habits": {}, "mood": None}
    for i, habit in enumerate(data["habit_list"]):
        data["days"][today]["habits"][habit] = i in done_indices
    if "mood_list" not in data or not data["mood_list"]:
        print("You have no moods set! Please add moods first.")
        return
    print("\nHow are you feeling today? Pick one mood:")
    for i, mood in enumerate(data["mood_list"]):
        print(f"{i}. {mood}")
    while True:
        mood_choice = input("Mood number: ")
        if mood_choice.isdigit():
            mood_choice = int(mood_choice)
            if 0 <= mood_choice < len(data["mood_list"]):
                data["days"][today]["mood"] = data["mood_list"][mood_choice]
                print(f"Mood saved as: {data['mood_list'][mood_choice]}")
                break
        print("Please enter a valid mood number.")
    print("Today's progress saved!")
    save_data(data)

def view_day(data):
    if "days" not in data:
        print("No days logged yet!")
        return
    day_keys = list(data["days"].keys())
    for i, day_key in enumerate(day_keys):
        print(f"{i}. {day_key}")
    choice = int(input("Choose what day you want to see. (number): "))
    if 0 <= choice <len(day_keys):
        selected_day = day_keys[choice]
        day_data = data["days"][selected_day]
        print(f"\nData for {selected_day}:")
        print("Habits:")
        for habit, done in day_data.get("habits", {}).items():
            status = "✔" if done else "❌"
            print(f"- {habit}: {status}")
        mood = day_data.get("mood")
        print(f"Mood: {mood}")
    else:
        print("Invalid choice.")

def main():
    while True:
        data = load_data()
        print("===My Daily Tracker=== \n Welcome! \n 1. Log your day \n 2. Add habits \n 3. Add mood \n 4. View your day \n 5. Instructions \n 6. Exit")
        choice = input("Choose: ")
        if choice == "1":
            log_day(data)
        elif choice == "2":
            add_habit(data)
        elif choice == "3":
            add_mood(data)
        elif choice == "4":
            view_day(data)
        elif choice == "5":
            print("These are the instructions for this app.")
            print("To log your day, type number 1. If you don't have any habits yet, just type number 2. You can add as many habits as you want.")
            print("If you don't have any moods, type number 3. You can also add as many moods as you want. Then you can log your day.")
            print("First you have to type what habits you completed, then what was your mood. If you ever want to see what you did on a certain day, just type number 4.")
            print("Then, type a number of what day you want to see. Thank you! :)")
        elif choice == "6":
            save_data(data)
            print("Thank you for using this app! Bye! :)")
            print("Made by Toby8-dev (Tobias Pecho). :)")
            break
        else:
            print("Invalid choice. Try again.")
    
if __name__ == "__main__":
    main()