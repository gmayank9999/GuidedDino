# @'
# # logger.py
# import csv, os, time
# from datetime import datetime

# class RunLogger:
#     def __init__(self, filepath):
#         self.filepath = filepath
#         os.makedirs(os.path.dirname(filepath), exist_ok=True)
#         new = not os.path.exists(filepath)
#         self.f = open(filepath, "a", newline='', encoding='utf8')
#         self.writer = csv.writer(self.f)
#         if new:
#             self.writer.writerow(["timestamp","run_id","step","d","h","speed","y","player_action","oracle_action","helper_on","score"])
#         self.run_id = int(time.time())
#         self.step = 0

#     def log_step(self, state, player_action, oracle_action, helper_on, score):
#         d,h,speed,y = state
#         self.writer.writerow([datetime.utcnow().isoformat(), self.run_id, self.step, float(d), float(h), float(speed), float(y), int(player_action), int(oracle_action), int(helper_on), int(score)])
#         self.step += 1
#         self.f.flush()

#     def end_run(self, final_score):
#         self.writer.writerow([datetime.utcnow().isoformat(), self.run_id, "END", final_score])
#         self.f.flush()
#         self.run_id = int(time.time())
#         self.step = 0

#     def close(self):
#         self.f.close()
# '@ | Out-File -Encoding utf8 logger.py

# logger.py
import csv, os, time
from datetime import datetime

class RunLogger:
    def __init__(self, filepath):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        new = not os.path.exists(filepath)
        self.f = open(filepath, "a", newline='', encoding='utf8')
        self.writer = csv.writer(self.f)
        if new:
            self.writer.writerow(["timestamp","run_id","step","d","h","speed","y","player_action","oracle_action","helper_on","score"])
        self.run_id = int(time.time())
        self.step = 0

    def log_step(self, state, player_action, oracle_action, helper_on, score):
        # state = (d,h,speed,y) expected here
        try:
            d,h,speed,y = state
        except:
            # fallback default values
            d = state[0] if len(state) > 0 else 999
            h = state[1] if len(state) > 1 else 0
            speed = state[2] if len(state) > 2 else 0
            y = state[3] if len(state) > 3 else 0
        # ensure numeric oracle_action
        oa = -1 if oracle_action is None else oracle_action
        try:
            oa = int(oa)
        except:
            oa = -1
        self.writer.writerow([datetime.utcnow().isoformat(), self.run_id, self.step, float(d), float(h), float(speed), float(y),
                              int(player_action), int(oa), int(helper_on), int(score)])
        self.step += 1
        self.f.flush()

    def end_run(self, final_score):
        self.writer.writerow([datetime.utcnow().isoformat(), self.run_id, "END", final_score])
        self.f.flush()
        self.run_id = int(time.time())
        self.step = 0

    def close(self):
        try:
            self.f.close()
        except:
            pass
