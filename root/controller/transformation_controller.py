import numpy as np
from root.util import ImageUtil as util


class TransformationController():
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.current_image = None
        self.undo_image = None
        self.redo_image = None

    def update_memory_images(self, image):
        self.undo_image = self.current_image
        self.current_image = image
        self.redo_image = self.current_image.copy()

    def getCurrentImage(self):
        return self.current_image

    def undoAction(self):
        self.current_image = self.undo_image
        return self.current_image

    def redoAction(self):
        self.current_image = self.redo_image
        return self.current_image

    def openImage(self, image):
        img = util.read_image(image)
        if len(img.shape) == 2:
            img = converter.rgb_to_gray(self.original_image)
        return img

    def loadImage(self, image):
        self.update_memory_images(self.openImage(image))
        return self.current_image

    def saveImage(self, name, image):
        util.save_image(name, image)

    def save(self, name):
        util.save_image(name, self.current_image)

    def rgb_to_gray(self):
        img = self.current_image
        image = converter.rgb_to_gray(img)
        self.update_memory_images(image)
        return self.current_image
