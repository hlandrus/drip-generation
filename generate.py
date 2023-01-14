import random
import pandas as pd

def generate_drip():
    drip = {}
    drip["corner"] = random.randint(1, 4)
    drip["corner_location"] = random.randint(1, 3)
    drip["drip_location"] = (random.randint(1, 3), random.randint(1, 3))
    drip["time"] = random.randint(3, 20)
    drip["hanna_score"] = None
    return drip

def generate_paper():
    paper = {}
    paper["number_drips"] = random.randint(1, 5)
    paper["drips"] = [generate_drip() for drips in range(paper["number_drips"])]
    return paper

def generate_papers_dic(n):
    return {i: generate_paper() for i in range(n)}

def papers_to_df(papers, has_score=False):
    rows = []
    for paper in papers:
        drips = papers[paper]["drips"]
        drips_list = []
        for drip in drips:
            drips_list += [drip['corner'], drip['corner_location'], drip['drip_location'][0], drip['drip_location'][1], drip['time']]
        if has_score:
            row = [paper, papers[paper]["number_drips"], papers[paper]["hanna_score"]] + drips_list
            columns = ["paper_number", "number_drips", "hanna_score"] 
            number_columns = 28
        else:
            row = [paper, papers[paper]["number_drips"]] + drips_list
            columns = ["paper_number", "number_drips"] 
            number_columns = 27
        #print([{f"{direction}_{i}": drip[direction] for direction in drip} for i, drip in enumerate(drips)])
        length_row = len(row)
        row_filled = row + [0.0 for i in range(number_columns - length_row)] 
        rows.append(row_filled)
    
    for i in range(5):
        columns += [f"corner_{i}", f"corner_location_{i}", f"drip_x_{i}", f"drip_y_{i}", f"time_{i}"]

    df = pd.DataFrame(rows, columns=columns)
    return df

def generate_papers_df(n):
    return papers_to_df(generate_papers_dic(n))


"""
with open('second_run.txt', 'w') as fp:
    for paper in papers:
        fp.write(f"paper: {paper}\n")
        fp.write(f"number_drips: {papers[paper]['number_drips']}\n")
        for drip in papers[paper]["drips"]:
            drip_string = "    " + str(drip) + "\n"
            fp.write(drip_string)"""


"""for paper in papers:
    print(f"paper: {paper}\n")
    print(f"number_drips: {papers[paper]['number_drips']}")
    for drip in papers[paper]["drips"]:
        print(drip)
"""