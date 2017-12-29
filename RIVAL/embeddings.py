from collections import Counter
from datetime import datetime

import tensorflow as tf
import math
import numpy as np
import os
import sys
import pickle

sys.path.append('../')

from RIVAL import download
from RIVAL.settings import DATA_DIR

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
VALIDATION_WORDS = ['C++', '数据库', '程序员', '金融', '人工智能', '设计']


class SkipGram:
    vocab_size = 6000
    FULL = 2
    PROGRESS_ONLY = 1
    MUTE = 0
    skip_window = 10
    embedding_size = 150
    n_sampled = 100
    min_freq = 5
    loss_fn = tf.nn.sampled_softmax_loss

    def __init__(self, graph=tf.Graph()):
        self.graph = graph

    def build_graph(self, device='/cpu:0'):
        print('Constructing computational graph: ')
        with self.graph.as_default(), tf.device(device):
            # inputs: source data for training
            self.x = tf.placeholder(tf.int32, [None], 'input_layer')
            self.y = tf.placeholder(tf.int32, [None, 1], 'labels')

            # parameters of the neural network
            embeddings = tf.Variable(
                tf.random_uniform([self.vocab_size, self.embedding_size], -1.0, 1.0),
                name='embedding_lookup_table'
            )
            softmax_w = tf.Variable(
                tf.truncated_normal(
                    [self.vocab_size, self.embedding_size],
                    stddev=1.0 / math.sqrt(self.embedding_size)
                ),
                name='softmax_weights'
            )
            softmax_b = tf.Variable(tf.zeros([self.vocab_size]), name='softmax_biases')

            # operations
            embed = tf.nn.embedding_lookup(embeddings, self.x, name='word_vectors')
            loss = self.loss_fn(
                weights=softmax_w, biases=softmax_b, inputs=embed,
                labels=self.y, num_sampled=self.n_sampled, num_classes=self.vocab_size
            )
            self.loss = tf.reduce_mean(loss, name='loss')
            self.optimizer = tf.train.AdagradOptimizer(1.0).minimize(loss, name='optimizer')

            norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
            normalized_embeddings = tf.divide(embeddings, norm, name='normalized_lookup_table')

            self.final_embeddings = normalized_embeddings
        print('Construction complete.\n')

    def preprocess(self, words):

        def gen_keep_fn(counts, length):
            def keep_data(word):
                threshold = .5
                count = counts[word]
                fraction = count / length
                prob = (np.sqrt(fraction / .001) + 1) * .001 / fraction
                return prob >= threshold
            return keep_data

        def subsample_data(data):
            data_count = Counter(data)
            total_count = len(data)
            keep_fn = gen_keep_fn(data_count, total_count)
            return list(filter(keep_fn, data))

        print("Preprocessing words with a scale of {}...".format(len(words)))
        count = [['UNK', -1]]
        word_counts = Counter(words)
        most_common = word_counts.most_common(self.vocab_size - 1)
        count.extend(most_common)
        word2idx = {}
        for word, _ in count:
            word2idx[word] = len(word2idx)
        data = []
        unk_count = 0
        for word in words:
            if word in word2idx:
                index = word2idx[word]
            else:
                index = 0
                unk_count += 1
            data.append(index)
        count[0][1] = unk_count
        idx2word = dict(zip(word2idx.values(), word2idx.keys()))

        data = subsample_data(data)

        self.word2idx = word2idx
        self.idx2word = idx2word
        self.data = data
        self.vocab_size = len(self.idx2word)

        print('\tData size after preprocessing: ')
        print('\tNumber of unique words: {}'.format(self.vocab_size))
        print('\tNumber of words in the text: {}'.format(len(self.data)))
        print("Preprocessing complete\n")

    def get_target(self, idx, window_size):
        r = np.random.randint(1, window_size + 1)
        start = idx - r if idx > r else 0
        stop = idx + r
        target_words = set(self.data[start: idx] + self.data[idx + 1: stop + 1])
        return list(target_words)

    def build_dataset(self, window_size=5):
        print("Building dataset with a window size of {}...".format(window_size))
        x, y = [], []
        for i in range(len(self.data)):
            input_word = self.data[i]
            targets = self.get_target(i, window_size)
            x.extend([input_word] * len(targets))
            y.extend(targets)
        print('Building complete, verifying the sizes...')
        assert len(x) == len(y)
        print("Verification complete\n")
        return x, y

    @staticmethod
    def gen_batches(batch_size, x, y):
        print("Generating dataset batches...\n")
        for i in range(0, len(x), batch_size):
            end = i + batch_size
            yield x[i:end], y[i:end]

    def feed(self, words, validation_words):
        self.preprocess(words)
        self.validations = [self.word2idx[word] for word in validation_words]
        with self.graph.as_default(), tf.device('/cpu:0'):
            # validation set and similarity checks
            if hasattr(self, 'validations'):
                validation_embeddings = tf.nn.embedding_lookup(
                    self.final_embeddings, self.validations, name='validation_embeds'
                )
                self.similarity = tf.matmul(
                    validation_embeddings,
                    tf.transpose(self.final_embeddings),
                    name='similarity'
                )

    def train(self, epochs=1, batch_size=128, eval_step=10000, max_iter=None, verbose=FULL):
        print("Start training...")
        with tf.Session(graph=self.graph) as session:
            print('Initializing variables & dataset...')
            tf.global_variables_initializer().run()
            x, y = self.build_dataset(self.skip_window)

            average_loss, iteration = 0, 0
            n_batches = len(x) // batch_size

            print('Initialization complete\n')

            before = datetime.now()
            for epoch in range(epochs):
                batches = self.gen_batches(batch_size, x, y)
                for local_step, (batch_x, batch_y) in enumerate(batches):
                    if max_iter is not None and iteration > max_iter:
                        break
                    feed = {
                        self.x: batch_x,
                        self.y: np.array(batch_y)[:, np.newaxis]
                    }
                    _, loss = session.run([self.optimizer, self.loss], feed_dict=feed)
                    average_loss += loss

                    if verbose >= self.PROGRESS_ONLY and local_step > 0 and local_step % 500 == 0:
                        average_loss /= 500
                        current = datetime.now()
                        print('Epoch {}/{} | Batch {}/{} | Average loss: {:.2f} | Time consumed: {}'.format(
                            epoch + 1, epochs, local_step, n_batches, average_loss, current - before
                        ))
                        before = current
                        average_loss = 0

                    if verbose == self.FULL and iteration > 0 and iteration % eval_step == 0:
                        sim = session.run(self.similarity)
                        self.validate(sim)
                    iteration += 1

            print("Training complete, validation results:")
            sim = session.run(self.similarity)
            self.validate(sim)
            self.final_embeddings = self.final_embeddings.eval()

    def validate(self, similarity, top_k=5):
        for i in range(len(self.validations)):
            nearest = (-similarity[i, :]).argsort()[1:top_k + 1]
            log = "Nearest to [{}]: ".format(self.idx2word[self.validations[i]])
            for k in range(top_k):
                close_word = self.idx2word[nearest[k]]
                log = "{} {}, ".format(log, close_word)
            print(log + '\n')

    def plot(self, num_words=100):
        from sklearn.manifold import TSNE
        from matplotlib import pylab
        tsne = TSNE()
        embedding_2d = tsne.fit_transform(self.final_embeddings[:num_words, :])

        words = [self.idx2word[i] for i in range(num_words)]
        pylab.figure(figsize=(15, 15))
        for i, label in enumerate(words):
            x, y = embedding_2d[i, :]
            pylab.scatter(x, y)
            pylab.annotate(label, xy=(x, y), xytext=(5, 2), textcoords='offset points', ha='right', va='bottom')
        pylab.show()

    def save_embeddings(self, path):
        with open(path, 'wb') as fout:
            save = {
                'embeddings': self.final_embeddings,
                'word2idx': self.word2idx,
                'idx2word': self.idx2word
            }
            print("Saving embeddings and word-to-index, index-to-word dictionaries into file: \n{}".format(path))
            pickle.dump(save, fout, pickle.HIGHEST_PROTOCOL)
        print("Saving complete\n")


def concatenate(files):
    print('Concatenating the words in {} files...'.format(len(files)))
    words = []
    for i, file in enumerate(files):
        w = download.load(file)
        if w is None:
            continue
        words += w
    print("Concatenation complete, {} words in total.\n".format(len(words)))
    return words


def main(datafiles, save_path='.'):
    words = concatenate(datafiles)
    if not len(words):
        return
    engine = SkipGram()
    engine.build_graph()
    engine.feed(words, VALIDATION_WORDS)
    engine.train(epochs=2)
    engine.plot(1000)
    engine.save_embeddings(save_path)


def load(path=os.path.join(DATA_DIR, 'embeddings.pickle')):
    if not path.startswith(DATA_DIR):
        path = os.path.join(DATA_DIR, path)
    with open(path, 'rb') as fin:
        pack = pickle.load(fin)
    return pack['embeddings'], pack['word2idx'], pack['idx2word']


if __name__ == '__main__':
    main(['words0.pickle', 'words1.pickle'])
