original_data = [
    {"month": 1, "year": 2019, "stk": 255155.5},
    {"month": 2, "year": 2019, "stk": 256995.5},
    # Add more data if needed
]

converted_data = {"month": []}

for entry in original_data:
    month = entry["month"]
    year = entry["year"]
    stk = entry["stk"]

    converted_data["month"].append(month)
    converted_data.setdefault(year, []).append(stk)

print(converted_data)
