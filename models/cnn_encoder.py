import tensorflow as tf
"""
    One layer MLP to transfer CNN encodings for the GRU layers.
    Bahdanau Attention
    Helped by:
    https://www.tensorflow.org/tutorials/text/image_captioning
    https://arxiv.org/pdf/1502.03044.pdf
"""
class CNN_Encoder(tf.keras.Model):
    def __init__(self, embedding_dim):
        super(CNN_Encoder, self).__init__()
        self.fc = tf.keras.layers.Dense(embedding_dim)
    
    def call(self, x):
        x = self.fc(x)
        x = tf.nn.relu(x)
        return x