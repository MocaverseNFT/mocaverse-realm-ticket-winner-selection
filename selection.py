import numpy as np
import pandas as pd
import hashlib
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def select(s, sampleList, w, k):
    """
    random pick based on the weights without replacement
    """
    seed = int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
    logging.info(f"seed:{s},{seed}")
    rng = np.random.default_rng(seed=seed)
    randomList = rng.choice(
        sampleList.iloc[:, 0].values.tolist(), p=w, size=k, replace=False)
    return randomList


def calculate_weight(sampleList):
    """
    calculate probability based on tickets
    """
    total_tickets = sampleList.iloc[:, 1].sum()
    logging.info(f"Total tickets in this raffle are: {total_tickets}")
    weights = sampleList.iloc[:, 1].values.tolist()/total_tickets
    return weights


def checkIfDuplicates(listOfElems):
    """
    Check if given list contains any duplicates
    """
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True


def writemd(table, file_path):
    with open(file_path, "w") as f:
        comment = """# Mocaverse Realm Ticket Selection Round 2 \n\n## Congrats! The winners are: \n\n""" + \
            table.to_markdown() + "\n"
        f.write(comment)


# load in snapshot
logging.info("Starting.....")
table = pd.read_csv("data/diamondholders.csv")
# Sort by address
table.sort_values(by=table.columns[0], inplace=True)
logging.info(f"Loading....\n Snapshot Table\n{table.head(10)}")

# amount of mocalist
k = 150
logging.info(f"Mocalist: {k} winners .....")

if checkIfDuplicates(table['Address']):
    raise Exception("Yes, list contains duplicates")
else:
    logging.info("No duplicates found in list")
    # raffle
    weights=calculate_weight(table)
    # get block hash as seed
    s='MocaverseDiamond0x538fa6ec160cf840e39a5fe896c8992acb60181aef61f8769d3349767da024cc'
    result=select(s, table, weights, k)
    logging.info("Ta-da! Done!")
    writemd(pd.DataFrame(result, columns =['Winners']), "winners_round2.md")