import requests
from datetime import datetime
import os

# ************************* NUTRITIONIX API **********************************
APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")

GENDER = "MALE"
WEIGHT_KG = "78"
HEIGHT = "178.5"
AGE = "23"

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_input = input("Tell which exercise you did today?: ")

header = {
    "x-app-id": APP_ID,
    'x-app-key': API_KEY
}

parameters = {
    'query': exercise_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT,
    "age": AGE,
}

response = requests.post(url=exercise_endpoint, json=parameters, headers=header)
response.raise_for_status()
result = response.json()
print(result)


# ************************* SHEETY API **********************************
today = datetime.now()
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = today.strftime("%I:%M:%S")

# Add a row to your sheet
sheet_endpoint = "https://api.sheety.co/bd3ba7012c55722734bcf0e6204ef4fb/myWorkouts2/workouts"

BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
}

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=headers)

    print(sheet_response.text)
