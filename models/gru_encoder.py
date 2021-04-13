import tensorflow as tf

class GRU_Encoder(tf.keras.Model):
  def __init__(self, embedding_dim, units, vocab_size):
    super(GRU_Encoder, self).__init__()
    self.units = units

    self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
    self.gru = tf.keras.layers.GRU(self.units, return_sequences=True,
                                   return_state=True,
                                   recurrent_initializer='glorot_uniform')

  def call(self, x, hidden):
    # x = self.embedding(x)

    output, state = self.gru(x, initial_state = hidden)

    return output

  def reset_state(self, batch_size):
    return tf.zeros((batch_size, self.units))