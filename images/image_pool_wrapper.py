import os
import shutil
import cv2 as cv


class ImagePoolWrapper:
    def __init__(self, path, name = ''):
        # parent path
        path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', path))

        self.name = name
        self.path = path

        if name == '':
            name = path

        self.images = list()
        
        # if path is a file, create a folder with the same name and put the file there
        if not os.path.isdir(path):
            print(f'{path} is a file, creating a folder with the same name and putting the file there')
            if not os.path.exists(path + '.png'):
                print(f'{path + ".png"} does not exist, failed to create folder')

                self.path = path + '.png'
                return
            
            os.makedirs(path, exist_ok=True)
            shutil.copy(path + '.png', path + '\\0.png')


        for i in list(filter(lambda x: '.png' in x, os.listdir(path))):
            print(self.path + '\\' + i)
            self.images.append(cv.imread(self.path + '\\' + i, cv.IMREAD_COLOR))

    def add_image(self, img):
        last_image_number = 0
        
        for file in list(filter(lambda x: '.png' in x, os.listdir(self.path))):
            last_image_number = max(last_image_number, int(file.split('\\')[-1].split('.')[0]))

        img.save(os.path.join(self.path, f'{last_image_number + 1}.png'))
        self.images.append(cv.imread(os.path.join(self.path, f'{last_image_number + 1}.png'), cv.IMREAD_COLOR))

