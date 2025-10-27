@'
# eval.py
import torch, numpy as np
from game import DinoGame
from logger import RunLogger
from train_bc import BCNet
import argparse
import helper

parser = argparse.ArgumentParser()
parser.add_argument("--n", type=int, default=30)
args = parser.parse_args()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BCNet().to(device)
model.load_state_dict(torch.load("models/bc_model.pth", map_location=device))
model.eval()

def bc_oracle(state):
    x = np.array(state, dtype=np.float32)
    import torch
    t = torch.from_numpy(x).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(t)
        action = int(logits.argmax(dim=1).cpu().item())
    return action

# replace helper oracle with bc
helper.oracle_action = bc_oracle

scores = []
for i in range(args.n):
    logger = RunLogger(f"data/runs/run_model_{i}.csv")
    g = DinoGame(helper_on=True, auto_mode=True, logger=logger)
    s = g.run()
    scores.append(s)
    logger.close()
print("Mean score:", sum(scores)/len(scores))
'@ | Out-File -Encoding utf8 eval.py
