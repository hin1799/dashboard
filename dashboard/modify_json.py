def json_for_weekwise_raw(data):
    converted_data = {"week_no": set(), "year": {}}

    for entry in data:
        week = entry["week_no"]
        year = entry["year"]
        stk = entry["stk"]

        converted_data["week_no"].add(week)

        if year not in converted_data["year"]:
            converted_data["year"][year] = []

        converted_data["year"][year].append(stk)
    return converted_data

def json_for_monthwise_raw(data):
    converted_data = {"month": set(), "year": {}}

    for entry in data:
        month = entry["month"]
        year = entry["year"]
        stk = entry["stk"]

        converted_data["month"].add(month)

        if year not in converted_data["year"]:
            converted_data["year"][year] = []

        converted_data["year"][year].append(stk)

    return converted_data

def json_for_percentage_data(data):
    converted_data = {"date": [], "data": {"spr_per": [], "gas_per": [], "dist_per": []}}
    for entry in data:
        date = entry["date"]
        spr_per = entry["spr_per"]
        gas_per = entry["gas_per"]
        dist_per = entry["dist_per"]

        converted_data["date"].append(date)
        converted_data["data"]["spr_per"].append(spr_per)
        converted_data["data"]["gas_per"].append(gas_per)
        converted_data["data"]["dist_per"].append(dist_per)
    
    return converted_data

def json_for_percentage_data_yearly(data):
    converted_data = {"year": [], "data": {"spr_per": [], "gas_per": [], "dist_per": []}}
    for entry in data:
        year = entry["year"]
        spr_per = entry["spr_per"]
        gas_per = entry["gas_per"]
        dist_per = entry["dist_per"]

        converted_data["year"].append(year)
        converted_data["data"]["spr_per"].append(spr_per)
        converted_data["data"]["gas_per"].append(gas_per)
        converted_data["data"]["dist_per"].append(dist_per)

    return converted_data

def json_for_weekwise_difference(data):
    converted_data = {"week_diff": [], "year": {}}

    flag=0
    for entry in data:
        week_diff = entry["week_diff"]
        year = entry["year"]
        stk = entry["stk"]

        if flag==0:
            converted_data["week_diff"].append(week_diff)
            if week_diff == "51-52":
                flag=1

        if year not in converted_data["year"]:
            converted_data["year"][year] = []

        converted_data["year"][year].append(stk)

    return converted_data

def json_for_summer_analysis(data):
    converted_data = {"date": [], "stk": []}

    for entry in data:
        date_str = entry["date"]
        stk = entry["stk"]

        converted_data["date"].append(date_str)
        converted_data["stk"].append(stk)

    return converted_data

def json_for_weekwise_aggregation(data):
    converted_data = {"week": [], "data": {"avg": [], "min":[], "max":[], "yr2023":[]}}

    for entry in data:
        week = entry["week_month"]
        avg = entry["avg"]
        min = entry["minimum"]
        max = entry["maximum"]
        yr2023 = entry["data_2023"]

        converted_data["week"].append(week)
        converted_data["data"]["avg"].append(avg)
        converted_data["data"]["min"].append(min)
        converted_data["data"]["max"].append(max)
        converted_data["data"]["yr2023"].append(yr2023)

    return converted_data

def json_for_monthwise_aggregation(data):
    converted_data = {"month": [], "data": {"avg": [], "min": [], "max": [], "yr2023": []}}

    for entry in data:
        month = entry["week_month"]
        avg = entry["avg"]
        min = entry["minimum"]
        max = entry["maximum"]
        yr2023 = entry["data_2023"]

        converted_data["month"].append(month)
        converted_data["data"]["avg"].append(avg)
        converted_data["data"]["min"].append(min)
        converted_data["data"]["max"].append(max)
        converted_data["data"]["yr2023"].append(yr2023)
    
    return converted_data

def json_for_build_draw_monthwise(data):
    converted_data = {"year": [], "data": {"from_month_stk": [], "to_month_stk": [], "build_or_draw": []}}

    for entry in data:
        year = entry["year"]
        curr = entry["curr_month_stk"]
        prev = entry["prev_month_stk"]
        build_draw = entry["build_or_draw"]

        converted_data["year"].append(year)
        converted_data["data"]["from_month_stk"].append(curr)
        converted_data["data"]["to_month_stk"].append(prev)
        converted_data["data"]["build_or_draw"].append(build_draw)
    
    return converted_data

def json_for_build_draw_years(data):
    converted_data = {"date": [], "data": {"stk": [], "diff": []}}

    for entry in data:
        date = entry["date"]
        stk = entry["stk"]
        diff = entry["diff"]

        converted_data["date"].append(date)
        converted_data["data"]["stk"].append(stk)
        converted_data["data"]["diff"].append(diff)
    return converted_data

def json_for_build_draw_percentage(data):
    converted_data = {"month": [], "data": {"build_per": [], "draw_per": []}}

    for entry in data:
        month = entry["month"]
        build_per = entry["build_per"]
        draw_per = entry["draw_per"]

        converted_data["month"].append(month)
        converted_data["data"]["build_per"].append(build_per)
        converted_data["data"]["draw_per"].append(draw_per)
    return converted_data

def json_for_build_draw_percentage_weekly(data):
    converted_data = {"week": [], "data": {"build_per": [], "draw_per": []}}

    for entry in data:
        week = entry["week"]
        build_per = entry["build_per"]
        draw_per = entry["draw_per"]

        converted_data["week"].append(week)
        converted_data["data"]["build_per"].append(build_per)
        converted_data["data"]["draw_per"].append(draw_per)
    return converted_data