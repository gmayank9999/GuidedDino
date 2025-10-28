# run_collect.py
import argparse
from game import DinoGame
from logger import RunLogger
import helper

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["human", "helper", "oracle"], help="Mode of data collection")
parser.add_argument("--n", type=int, default=10, help="Number of runs")
args = parser.parse_args()

print(f"Starting data collection: {args.mode} mode for {args.n} runs")

for i in range(args.n):
    if args.mode == "human":
        logger = RunLogger(f"data/runs/run_human_{i}.csv")
        g = DinoGame(helper_on=False, auto_mode=False, logger=logger)

    elif args.mode == "helper":
        logger = RunLogger(f"data/runs/run_human_helper_{i}.csv")
        g = DinoGame(helper_on=True, auto_mode=False, logger=logger)

    elif args.mode == "oracle":
        logger = RunLogger(f"data/runs/run_oracle_{i}.csv")
        g = DinoGame(helper_on=True, auto_mode=True, logger=logger)

    score = g.run()
    logger.end_run(score)
    logger.close()
    print(f"Run {i+1}/{args.n} complete. Score: {score}")

print("---Data collection complete!---")
