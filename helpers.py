import itertools

def get_drip_from_row(row, drip_number):
    drip = {
        "corner": row[f"corner_{drip_number}"],
        "corner_location": row[f"corner_location_{drip_number}"],
        "drip_location": (row[f"drip_x_{drip_number}"], row[f"drip_x_{drip_number}"]),
        "time": row[f"time_{drip_number}"],
    }
    return drip 

def get_corner_drip_string(row, drip_number):
    corner_drip_string = (
        str(int(row[f"corner_{drip_number}"]))
        + "_"
        + str(int(row[f"corner_location_{drip_number}"]))
        + "_"
        + str(int(row[f"drip_x_{drip_number}"]))
        + "_"
        + str(int(row[f"drip_y_{drip_number}"]))
    )
    return corner_drip_string

def create_corner_drip_scored_dict(all_painted):
    corner_drip_scored_dict = {
    str(c)
    + "_"
    + str(c_l): {
        str(x) + "_" + str(y): 0 for x, y in itertools.product(range(1, 4), range(1, 4))
    }
    for c, c_l in itertools.product(range(1, 5), range(1, 5))}

    for index, row in all_painted.iterrows():
        score = row["hanna_second_score"] - 1
        number_drips = row["number_drips"]
        for drip_number in range(number_drips - 1):
            corner = (
                str(int(row[f"corner_{drip_number}"]))
                + "_"
                + str(int(row[f"corner_location_{drip_number}"]))
            )
            drip_location = (
                str(int(row[f"drip_x_{drip_number}"]))
                + "_"
                + str(int(row[f"drip_y_{drip_number}"]))
            )
            corner_drip_scored_dict[corner][drip_location] += score

    return corner_drip_scored_dict

def create_drip_corner_scored_dict(all_painted):
    drip_corner_scored_dict = {
        str(c)
        + "_"
        + str(c_l): {
            str(x) + "_" + str(y): 0 for x, y in itertools.product(range(1, 5), range(1, 5))
        }
        for c, c_l in itertools.product(range(1, 4), range(1, 4))}

    for index, row in all_painted.iterrows():
        score = row["hanna_second_score"] - 1
        number_drips = row["number_drips"]
        for drip_number in range(number_drips - 1):
            next_corner = (
                str(int(row[f"corner_{drip_number + 1}"]))
                + "_"
                + str(int(row[f"corner_location_{drip_number + 1}"]))
            )
            drip_location = (
                str(int(row[f"drip_x_{drip_number}"]))
                + "_"
                + str(int(row[f"drip_y_{drip_number}"]))
            )
            drip_corner_scored_dict[drip_location][next_corner] += score
    
    return drip_corner_scored_dict

def create(all_painted):
    drip_pairs = []
    for index, row in all_painted.iterrows():
        score = row["hanna_second_score"]
        number_drips = row["number_drips"]
        for i in range(number_drips - 1):
            current_drip = get_drip_from_row(row, i)
            next_drip =  get_drip_from_row(row, i + 1)
            drip_pair = {"current_drip": current_drip, "next_drip": next_drip, "score": score}
            drip_pairs.append(drip_pair)
    return drip_pairs

def select_one_corner(i, all_painted):
    corner_df = all_painted[
        [
            f"corner_{i}",
            f"corner_location_{i}",
            f"drip_x_{i}",
            f"drip_y_{i}",
            f"time_{i}",
            "hanna_second_score"
        ]
    ]
    return corner_df.rename(
        columns={
            f"corner_{i}": "corner",
            f"corner_location_{i}": "corner_location",
            f"drip_x_{i}": "drip_x",
            f"drip_y_{i}": "drip_y",
            f"time_{i}": "time",
        }
    )