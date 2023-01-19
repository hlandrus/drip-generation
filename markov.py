import itertools
import pandas as pd
import random

NUMBER_CORNERS = 4
NUMBER_LOCATIONS = 3
NUMBER_XS = 3
NUMBER_YS = 3


class MarkovModel:
    def __init__(self, df):
        self.df = df
        self.corner_drip_scored_dict = self.create_corner_drip_scored_dict()
        self.drip_corner_scored_dict = self.create_drip_corner_scored_dict()

        self.drips_df = self.create_drips_df()

        self.times_list = self.create_times_list()
        self.len_time_list = len(self.times_list)

        self.corners_list = self.create_corners_list()
        self.len_corners_list = len(self.corners_list)

        self.number_drips_list = self.create_number_drips_list()
        self.len_number_drips_list = len(self.number_drips_list)

    def create_corner_drip_scored_dict(self):
        corner_drip_scored_dict = {
            str(c) + "_" + str(c_l): {"list_length": 0, "x_y_list": []}
            for c, c_l in itertools.product(
                range(1, NUMBER_CORNERS + 1), range(1, NUMBER_LOCATIONS + 1)
            )
        }

        for index, row in self.df.iterrows():
            score = row["hanna_second_score"]
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
                corner_drip_scored_dict[corner]["list_length"] += score
                corner_drip_scored_dict[corner]["x_y_list"] += [
                    drip_location for i in range(score)
                ]

        return corner_drip_scored_dict

    def get_drip_given_corner(self, corner):
        list_length = self.corner_drip_scored_dict[corner]["list_length"]
        x_y_list = self.corner_drip_scored_dict[corner]["x_y_list"]
        return x_y_list[random.randint(0, list_length - 1)]

    def create_drip_corner_scored_dict(self):
        drip_corner_scored_dict = {
            str(x) + "_" + str(y): {"list_length": 0, "corner_loc_list": []}
            for x, y in itertools.product(
                range(1, NUMBER_XS + 1), range(1, NUMBER_YS + 1)
            )
        }

        for index, row in self.df.iterrows():
            score = row["hanna_second_score"]
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
                drip_corner_scored_dict[drip_location]["list_length"] += score
                drip_corner_scored_dict[drip_location]["corner_loc_list"] += [
                    next_corner for i in range(score)
                ]

        return drip_corner_scored_dict

    def get_corner_given_drip(self, drip):
        list_length = self.drip_corner_scored_dict[drip]["list_length"]
        corner_loc_list = self.drip_corner_scored_dict[drip]["corner_loc_list"]
        return corner_loc_list[random.randint(0, list_length - 1)]

    def select_one_corner(self, i):
        corner_df = self.df[
            [
                f"corner_{i}",
                f"corner_location_{i}",
                f"drip_x_{i}",
                f"drip_y_{i}",
                f"time_{i}",
                "hanna_second_score",
            ]
        ]
        corner_df.loc[:, "corner_and_location"] = (
            corner_df.loc[:, f"corner_{i}"].astype(int).astype(str)
            + "_"
            + corner_df.loc[:, f"corner_location_{i}"].astype(int).astype(str)
        )

        return corner_df.rename(
            columns={
                f"corner_{i}": "corner",
                f"corner_location_{i}": "corner_location",
                f"drip_x_{i}": "drip_x",
                f"drip_y_{i}": "drip_y",
                f"time_{i}": "time",
            }
        )

    def create_drips_df(self):
        drips_df = pd.concat([self.select_one_corner(i) for i in range(5)])
        drips_df = drips_df[drips_df.loc[:, "drip_x"] != 0].reset_index()
        return drips_df

    def create_times_list(self):
        top_score = self.drips_df[self.drips_df["hanna_second_score"] == 2][
            "time"
        ].tolist()
        mid_score = self.drips_df[self.drips_df["hanna_second_score"] == 1][
            "time"
        ].tolist()

        times_list = top_score + top_score + mid_score
        return times_list

    def get_time(self):
        return self.times_list[random.randint(0, self.len_time_list - 1)]

    def create_corners_list(self):
        top_score = self.drips_df[self.drips_df["hanna_second_score"] == 2][
            "corner_and_location"
        ].tolist()
        mid_score = self.drips_df[self.drips_df["hanna_second_score"] == 1][
            "corner_and_location"
        ].tolist()

        corner_list = top_score + top_score + mid_score
        return corner_list

    def get_corner(self):
        return self.corners_list[random.randint(0, self.len_corners_list - 1)]

    def create_number_drips_list(self):
        top_score = self.df[self.df["hanna_second_score"] == 2]["number_drips"].tolist()
        mid_score = self.df[self.df["hanna_second_score"] == 1]["number_drips"].tolist()

        number_drips_list = top_score + top_score + mid_score
        return number_drips_list

    def get_number_drips(self):
        return self.number_drips_list[random.randint(0, self.len_number_drips_list - 1)]
