from tensorflow.keras.applications.resnet50 import preprocess_input
import tensorflow as tf
import numpy as np

class Preparation():
    """
        Class that stores all the functions that are necessary
        for image processing tasks in the context of this research.
        - Loading Images
        - Loading Image Embedding
        - 
    """
    #Load image
    def load_image(self, image_path):
        img = tf.io.read_file(image_path)
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, (299,299))
        img = preprocess_input(img)

        return img, image_path

    # Load image embedding
    def map_func(self, targ_name, dis_name):
        targ_tensor = np.load("../dataset/prep_data/" + targ_name.decode('utf-8')+'.jpg.npy')
        dis_tensor = np.load("../dataset/prep_data/" + dis_name.decode('utf-8')+'.jpg.npy')
        return targ_tensor, dis_tensor
    
    #Load image embedding and associate the appropriate caption
    def map_func_oracle(self, targ_name, dis_name, cap):
        targ_tensor = np.load("../dataset/prep_data/" + targ_name.decode('utf-8')+'.jpg.npy')
        dis_tensor = np.load("../dataset/prep_data/" + dis_name.decode('utf-8')+'.jpg.npy')
        return targ_tensor, dis_tensor, cap