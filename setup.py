# -*- coding: utf-8 -*-
"""
Created by: Mistayan
Project: President-Game
IDE: PyCharm
Creation-date: 11/26/22
"""
import os
import sys
from subprocess import Popen

from setuptools import setup

BASEDIR = os.path.dirname(os.path.abspath(__file__))
ENV_NAME = "venv"
VENV_PYTHON = os.path.join(BASEDIR, ENV_NAME, "Scripts", "python.exe")

if __name__ == "__main__":
    print("Upgrading pip and wheel :\n"
          "\t- upgrading pip ensure you match last security standards \n"
          "\t- wheel is faster than pip, allowing smaller downloads and faster install")
    check_pip = Popen("py -m pip install --upgrade pip".split()).communicate()
    check_wheel = Popen("py -m pip install --upgrade wheel".split()).communicate()

    if sys.argv and len(sys.argv) < 2:
        if not os.path.exists(os.path.join(BASEDIR, "venv")):
            print(f"Creating virtual environment : {ENV_NAME}")
            # communicate, so we know what happens
            init = Popen(f"python -m venv {ENV_NAME}".split()).communicate()  # <==
        print("Applying requirements ...")
        check_pip = Popen(f"{VENV_PYTHON} -m pip install --upgrade pip".split()).communicate()
        check_wheel = Popen(f"{VENV_PYTHON} -m pip install --upgrade wheel".split()).communicate()
        install = Popen(f"{VENV_PYTHON} -m pip install -r requirements.txt".split()).communicate()

        # argparse.ArgumentParser(
        #     prog="setup.py",
        #     exit_on_error=True,
        #     parents=[]
        #                         )
    else:
        setup(
            name='OVA_Finder',
            version='0.42.0',
            description="""AI Training with OVA.""",
            author='Mistayan',
            url='https://github.com/Mistayan/AI_Training',
            author_email='helixmastaz@gmail.com',
            packages=[],
            requires=['Python (>=3.11)'],
            # from requirements.txt
            install_requires=[
                'numpy',
                'pandas',
                'matplotlib',
                'seaborn',
                'scipy',
                'scikit-learn',
                'scikit-image',
                'coloredlogs',
                'paho-mqtt'
            ],  # external packages as dependencies
            license="MIT",
            long_description="""
        Future plans :
                    - use OpenCV to detect circles
                    - from detected circles get the color
                    - make beautiful MelodyX with the colors (and buzzer)
        """
        )
