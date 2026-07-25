import json
import os
from datetime import datetime
import requests

# File path to save output
FILE_PATH = "data.json"

# Global variable to hold the most recently fetched result
latest_fetched_data = None


def fetch_weather():
    """Fetch current weather data for a specified city using wttr.in API."""
    global latest_fetched_data
    
    city = input("Enter city name: ").strip()
    if not city:
        print("\n❌ City name cannot be empty.\n")
        return

    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            print(f"\n❌ Error fetching weather data (HTTP {response.status_code}).\n")
            return
            
        data = response.json()
        
        # Extract fields from wttr.in JSON structure
        current_condition = data["current_condition"][0]
        
        temp_c = current_condition["temp_C"]
        humidity = current_condition["humidity"]
        wind_speed_kmh = current_condition["windspeedKmph"]
        weather_desc = current_condition["weatherDesc"][0]["value"]
        
        # Format current timestamp
        now = datetime.now()
        timestamp_display = now.strftime("%d-%m-%Y %I:%M %p")
        timestamp_iso = now.strftime("%Y-%m-%d %H:%M:%S")

        # Display result
        print("\n------ Weather Report ------")
        print(f"City: {city.title()}")
        print(f"Temperature: {temp_c}°C")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed_kmh} km/h")
        print(f"Condition: {weather_desc}")
        print(f"Fetched At: {timestamp_display}")
        print("----------------------------\n")

        # Prepare dictionary for saving
        latest_fetched_data = {
            "type": "weather",
            "city": city.title(),
            "temperature": float(temp_c),
            "humidity": float(humidity),
            "condition": weather_desc,
            "time": timestamp_iso
        }

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Network error: Could not reach weather service. ({e})\n")
    except (KeyError, IndexError):
        print(f"\n❌ Could not parse weather data for '{city}'. Please verify the city name.\n")


def fetch_currency():
    """Fetch real-time exchange rates using open.er-api.com API."""
    global latest_fetched_data
    
    base_curr = input("Base Currency (e.g., USD): ").strip().upper()
    target_curr = input("Target Currency (e.g., BDT): ").strip().upper()
    
    if not base_curr or not target_curr:
        print("\n❌ Currency codes cannot be empty.\n")
        return

    url = f"https://open.er-api.com/v6/latest/{base_curr}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200 or data.get("result") != "success":
            print(f"\n❌ Failed to fetch rates for currency: {base_curr}\n")
            return

        rates = data.get("rates", {})
        
        if target_curr not in rates:
            print(f"\n❌ Currency '{target_curr}' not found in exchange rate table.\n")
            return

        rate = rates[target_curr]
        
        # Format current timestamp
        now = datetime.now()
        timestamp_display = now.strftime("%d-%m-%Y %I:%M %p")
        timestamp_iso = now.strftime("%Y-%m-%d %H:%M:%S")

        # Display result
        print(f"\n1 {base_curr} = {rate:.2f} {target_curr}")
        print(f"Fetched At: {timestamp_display}\n")

        # Prepare dictionary for saving
        latest_fetched_data = {
            "type": "currency",
            "base": base_curr,
            "target": target_curr,
            "rate": round(float(rate), 2),
            "time": timestamp_iso
        }

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Network error: Could not reach currency service. ({e})\n")


def save_json():
    """Save the most recently fetched data to data.json file."""
    global latest_fetched_data
    
    if not latest_fetched_data:
        print("\n⚠️ No new data fetched yet. Fetch weather or currency data first!\n")
        return

    try:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(latest_fetched_data, file, indent=4)
        print(f"\n✅ Data successfully saved to '{FILE_PATH}'.\n")
    except IOError as e:
        print(f"\n❌ Failed to write to file: {e}\n")


def view_json():
    """Read and display saved data from data.json if it exists."""
    if not os.path.exists(FILE_PATH):
        print(f"\n⚠️ File '{FILE_PATH}' does not exist yet. Please fetch and save data first.\n")
        return

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        print("\n------ Last Saved Data ------")
        data_type = data.get("type", "").capitalize()
        print(f"Type: {data_type}")

        if data.get("type") == "weather":
            print(f"City: {data.get('city')}")
            print(f"Temperature: {data.get('temperature')}°C")
            print(f"Humidity: {data.get('humidity')}%")
            print(f"Condition: {data.get('condition')}")
        elif data.get("type") == "currency":
            print(f"Base Currency: {data.get('base')}")
            print(f"Target Currency: {data.get('target')}")
            print(f"Exchange Rate: {data.get('rate')}")

        print(f"Saved Time: {data.get('time')}")
        print("-----------------------------\n")

    except json.JSONDecodeError:
        print(f"\n❌ File '{FILE_PATH}' exists but contains invalid JSON.\n")
    except IOError as e:
        print(f"\n❌ Error reading file: {e}\n")


def main_menu():
    """Main program execution loop."""
    while True:
        print("========== Data Fetcher ==========")
        print("1. Current Weather")
        print("2. Currency Exchange Rate")
        print("3. Save Result to JSON File")
        print("4. View Previous Saved Data")
        print("5. Exit")
        print("==================================")
        
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            fetch_weather()
        elif choice == "2":
            fetch_currency()
        elif choice == "3":
            save_json()
        elif choice == "4":
            view_json()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("\n❌ Invalid choice! Please select a number from 1 to 5.\n")


if __name__ == "__main__":
    main_menu()