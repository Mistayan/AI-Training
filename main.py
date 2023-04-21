import os
import pickle
import time

import coloredlogs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from numpy import array
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from ova import ChromatX
from ova import OvaClientMqtt

## STATICS ##
center_colors = [(255, 0, 0), (255, 255, 0), (0, 255, 84), (0, 255, 255), (0, 0, 255), (254, 0, 255), (0, 0, 0)]
frequencies = [261, 391, 349, 329, 293, 523, 666]
csv_file = "training.csv"


def mean_color(image):
    # Convert the image to numpy array
    img_array = np.array(image)

    # Calculate the mean color of the image
    mean = np.mean(img_array, axis=(0, 1))

    # Convert the mean color to integers
    mean_color = [int(i) for i in mean]

    return mean_color


def circle_color(image: Image):
    # crop image to 50 height  50 width, in the bottom left corner
    outer_image = image.crop((0, 0, 50, 50))

    # Set the color of the robot's LEDs to the mean color of the outer circle
    _mean_color = mean_color(outer_image)
    return _mean_color


def pixel_color(robot):
    # Get the image from the robot
    image = robot.last_image

    # Calculate the mean color of the pixel area
    _mean_color = mean_color(image)

    # Find the closest color in the center_colors list
    closest_color = None
    closest_distance = float('inf')
    for color in center_colors:
        distance = np.mean(color, _mean_color)
        if distance < closest_distance:
            closest_color = color
            closest_distance = distance

    return closest_color


class RobotTest(OvaClientMqtt, ChromatX):
    def __init__(self, train=False):
        self.__arena = "ishihara"
        super().__init__(id=input("ova_id ?"),
                         username="plop",
                         password="yolo",
                         imgOutputPath="imgs/captured/to_crop.jpeg",
                         arena=self.__arena,
                         server="192.168.10.103")
        # self.color_dict = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (127, 0, 127)]
        self.__previous_color = (255, 255, 255)
        self.__brain = None
        self.__load()
        self.__go = False
        self.__data = self.__x = self.__y = None, None, None
        self.update()
        self.__mean_color = None
        self.__vue = None
        # self.__pool = ThreadPool(processes=2)
        # self.sensors()

    def _onUpdated(self):
        ...

    def _onImageReceived(self, img: Image):
        self.__vue = img
        self.__mean_color = circle_color(self.last_image)

    def train(self):
        self.__go = True

        while self.__go:
            self.update()
            try:
                img = self.last_image
                plt.imshow(img)
                plt.show()
                # grad_mean, var_mean = characterize(self.getImagePixelRGB)

                category = input(f"category ? (1-{len(center_colors)}) 0 to skip")
                if category == "0":
                    continue
                print(self.__mean_color)

                if self.__mean_color:
                    with open(csv_file, 'a+') as fp:
                        print(f"{category},{self.__mean_color[0]},{self.__mean_color[1]},{self.__mean_color[2]}",
                              file=fp,
                              flush=True)

            except KeyboardInterrupt:
                _in = input('stop ? (y/n)')
                self.__go = _in == 'y'
            except ValueError as e:
                print(e.args)
                e.with_traceback(None)

    @property
    def last_image(self) -> Image:
        return self.__vue

    def color_matcher(self):
        """
            when using this method,
            the robot will enter a loop where it will try
            and match the color of the object in front of it
            as fast as possible, and as close as possible from the color
        """
        if self.__brain is None:
            print("Loading csv for recognitions")
            self.__load_csv()
        print("📸 Test camera")
        self.update()
        self.__go = True
        while self.__go:
            self.update()
            _arr = array(self.__mean_color)
            y_pred = self.__brain.predict(_arr.reshape(1, -1))
            y_pred = int(y_pred) - 1
            melody = frequencies[y_pred]
            color = center_colors[y_pred]
            if self.__previous_color != color:
                print(self.__previous_color, " => ", color)
                self.setLedColor(*color)
                self.playMelody([(melody, 100)])
                self.__previous_color = color

            # time.sleep(0.1)

    def sensors(self):
        print("🔦 Test sensors")
        print("Change the light above the robot to see how sensors values change")
        for i in range(5):
            self.update()
            print("⬆️ Photo front lum: ", self.getFrontLuminosity())
            print("⬇️ Photo back lum: ", self.getBackLuminosity())
            print("🔋 Battery voltage: ", self.getBatteryVoltage())
            print("⏱️ Timestamp: ", self.getTimestamp())
            print("📸 Camera img " + str(self.getImageWidth()) + "x" + str(
                self.getImageWidth()) + " shot after " + str(
                self.getImageTimestamp()) + "ms")
            time.sleep(0.1)

    def __load_csv(self):
        if not self.__brain:
            self.__brain = SVC(kernel='linear', C=1, gamma='auto')
        with open(csv_file, 'r') as fp:
            self.__data = pd.read_csv(fp)
            # Split the data into input features (columns 1 to n) and target variable (column 0)
            self.__x = self.__data.iloc[:, 1:].values
            self.__y = self.__data.iloc[:, 0].values
            fp.close()

        print(f"Data loaded : {self.__data}")
        print(f"X : {self.__x}")
        print(f"Y : {self.__y}")
        x_train, x_test, y_train, y_test = train_test_split(self.__x, self.__y, test_size=0.2)
        self.__brain.fit(x_train, y_train)

        y_pred = self.__brain.predict(x_test)
        print(f"Predictions on dataset : {y_pred}")
        # Génération de la matrice de confusion pour vérifier la bonne précision de notre modèle
        print(f"Confusion Matrice :\n{confusion_matrix(y_test, y_pred)}")
        print(classification_report(y_test, y_pred))
        # plot_confusion_matrix("estimator", y_pred, y_test)

    def __load(self):
        # try:
        self.__load_pickle()
        # except Exception as e:
        #     print(e)
        #     self.__load_csv()

    def __load_pickle(self, pickle_file=None):
        print("Loading pickle file")
        if pickle_file is None:
            # list all pickle files
            print("Searching for pickles... ")
            pickle_files = []
            for f in os.listdir('./pickles'):
                if f.endswith(".pkl"):
                    pickle_files.append(f)

            if len(pickle_files) == 0:
                raise FileNotFoundError("No pickle file found")
            # ask user to choose one
            for i, f in enumerate(pickle_files):
                print(f"{i + 1} - {f}")
            pickle_file = pickle_files[int(input("Choose a pickle file to load")) - 1]
        with open("./pickles/" + pickle_file, 'rb') as fp:
            self.__brain = pickle.load(fp)
            fp.close()


def init_csv():
    init = False
    try:
        with open(csv_file, 'r+') as fp:
            if fp.read(1) != "c":
                init = True
                fp.close()
    except:
        init = True
    if init:
        with open(csv_file, 'w+') as fp:
            print("category,r,g,b", file=fp)
            fp.close()


if __name__ == '__main__':
    init_csv()
    bot = RobotTest()
    camera = bot
    mode = input('train ? (y/n)')
    if mode == 'n':
        bot.color_matcher()
    else:
        coloredlogs.install(level='DEBUG', program_name='RobotTest', propagate=True, )
        bot.train()
