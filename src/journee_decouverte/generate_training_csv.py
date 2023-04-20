import os
import re

from PIL import Image

from main import init_csv, csv_file, circle_color

if __name__ == '__main__':
    init_csv()
    for _dir in os.listdir('imgs/captured'):
        if not re.match(r'^\d$', _dir):
            continue
        for image in os.listdir(f'imgs/captured/{_dir}'):
            print(image)
            img: Image = Image.open(f'imgs/captured/{_dir}/{image}')
            _mean = circle_color(img)
            with open(csv_file, 'a+') as fp:
                print(f"{_dir},{_mean[0]},{_mean[1]},{_mean[2]}", file=fp)
                fp.close()
