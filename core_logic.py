import json
import random

def load_surahs(filename="quran_data.json"):
    """Loads Surah data from the JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return []

def generate_weekly_schedule(surahs):
    """Generates a 7-day prayer schedule."""
    if not surahs:
        print("Cannot generate schedule because no Surahs were loaded.")
        return {}

    prayer_names = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    schedule = {}

    # Create a pool of Surahs to choose from.
    # With a full dataset, we could ensure no repeats in a week.
    # With the sample, we will have to repeat, so we shuffle and cycle.
    surah_pool = surahs.copy()

    print("--- Generating 7-Day Prayer Schedule ---")
    for day in range(1, 8):
        day_key = f"Day {day}"
        schedule[day_key] = {}
        random.shuffle(surah_pool) # Shuffle for variety each day

        print(f"\n{day_key}:")
        for i, prayer in enumerate(prayer_names):
            # Cycle through the pool of surahs
            surah = surah_pool[i % len(surah_pool)]
            schedule[day_key][prayer] = surah['name']
            print(f"  {prayer}: {surah['name']}")
            # Simulate scheduling a notification for this prayer
            schedule_notification(prayer, surah['name'], day)

    return schedule

def schedule_notification(prayer_name, surah_name, day):
    """Simulates scheduling a local notification."""
    # In a real app, this would interface with the OS notification service.
    print(f"    -> Notification scheduled for {prayer_name} on Day {day} to read Surah {surah_name}")

if __name__ == "__main__":
    surahs_data = load_surahs()
    weekly_schedule = generate_weekly_schedule(surahs_data)
    print("\n--- Weekly Schedule Generation Complete ---")
    # The 'weekly_schedule' variable now holds the generated schedule data.
    # In a real app, this would be stored and used by the UI.
