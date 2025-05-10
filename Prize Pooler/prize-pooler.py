import argparse
import yaml
import os
import math

PROJECT_PATH        = os.path.dirname(os.path.abspath(__file__))
DISTRIBUTION_PATH   = os.path.join(PROJECT_PATH, "distributions.yml")

def prepare_arg_parser():
    parser = argparse.ArgumentParser(prog="Prize-Pooler",        
                                     description="Calculates Prize Pools")
    
    parser.add_argument("-p",
                        "--pool",
                        dest        = "pool",
                        required    = True, 
                        type        = int,
                        help        = "Total amount of Keys.")
    parser.add_argument("-m",
                        "--mode",
                        dest        = "mode",
                        required    = True, 
                        nargs       = 1,
                        type        = str,
                        choices     = ["s", "d"],
                        help        = "What distribution are we calculating for?")
    
    return parser


def load_distributions(config_path):
    loaded_data = {}
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            loaded_data = yaml.safe_load(file)
    else:
        print ("Distributions could not be found at specified path")
    
    return loaded_data

def validate_distribution(distribution):
    valid       = True
    total       = 0

    for div, shares in distribution.items():
        div_total   = 0

        total += shares["share"]
        
        for share in shares["distribution"]:
            div_total += share

        if div_total != 100 and div_total != 100.0:
            print (f"Total of {div} division is {div_total}")
            valid = False
        
    if total != 100 and total != 100.0:
        print (f"All divisions add up to {total}")
        valid = False

    return valid

def calculate_prizes (pool, distribution):
    prize_pool = {}
    
    # Distribute keys over all divs
    key_total = 0
    for div, shares in distribution.items():
        div_pool = {}
        
        div_pool["p"]       = shares["share"]
        keys                = math.floor(pool * (shares["share"] / 100))
        div_pool["keys"]    = keys
        key_total           += keys

        rank_distribution = []
        for share in shares["distribution"]:
            rank_share = {}
            rank_share["p"] = share
            rank_distribution.append(rank_share)
        div_pool["distribution"] = rank_distribution

        prize_pool[div] = div_pool

    key_remainder   = pool - key_total
    divs            = list(distribution.keys())
    i               = 0
    while key_remainder > 0:
        prize_pool[divs[i]]["keys"] += 1
        i = (i + 1) % len(divs)
        key_remainder -= 1

    # Distribute keys within each div
    for div, shares in prize_pool.items():
        div_keys = shares["keys"]

        
        key_total = 0
        for rank_share in shares["distribution"]:
            rank_keys = math.floor(div_keys * (rank_share["p"] / 100))
            rank_share["keys"] = rank_keys
            key_total += rank_keys

        key_remainder   = div_keys - key_total
        i               = 0
        while key_remainder > 0:
            shares["distribution"][i]["keys"] += 1
            i = (i + 1) % len(shares["distribution"])
            key_remainder -= 1

    return prize_pool


def format_prize_pool (pool, prizes):
    formatted = ""
    formatted += f"Total Pool: {pool} Keys \n\n"

    for div, shares in prizes.items():
        formatted += f"{div}: {shares['p']:5.2f} % | Total {shares['keys']:3.0f} Keys\n"

        i = 1
        for share in shares["distribution"]:
            formatted += f"   {i}: {share['p']:5.2f} % | Total {share['keys']:3.0f} Keys\n"
            i +=1

        formatted += "\n"

    return formatted

def main():
    parser  = prepare_arg_parser()
    args    = parser.parse_args() 

    match args.mode:
        case "s":   mode = "Soldier Monthly"
        case "d":   mode = "Demoman Monthly"
        case _:     mode = "Soldier Monthly"
    print (f"Loading distribution for mode: {mode}")
    distribution = load_distributions(DISTRIBUTION_PATH)[mode]
    if not validate_distribution(distribution):
        return -1
    
    prizes = calculate_prizes(args.pool, distribution)
    formatted = format_prize_pool(args.pool, prizes)

    print (formatted)


if __name__ == "__main__":
    main()