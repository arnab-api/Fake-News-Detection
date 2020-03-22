# Copyright 2017 Benjamin Riedel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Import relevant packages and modules
from util import *
import random
import tensorflow as tf


# Prompt for mode
mode = input('mode (load / train)? ')


# Set file names
file_train_instances = "Bangla_dataset/our_train_stances.csv"
file_train_bodies = "Bangla_dataset/our_train_body.csv"
file_test_instances = "Bangla_dataset/our_test_stances.csv"
file_test_bodies = "Bangla_dataset/our_test_body.csv"
file_predictions = 'Bangla_dataset/our_predictions_test.csv'


# Initialise hyperparameters
r = random.Random()
lim_unigram = 6000
target_size = 2
hidden_size = 200
train_keep_prob = 0.6
l2_alpha = 0.00001
learn_rate = 0.01
clip_ratio = 5
batch_size_train = 100
epochs = 100


# Load data sets
print("loading dataset")
raw_train = FNCData(file_train_instances, file_train_bodies)
raw_test = FNCData(file_test_instances, file_test_bodies)
print("Dataset loaded")
n_train = len(raw_train.instances)


# Process data sets
train_set, train_stances, bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer = \
    pipeline_train(raw_train, raw_test, lim_unigram=lim_unigram)
feature_size = len(train_set[0])
test_set = pipeline_test(raw_test, bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer)


# Define model

# Create placeholders
features_pl = tf.placeholder(tf.float32, [None, feature_size], 'features')
stances_pl = tf.placeholder(tf.int64, [None], 'stances')
keep_prob_pl = tf.placeholder(tf.float32)

# Infer batch size
batch_size = tf.shape(features_pl)[0]

# Define multi-layer perceptron
hidden_layer = tf.nn.dropout(tf.nn.relu(tf.contrib.layers.linear(features_pl, hidden_size)), keep_prob=keep_prob_pl)
logits_flat = tf.nn.dropout(tf.contrib.layers.linear(hidden_layer, target_size), keep_prob=keep_prob_pl)
logits = tf.reshape(logits_flat, [batch_size, target_size])

# Define L2 loss
tf_vars = tf.trainable_variables()
l2_loss = tf.add_n([tf.nn.l2_loss(v) for v in tf_vars if 'bias' not in v.name]) * l2_alpha

# Define overall loss
#loss = tf.reduce_sum(tf.nn.sparse_softmax_cross_entropy_with_logits(logits, stances_pl) + l2_loss)
loss = tf.reduce_sum(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=stances_pl) + l2_loss)

# Define prediction
softmaxed_logits = tf.nn.softmax(logits)
predict = tf.arg_max(softmaxed_logits, 1)


# Load model
if mode == 'load':
    with tf.Session() as sess:
        load_model(sess)


        # Predict
        test_feed_dict = {features_pl: test_set, keep_prob_pl: 1.0}
        test_pred = sess.run(predict, feed_dict=test_feed_dict)


# Train model
if mode == 'train':
    print("Training Started")
    # Define optimiser
    opt_func = tf.train.AdamOptimizer(learn_rate)
    grads, _ = tf.clip_by_global_norm(tf.gradients(loss, tf_vars), clip_ratio)
    opt_op = opt_func.apply_gradients(zip(grads, tf_vars))

    print("Session Started")
    # Perform training
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for epoch in range(epochs):
            total_loss = 0
            indices = list(range(n_train))
            r.shuffle(indices)
            print("Training =====> EPOCH: " , epoch , end=' :')
            for i in range(n_train // batch_size_train):
                batch_indices = indices[i * batch_size_train: (i + 1) * batch_size_train]
                batch_features = [train_set[i] for i in batch_indices]
                batch_stances = [train_stances[i] for i in batch_indices]
                if(i%10 == 0):
                    print("." , end='')
                batch_feed_dict = {features_pl: batch_features, stances_pl: batch_stances, keep_prob_pl: train_keep_prob}
                _, current_loss = sess.run([opt_op, loss], feed_dict=batch_feed_dict)
                total_loss += current_loss
            print('loss:',total_loss)

        # Predict
        print("Training Ended :: Prediction started")
        predictions = np.zeros(len(test_set))
#        print(type(test_set) , len(test_set))
        sub_part_len = 500
        idx = 0
        while(True):
            start_idx = idx*sub_part_len
            end_idx = (idx+1)*sub_part_len
            flag = True
            if(end_idx >= len(test_set)):
                end_idx = len(test_set)
                flag = False
                
            print(' ===> processing' , start_idx , "to" , end_idx)
            sub_test = test_set[start_idx:end_idx]
            test_feed_dict = {features_pl: sub_test, keep_prob_pl: 1.0}
            test_pred = sess.run(predict, feed_dict=test_feed_dict)
            for i in range(start_idx , end_idx , 1):
                predictions[i] = test_pred[i-start_idx]
            
            if(flag == False):
                break
            idx += 1
            
# Save predictions
print("saving predictions")
save_predictions(predictions, file_predictions)