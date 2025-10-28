# @'
# # plot_scores.py
# import pandas as pd
# import glob
# import numpy as np
# import matplotlib.pyplot as plt
# import os

# def extract_final_score(path):
#     try:
#         df = pd.read_csv(path)
#         # find last numeric entry in 'score' column
#         if 'score' in df.columns:
#             vals = df['score'].dropna().values
#             if len(vals)>0:
#                 last = vals[-1]
#                 try:
#                     return float(last)
#                 except:
#                     return None
#     except:
#         return None

# def mean_scores(pattern):
#     files = glob.glob(pattern)
#     arr=[]
#     for f in files:
#         s = extract_final_score(f)
#         if s is not None:
#             arr.append(s)
#     return arr

# human = mean_scores("data/runs/run_human_*.csv")
# helper = mean_scores("data/runs/run_human_helper*.csv")
# model = mean_scores("data/runs/run_model_*.csv")

# # ensure results directory
# os.makedirs("results", exist_ok=True)
# plt.boxplot([human if human else [0], helper if helper else [0], model if model else [0]], labels=['Human','Human+Helper','Model'])
# plt.ylabel("Score")
# plt.savefig("results/score_boxplot.png")
# print("Saved results/score_boxplot.png")
# '@ | Out-File -Encoding utf8 plot_scores.py


# plot_scores.py
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import os

def extract_final_score(path):
    try:
        df = pd.read_csv(path)
        if 'score' in df.columns:
            vals = df['score'].dropna().values
            if len(vals)>0:
                last = vals[-1]
                try:
                    return float(last)
                except:
                    return None
    except:
        return None

def mean_scores(pattern):
    files = glob.glob(pattern)
    arr=[]
    for f in files:
        s = extract_final_score(f)
        if s is not None:
            arr.append(s)
    return arr

human = mean_scores("data/runs/run_human*.csv")
helper = mean_scores("data/runs/run_human_helper*.csv")
model = mean_scores("data/runs/run_model_*.csv")

os.makedirs("results", exist_ok=True)
plt.boxplot([human if human else [0], helper if helper else [0], model if model else [0]], labels=['Human','Human+Helper','Model'])
plt.ylabel("Score")
plt.savefig("results/score_boxplot.png")
print("Saved results/score_boxplot.png")
