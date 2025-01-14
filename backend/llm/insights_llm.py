import os
import openai
from helper import *
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

# Base BP reading provided
base_reading = {'id': 1364955, 'type': 'BP', 'value': '136/54 (60)', 'timeStr': '11/01/2024 10:46', 'timestamp': 1730472400000}

# Function to generate BP values with variations
def generate_bp_values():
    systolic = random.randint(110, 180)  # Elderly may have a wider range
    diastolic = random.randint(50, 90)
    pulse = random.randint(55, 90)
    # return f"{systolic}/{diastolic} ({pulse})"
    return (systolic,diastolic,pulse)

# Function to generate timestamp and timeStr for different times of the day
def generate_time_for_day(date):
    time_of_day = random.choice(["08:00", "12:00", "15:30", "18:00", "21:45"])
    datetime_str = f"{date.strftime('%m/%d/%Y')} {time_of_day}"
    datetime_obj = datetime.strptime(datetime_str, '%m/%d/%Y %H:%M')
    timestamp = int(datetime_obj.timestamp() * 1000)
    return datetime_str, timestamp

# Generate readings for the entire month
def generate_readings():
    readings = []
    # readings.append(base_reading)

    start_date = datetime.strptime('11/01/2024', '%m/%d/%Y')
    for day_offset in range(0, 30):  # From November 2 to November 30
        current_date = start_date + timedelta(days=day_offset)
        num_readings_per_day = random.randint(1, 3)  # 1 to 3 readings per day

        for _ in range(num_readings_per_day):
            # reading = {
            #     'id': base_reading['id'],
            #     'type': base_reading['type'],
            #     'value': generate_bp_values(),
            #     'timeStr': None,
            #     'timestamp': None
            # }
            systolic, diastolic, pulse = generate_bp_values()
            time_str, _ = generate_time_for_day(current_date)
            reading = {
                'date': time_str,
                'systolic': systolic,
                'diastolic': diastolic,
                'pulse': pulse
            }
            # time_str, timestamp = generate_time_for_day(current_date)
            # reading['timeStr'] = time_str
            # reading['timestamp'] = timestamp
            readings.append(reading)

    return readings

def generate_visuals(readings):
    # Convert data to a DataFrame
    df = pd.DataFrame(readings)
    df['date'] = pd.to_datetime(df['date'])

    # Sort by date
    df = df.sort_values('date')

    # Plotting
    plt.figure(figsize=(14, 6))
    plt.plot(df['date'], df['systolic'], label='Systolic', color='red', marker='o')
    plt.plot(df['date'], df['diastolic'], label='Diastolic', color='blue', marker='o')
    plt.plot(df['date'], df['pulse'], label='Diastolic', color='green', marker='o')
    plt.xlabel('Date')
    plt.ylabel('BP Values')
    plt.title('Systolic, Diastolic and Pulse BP Readings Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def generate_insights(username, readings): 
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI()

    syst = f""" 
    You are a blood pressure analyzer and a helpful assistant for the elderly. 
    You will be talking with {username}, greet them and provide their health report.
    The blood pressure readings are present in READINGS. Your task is to analyse these readings and give the users a comprehensive summary of their health and blood pressure over the provided time frame.
    Utilise the information given below to help drive your analysis:
    
    Blood pressure categories for adults 65+  | Systolic mm Hg | Diastolic mm Hg
    Low blood pressure	                      |  90 or lower   |  60 or lower
    Normal blood pressure	                  | Lower than 120 | Lower than 80
    Elevated blood pressure	                  | 120-129	       | Lower than 80
    High blood pressure stage 1 (severe)	  | 130-139	       | 80-89
    High blood pressure stage 2 (more severe) | 140 or higher  | 90 or higher
    High blood pressure crisis (see your doctor immediately)	| 180 or higher	 | 120 or higher

    The analysis should be put forward in such a manner that it doesnt cause panic among the elderly reading it. Mention the positives and highlight the days where blood pressure readings didn't
    look so good. Dont make the summary too big as the elderly wouldn't wanna spend too much time reading it, keep it under 150 words. 
    Provide the analysis in a conversational tone and in paragraphs not pointers. Talk as if a nurse would talk to her patients, but make sure you sound like an assistant in an application.

    READINGS = {readings}
    """


    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content" : syst}
        ]
    )

    response = completion.choices[0].message.content

    print(response)


if __name__ == "__main__":
    readings = generate_readings()
    for r in readings:
        print(r)
    print("\n")
    # generate_visuals(readings)
    generate_insights("Prasoon" , readings)





