import re
from datetime import datetime
import matplotlib.pyplot as plt

def extract_data_from_file(filename, pattern):
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()

    matches = re.findall(pattern, html_content, re.DOTALL)
    return matches

# Sample HTML content
data = {}

with open("bodyweight.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Define the regex pattern to match dates and bodyweights
bw_pattern = r'<div class="date"><div class="value">(\w{3} \d{1,2}, \d{4})</div></div><div class="bodyweight"><div class="value">([\d.]+)</div></div>'
exercise_pattern = r'<span class="history-value date">(\d{2}-\w{3}-\d{2})</span>.*?<div class="values-column">(.*?)<\/div>.*?<div class="values-column">(.*?)<\/div>'


# Find all matches using the pattern
bodyweight_matches = extract_data_from_file("bodyweight.html", bw_pattern)
data["bodyweight"] = bodyweight_matches

# get squat max values
# Create a dictionary to store the highest e1RM value for each date
files = ["squat.html", "bench.html", "deadlift.html"]

for file in files:
    exercise_type = file.split('.')[0]
    exercise_matches = extract_data_from_file(file, exercise_pattern)
    highest_e1rm_values = {}

    for date, lift, e1rm in exercise_matches:
        e1rm = e1rm+lift
        date = date.strip()
        e1rm = re.sub(r'[^0-9. ]', '', e1rm)
        e1rm = e1rm.split()
        print(e1rm)

        e1rm = [float(x) for x in e1rm]
        # Check if the date is already in the dictionary and if the current e1rm is higher
        mx = max(e1rm)
        if date in highest_e1rm_values:
            if mx > highest_e1rm_values[date]:
                highest_e1rm_values[date] = mx
        else:
            highest_e1rm_values[date] = mx
    data[exercise_type] = highest_e1rm_values

# Convert bodyweight data to the same format as other data
formatted_bodyweight_data = {}
print(data)

for date_str, weight_str in data["bodyweight"]:
    # Convert date string to the desired format 'DD-Mon-YY'
    date_obj = datetime.strptime(date_str, '%b %d, %Y')
    formatted_date = date_obj.strftime('%d-%b-%y')

    # Convert weight string to float
    weight = float(weight_str)

    # Add the formatted date and weight to the dictionary
    formatted_bodyweight_data[formatted_date] = weight

data['bodyweight'] = formatted_bodyweight_data

# for key, value in data.items():
#     print(f"{key} data:")
#     for date, result in value.items():
#         print(f"Date: {date}, Value: {result} lb")
# print(data)
# Convert date strings to datetime objects for sorting
for label, exercise_data in data.items():
    data[label] = {datetime.strptime(date, "%d-%b-%y"): value for date, value in exercise_data.items()}

# Sort the data by date
for label, exercise_data in data.items():
    data[label] = dict(sorted(exercise_data.items()))

# Create a figure and primary axes
fig, ax1 = plt.subplots()

# Create a dictionary to store the secondary y-axes for each exercise category
secondary_axes = {}

# Plot the exercise data on the primary y-axis and create secondary y-axes
for label, exercise_data in data.items():
    if label != 'bodyweight':
        print(exercise_data.values())
        ax1.plot(exercise_data.keys(), exercise_data.values(), label=label, linestyle='dashed', marker='')
    else:
        secondary_axes[label] = ax1.twinx()
        secondary_axes[label].plot(exercise_data.keys(), exercise_data.values(), label=label, color='red', linestyle='dashed', marker='')

# Set labels and legends for the primary axes
ax1.set_xlabel('Date')
ax1.set_ylabel('Exercise Values')
ax1.legend(loc='upper left')

# Set labels and legends for the secondary axes
for label, ax in secondary_axes.items():
    ax.set_ylabel(f'{label.capitalize()}')
    ax.legend(loc='upper right')


plt.rc('lines', linewidth=1.5)
# Show the plot
plt.show()