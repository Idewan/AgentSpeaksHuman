import tensorflow as tf
import numpy as np
import json
import random
from ..models.prep import Preparation

from tqdm import tqdm

"""
Feature Encoding pre-loads Resnet50 trained on imagenet weights without the last softmax layer.
It then encodes the images that were cleaned up so that there are no duplicates by another script.
It saves all the encodings as dataset/prep_data/*.npy.

"""

if __name__ == "__main__":

    image_model = tf.keras.applications.ResNet50(include_top=False, weights='imagenet')
    image_input = image_model.input
    hidden_layer = image_model.layers[-1].output
    image_features_extract_model = tf.keras.Model(image_input, hidden_layer)

    with open("./captions.json", "r") as jf:
    data = json.loads(jf.read())
    data.pop("lstm_labels")
    image_paths = list(data.keys())
    random.shuffle(image_paths)

    img_name_vector = []
    for i in range(len(image_paths)):
        img_name_vector.append(f"./prep_data/{image_paths[i]}.jpg")

    encode_train = sorted(set(img_name_vector))
    image_dataset = tf.data.Dataset.from_tensor_slices(encode_train)
    prep = Preparation()
    image_dataset = image_dataset.map(prep.load_image).batch(16)

    for img, path in tqdm(image_dataset):
        batch_features = image_features_extract_model(img)
        batch_features = tf.reshape(batch_features,
                                    (batch_features.shape[0], -1, batch_features.shape[3]))
        for bf, p in zip(batch_features, path):
            path_of_feature = p.numpy().decode("utf-8")[:-4]
            np.save(path_of_feature, bf.numpy())
    
    print('Done!')