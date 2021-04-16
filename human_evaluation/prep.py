from tensorflow.keras.applications.resnet50 import preprocess_input
from PIL import Image

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

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
    
    def plot_attention(self, image, result, attention_plot):
        temp_image = np.array(Image.open(image))

        fig = plt.figure(figsize=(10, 10))

        len_result = len(result)
        for l in range(len_result):
            temp_att = np.resize(attention_plot[l], (8, 8))
            ax = fig.add_subplot(len_result, len_result, l+1)
            ax.set_title(result[l])
            img = ax.imshow(temp_image)
            ax.imshow(temp_att, cmap='gray', alpha=0.6, extent=img.get_extent())

        plt.tight_layout()
        plt.show()
