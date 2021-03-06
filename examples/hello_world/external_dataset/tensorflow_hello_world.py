#  Copyright (c) 2017-2018 Uber Technologies, Inc.
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

"""Minimal example of how to read samples from a dataset generated by `generate_external_dataset.py`
using tensorflow, using make_batch_reader() instead of make_reader()"""

from __future__ import print_function

import tensorflow as tf

from petastorm import make_batch_reader
from petastorm.tf_utils import tf_tensors, make_petastorm_dataset


def tensorflow_hello_world(dataset_url='file:///tmp/external_dataset'):
    # Example: tf_tensors will return tensors with dataset data
    with make_batch_reader(dataset_url) as reader:
        tensor = tf_tensors(reader)
        with tf.Session() as sess:
            # Because we are using make_batch_reader(), each read returns a batch of rows instead of a single row
            batched_sample = sess.run(tensor)
            print("id batch: {0}".format(batched_sample.id))

    # Example: use tf.data.Dataset API
    with make_batch_reader(dataset_url) as reader:
        dataset = make_petastorm_dataset(reader)
        iterator = dataset.make_one_shot_iterator()
        tensor = iterator.get_next()
        with tf.Session() as sess:
            batched_sample = sess.run(tensor)
            print("id batch: {0}".format(batched_sample.id))


if __name__ == '__main__':
    tensorflow_hello_world()
