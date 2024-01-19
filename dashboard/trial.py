original_data = [
    {"month": 1, "year": 2019, "stk": 255155.5},
    {"month": 2, "year": 2019, "stk": 256995.5},
    # Add more data if needed
]

converted_data = {}

for entry in original_data:
    year = entry["year"]
    month = entry["month"]
    stk = entry["stk"]

    if year not in converted_data:
        converted_data[year] = {"month": [], "stk": []}

    converted_data[year]["month"].append(month)
    converted_data[year]["stk"].append(stk)

print(converted_data)