"""Creates a block with dense layers."""
from tensorflow import keras


class DenseBlock(keras.layers.Layer):
    """Subclass the Keras Layer class."""

    def __init__(self,
                 n_inputs=128,
                 num_hidden=4,
                 hidden_width='default',
                 output_width='default',
                 hidden_config=dict(activation='relu',
                                    kernel_initializer='he_normal'),
                 output_config=dict(activation=None,
                                    kernel_initializer='he_normal'),
                 **kwargs):
        """
        Create a block with dense layers.

        Arguments:
            n_inputs -- the number of inputs to the network
            num_hidden -- the number of hidden layers. 
            hidden_width -- width of each hidden layer. By default, this is
                the same width as the input layer. 
            output_width -- width of output layer. By default, this is
                the same width as the input layer. 
            hidden_config -- Python dictionary with keyword arguments to
                pass to the dense hidden layers
            output_config -- Python dictionary with keyword arguments to
                pass to the final dense (linear) layer
            **kwargs -- additional keyword arguments. Can be used to name the
                residual block.
        """
        super().__init__(**kwargs)

        self.n_inputs = n_inputs
        self.num_hidden = num_hidden

        if hidden_width == 'default':
            hidden_width = n_inputs
        self.hidden_width = hidden_width 

        if output_width == 'default':
            output_width = n_inputs
        self.output_width = output_width 

        # Construct a list of the hidden layers used in this block
        self.layers = [keras.layers.Dense(hidden_width,
                                          name='hidden{}'.format(i),
                                          **hidden_config)
                       for i in range(num_hidden)]
        # Append the output layer
        self.layers.append(keras.layers.Dense(output_width,
                                              name='output',
                                              **output_config))

    def call(self, inputs):
        """Run given inputs through the block."""
        x = inputs
        for layer in self.layers:
            x = layer(x)
        return x  # Add input to output
