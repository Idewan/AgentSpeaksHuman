import tensorflow as tf

"""
    Bahdanau Attention -- 
"""
class BahdanauAttention(tf.keras.Model):
    def __init__(self, units):
        super(BahdanauAttention, self).__init__()
        self.W1 = tf.keras.layers.Dense(units)
        self.W2 = tf.keras.layers.Dense(units)
        self.V = tf.keras.layers.Dense(1)
    
    def call(self, features, hidden):
        #Hidden shape
        hidden_with_time_axis = tf.expand_dims(hidden, 1)

        #Attention hidden layer
        attention_hidden_layer = (tf.nn.tanh(self.W1(features) + 
                                  self.W2(hidden_with_time_axis)))
        
        #Unformalized score for each image features
        score = self.V(attention_hidden_layer)

        #Attention weights
        attention_weights = tf.nn.softmax(score, axis=1)

        #Context vector
        context_vector = attention_weights * features
        context_vector = tf.reduce_sum(context_vector, axis=1)

        return context_vector, attention_weights

"""
    LSTM Decoder 
"""
class GRU_Speaker(tf.keras.Model):
    def __init__(self, embedding_dim, units, vocab_size):
        super(LSTM_Decoder, self).__init__()
        self.units = units

        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.lstm = tf.keras.layers.GRU(self.units, return_sequences=True, 
                                        return_state=True,
                                        recurrent_initializer='glorot_uniform')
        self.fc1 = tf.keras.layers.Dense(self.units)
        self.fc2 = tf.keras.layers.Dense(vocab_size)

        self.attention = BahdanauAttention(self.units)

    def call(self, x, features, hidden):
        context_vector, attention_weights = self.attention(features, hidden)

        x = self.embedding(x)

        x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=-1)

        output, state = self.lstm(x)

        x =  self.fc1(output)

        x = tf.reshape(x, (-1, x.shape[2]))

        x = self.fc2(x)

        return x, state, attention_weights
    
    def reset_state(self, batch_size):
        return tf.zeros((batch_size, self.units))