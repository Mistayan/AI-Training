import os


def gen_file(filename: str, save_dir="plots", fext=".txt"):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    if os.path.exists(os.path.join(save_dir, filename)):
        fname = filename
        if filename.__contains__('.'):
            fname, fext = filename.split(".")
        for i in range(999):
            fn = f"{fname}-{i}.{fext}"
            if not os.path.exists(os.path.join(save_dir, fn)):
                filename = fn
                break
    return os.path.join(save_dir, filename)
