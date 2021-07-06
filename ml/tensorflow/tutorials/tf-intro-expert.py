# https://www.tensorflow.org/tutorials/quickstart/advanced

import tensorflow as tf

from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model

tf.random.set_seed(1)  # set random seed so that we can compare results
print("is exeucting eagerly", tf.executing_eagerly())  # default is eager execution

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0  # 255 is the max value for RGB (could also use max(x_train.max(), y_train.max()) to normalise)

# Add a (channels) dimension ([10 000, 28, 28]) -> ([10 000, 28, 28, 1])
x_train = x_train[..., tf.newaxis].astype("float32")
x_test = x_test[..., tf.newaxis].astype("float32")

# Use tf.data to batch / shuffle the dataset
train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(10000).batch(32)  #10,000 is the total number of rows (the buffer) to be shuffled
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)  # creates batches of 32 to test


class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv1 = Conv2D(32, 3, activation="relu")  # Convoluted 2D layer mainly used for spatial/image problems)
        self.flatten = Flatten()
        self.d1 = Dense(128, activation="relu")  # Regular densely connected NN layer w/128 nodes
        self.d2 = Dense(10)  

    def call(self, x):  # The order of the calls/operations to be made on inputs when making the graph (graph = execution order for non-eager execution)
        x = self.conv1(x)  
        x = self.flatten(x)
        x = self.d1(x)
        return self.d2(x)


# Create an instance of the model
model = MyModel()

# Choose an optimizer and loss function for training:
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)  # e.g. MSE or CrossEntropy (how close we are to desired)
# Loss object example. e.g. a human trying to open the door. Running away from door = 0 points. Touching handle = 0.3 points. Turning handle = 0.5 points. Open door = 1 point.
# Loss object example 2. e.g. points on the graph, want to make sure all same distance away, use Mean squared Error
# It's the method we're using to score the model.

optimizer = tf.keras.optimizers.Adam()  # How to change the model to get closer to desired
# Optimiser - how we can improve the model, e.g. change the weights in the NN to improve accuracy



# Select the metrics to measure the loss / model accuracy.
# The metrics accumulate the values over the epochs -> print overall result
train_loss = tf.keras.metrics.Mean(name="train_loss")
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name="train_accuracy")

test_loss = tf.keras.metrics.Mean(name="test_loss")
test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name="test_accuracy")


# Train the model
@tf.function  # Converts to non-eager (graph) execution => can't use tf.print() on tensors, but faster.
def train_step(images, labels):
    with tf.GradientTape() as tape:
        # training=True required if layers are different behaviours during training vs inference (e.g. dropout)
        predictions = model(images, training=True)
        # import pdb; pdb.set_trace()
        loss = loss_object(labels, predictions)
        # breakpoint()
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    train_loss(loss)
    train_accuracy(labels, predictions)


# Test the model
@tf.function
def test_step(images, labels):
    # training=False is only needed if there are layers with different
    # behavior during training versus inference (e.g. Dropout).
    predictions = model(images, training=False)
    t_loss = loss_object(labels, predictions)

    test_loss(t_loss)
    test_accuracy(labels, predictions)
    # breakpoint()


EPOCHS = 5  # number of times to go through entire dataset
for epoch in range(EPOCHS):
    # Reset the metrics at the start of the next epoch
    train_loss.reset_states()
    train_accuracy.reset_states()
    test_loss.reset_states()
    test_accuracy.reset_states()

    for images, labels in train_ds:
        train_step(images, labels)

    for test_images, test_labels in test_ds:
        test_step(test_images, test_labels)

    print(
        f'Epoch {epoch + 1}, '
        f'Loss: {train_loss.result()}, '
        f'Accuracy: {train_accuracy.result() * 100}, '
        f'Test Loss: {test_loss.result()}, '
        f'Test Accuracy: {test_accuracy.result() * 100}'
    )
