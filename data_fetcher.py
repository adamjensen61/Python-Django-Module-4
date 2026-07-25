import requests
import json
import os
from datetime import datetime

file_name = "data.json"
latest_data = None



def weather():
    global latest_data

    city = input("Enter city name: ")

    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        data = response.json()

        current = data ["current_condition"][0]

        temperature = current["temp_C"]
        humidity = current["humidity"]
        wind_speed = current["windspeedKmph"]
        condition = current["weatherDesc"][0]["value"]

        current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

        print("\n ======== Weather Report ========")
        print("City: ", city)
        print("Temperature: ", temperature + "°C")
        print("Humidity: ", humidity + "%")
        print("Wind speed: ", wind_speed + " km/h")
        print("Condition: ", condition)
        print("Fetched at: ", current_time)
        print("===================================")

        latest_data = {
            "type": "weather",
            "city": city,
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "condition": condition,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        print("Error: ", e)


def currency():
    global latest_data

    base = input("Base currency: ").upper()
    target = input("Target currency: ").upper()

    try:
        url = f"https://open.er-api.com/v6/latest/{base}"
        response = requests.get(url)
        data = response.json()

        if target in data["rates"]:
            rate = data["rates"][target]

            current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

            print()
            print(f"1 {base} = {rate} {target}")
            print("Fetched at: ", current_time)

            latest_data = {
                "type": "currency",
                "base": base, 
                "target": target,
                "rate": rate, 
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        else:
            print("Invalid currency code.")

    except Exception as e:
        print("Error:", e)


def save_json():
    global latest_data

    if latest_data is None:
        print("No data available to save")
        return

    try:
        with open(file_name, "w") as file:
            json.dump(latest_data, file, indent=4)

        print("Data save successfully")

    except Exception as e:
        print("Error:", e)



def view_json():
    if not os.path.exists(file_name):
        print("No saved data found")
        return

    try:
        with open(file_name, "r") as file:
            data = json.load(file)

        print("\n ======= Last saved data ========")

        if data["type"] == "weather":
            print("Type: Weather")
            print("City: ", data["city"])
            print("Temperature: ", str(data["temperature"]) + "°C")
            print("Humidity: ", str(data["humidity"]) + "%")
            print("Wind speed: ", str(data["wind_speed"]) + " km/h")
            print("Condition: ", data["condition"])
            print("Saved time: ", data["time"])

        elif data["type"] == "currency":
            print("Type: Currency")
            print("Base: ", data["base"])
            print("Target: ", data["target"])
            print("Rate: ", data["rate"])
            print("Saved time: ", data["time"])

        print("==============================")

    except Exception as e:
        print("Error: ", e)


def main_menu():

    while True:

        print("\n========== Data Fetcher ============")
        print("1- Current weather")
        print("2- Currency Exchange Rate")
        print("3- Save result to JSON file")
        print("4- View previous saved data")
        print("5- Exit")
        print("======================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            weather()

        elif choice == "2":
            currency()

        elif choice == "3":
            save_json()

        elif choice == "4":
            view_json()

        elif choice == "5":
            print("Thank you")
            break

        else:
            print("Invalid choice !")


main_menu()


