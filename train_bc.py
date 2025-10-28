    # @'
    # # train_bc.py
    # import torch, torch.nn as nn, torch.optim as optim
    # import pandas as pd
    # import numpy as np
    # from sklearn.model_selection import train_test_split

    # DATA = "data/runs/run_oracle.csv"
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # class BCNet(nn.Module):
    #     def __init__(self, inp=4, hid=128, out=3):
    #         super().__init__()
    #         self.net = nn.Sequential(
    #             nn.Linear(inp, hid), nn.ReLU(),
    #             nn.Linear(hid, hid), nn.ReLU(),
    #             nn.Linear(hid, out)
    #         )
    #     def forward(self,x):
    #         return self.net(x)

    # def load_data(path):
    #     df = pd.read_csv(path)
    #     df = df[df['oracle_action']!=-1]
    #     X = df[['d','h','speed','y']].values.astype(np.float32)
    #     y = df['oracle_action'].astype(int).values
    #     return X, y

    # def main():
    #     X, y = load_data(DATA)
    #     if len(X) < 10:
    #         print("Not enough data. Collect oracle demos first.")
    #         return
    #     X_train, X_val, y_train, y_val = train_test_split(X,y,test_size=0.1, random_state=42)
    #     model = BCNet().to(device)
    #     opt = optim.Adam(model.parameters(), lr=1e-3)
    #     loss_fn = nn.CrossEntropyLoss()
    #     bs=256
    #     for epoch in range(1,21):
    #         perm = np.random.permutation(len(X_train))
    #         model.train()
    #         total=0; loss_acc=0
    #         for i in range(0,len(perm),bs):
    #             idx = perm[i:i+bs]
    #             xb = torch.from_numpy(X_train[idx]).to(device)
    #             yb = torch.from_numpy(y_train[idx]).to(device)
    #             logits = model(xb)
    #             loss = loss_fn(logits, yb)
    #             opt.zero_grad(); loss.backward(); opt.step()
    #             loss_acc += loss.item()*len(idx); total += len(idx)
    #         model.eval()
    #         with torch.no_grad():
    #             v = torch.from_numpy(X_val).to(device)
    #             logits = model(v)
    #             pred = logits.argmax(dim=1).cpu().numpy()
    #             acc = (pred == y_val).mean()
    #         print(f"Epoch {epoch} train_loss={loss_acc/total:.4f} val_acc={acc:.4f}")
    #     torch.save(model.state_dict(), "models/bc_model.pth")
    #     print("Saved models/bc_model.pth")

    # if __name__ == "__main__":
    #     main()
    # '@ | Out-File -Encoding utf8 train_bc.py


    # train_bc.py
import torch, torch.nn as nn, torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

DATA = "data/runs/run_oracle.csv"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class BCNet(nn.Module):
        def __init__(self, inp=4, hid=128, out=3):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(inp, hid), nn.ReLU(),
                nn.Linear(hid, hid), nn.ReLU(),
                nn.Linear(hid, out)
            )
        def forward(self,x):
            return self.net(x)

def load_data(path):
        df = pd.read_csv(path)
        # keep only rows where oracle_action exists
        if 'oracle_action' not in df.columns:
            raise ValueError("oracle_action column missing in CSV")
        df = df[df['oracle_action'] != -1]
        X = df[['d','h','speed','y']].values.astype(np.float32)
        y = df['oracle_action'].astype(int).values
        return X, y

def main():
        X, y = load_data(DATA)
        if len(X) < 10:
            print("Not enough data. Collect oracle demos first.")
            return
        X_train, X_val, y_train, y_val = train_test_split(X,y,test_size=0.1, random_state=42)
        model = BCNet().to(device)
        opt = optim.Adam(model.parameters(), lr=1e-3)
        loss_fn = nn.CrossEntropyLoss()
        bs=256
        for epoch in range(1,21):
            perm = np.random.permutation(len(X_train))
            model.train()
            total=0; loss_acc=0
            for i in range(0,len(perm),bs):
                idx = perm[i:i+bs]
                xb = torch.from_numpy(X_train[idx]).to(device)
                yb = torch.from_numpy(y_train[idx]).to(device)
                logits = model(xb)
                loss = loss_fn(logits, yb)
                opt.zero_grad(); loss.backward(); opt.step()
                loss_acc += loss.item()*len(idx); total += len(idx)
            model.eval()
            with torch.no_grad():
                v = torch.from_numpy(X_val).to(device)
                logits = model(v)
                pred = logits.argmax(dim=1).cpu().numpy()
                acc = (pred == y_val).mean()
            print(f"Epoch {epoch} train_loss={loss_acc/total:.4f} val_acc={acc:.4f}")
        torch.save(model.state_dict(), "models/bc_model.pth")
        print("Saved models/bc_model.pth")

if __name__ == "__main__":
        main()
