# PyCharm has a bug where it does not stop at breakpoints (see https://youtrack.jetbrains.com/issue/PY-44361)
# Fix: use the decorator `@tf.autograph.experimental.do_not_convert`

import tensorflow as tf

class MyLoss(tf.keras.losses.Loss):
    def __init__(self):
        super().__init__()
        # put your __init__ layers here
        self.d2 = Dense(10)

    @tf.autograph.experimental.do_not_convert   # breakpoint now recognized with this decorator
    def call(self, inputs, training=None, mask=None):
        x = self.conv1(inputs)
        x = self.flatten(x)
        x = self.d1(x)
        return self.d2(x)
