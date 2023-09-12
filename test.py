import re

with open("deadlift.html", "r", encoding="utf-8") as file:
    html_content = file.read()

exercise_date_pattern = r'<span class="history-value date">(.*?)</span>'
exercise_e1rm_pattern = r'<span class="history-value">([\d.]+ lb)</span>'
block_pattern = r'<div class="exercises-row values">(.*?)</div>'

data = {}

html_blocks = re.findall(block_pattern, html_content, re.DOTALL)

for html_block in html_blocks:

    date_match = re.search(exercise_date_pattern, html_block)
    date = date_match.group(1) if date_match else None

    e1rm_matches = re.findall(exercise_e1rm_pattern, html_block)

    e1rm_values = [float(re.sub(r'^[0-9.]', '', value)) for value in e1rm_matches]
    highest_e1rm = max(e1rm_values) if e1rm_values else None
    if date:
        data[date] = highest_e1rm

print(data)
# for date, val in data:
#     print(f"{date}, {val}\n")