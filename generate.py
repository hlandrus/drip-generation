import random


def generate_drip():
    drip = {}
    drip["corner"] = random.randint(1, 4)
    drip["corner_location"] = random.randint(1, 3)
    drip["drip_location"] = (random.randint(1, 3), random.randint(1, 3))
    drip["time"] = random.randint(3, 20)

    return drip

def generate_paper():
    paper = {}
    paper["number_drips"] = random.randint(1, 5)
    paper["drips"] = [generate_drip() for drips in range(paper["number_drips"])]
    return paper

papers = {i: generate_paper() for i in range(16)}

with open('first_run.txt', 'w') as fp:
    for paper in papers:
        fp.write(f"paper: {paper}\n")
        fp.write(f"number_drips: {papers[paper]['number_drips']}\n")
        for drip in papers[paper]["drips"]:
            drip_string = "    " + str(drip) + "\n"
            fp.write(drip_string)


"""for paper in papers:
    print(f"paper: {paper}\n")
    print(f"number_drips: {papers[paper]['number_drips']}")
    for drip in papers[paper]["drips"]:
        print(drip)
"""