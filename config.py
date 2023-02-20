import os

base_dir = os.getcwd().split("\\")
i = 0
for i, b in enumerate(base_dir):
    if b == "AI-Training":
        break
base_dir = os.path.join('\\'.join(base_dir[0: i + 1]))
