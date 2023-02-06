import numpy as np
import pandas as pd
import hashlib
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def raffle(s, sampleList, w, k):
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
        comment = """# Mocaverse Raffle\n\n## Congrats! The winners are: \n\n""" + \
            table.to_markdown() + "\n"
        f.write(comment)


# load in snapshot
logging.info("Starting.....")
table = pd.read_csv("data/holders.csv")
# Sort by address
table.sort_values(by=table.columns[0], inplace=True)
logging.info(f"Loading....\n Snapshot Table\n{table.head(10)}")

# amount of mocalist
k = 1500
logging.info(f"Mocalist: {k} winners .....")

if checkIfDuplicates(table['Address']):
    raise Exception("Yes, list contains duplicates")
else:
    logging.info("No duplicates found in list")
    # raffle
    weights=calculate_weight(table)
    # get block hash as seed
    s='Mocaverse0x713eed01a79cb3a721a5adb9de4a63045d4b835cab07b6921454a968f29af21a'
    result=raffle(s, table, weights, k)
    logging.info("Ta-da! Done!")
    writemd(pd.DataFrame(result, columns =['Winners']), "winners.md")