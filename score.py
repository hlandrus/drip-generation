import ast
import pandas as pd
from generate import papers_to_df

def read_first_run():
    fp = open('first_run.txt', 'r') 
    lines = fp.readlines()

    papers = {}

    for line in lines:
        if "paper: " in line:
            paper_number = int(line.split(" ")[1])
            papers[paper_number] = {"drips": []}
        elif "number_drips: " in line:
            number_drips = int(line.split(" ")[1])
            papers[paper_number]["number_drips"] = number_drips
        elif "hanna_score: " in line:
            hanna_score = int(line.split(" ")[1])
            papers[paper_number]["hanna_score"] = hanna_score
        else:
            drip = ast.literal_eval(line.strip())
            papers[paper_number]["drips"].append(drip)

    return papers

def first_run_to_df():
    papers = read_first_run()
    return papers_to_df(papers, True)
    