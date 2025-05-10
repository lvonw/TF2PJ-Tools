import argparse
import yaml
import os

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
                        help        = "Total amount of Keys")

    parser.add_argument("-m",
                        "--mode",
                        dest        = "mode",
                        required    = True, 
                        nargs       = 1,
                        type        = str,
                        choices     = ["s", "d"],
                        help        = "What are we calculating for?")
    
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

def format_prize_pool (pool, distribution):
    print (f"Total Pool: {pool}")
    for div, shares in distribution.items():
        div_pool = pool * (shares["share"] / 100.0)
        print (f"{div}: Total {div_pool:.2f} Keys")

        i = 1
        for share in shares["distribution"]:
            rank_share = div_pool * (share / 100.0)
            print (f"\t{i}: {rank_share:.2f} Keys")
            i +=1




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
    
    print (args.pool)
    format_prize_pool(args.pool, distribution)



if __name__ == "__main__":
    main()