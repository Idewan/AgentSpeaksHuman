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
    def map_func(self, image_name, caption):
        image_tensor = np.load(image_name.decode('utf-8')+'.npy')
        return img_tensor, caption
