#!/usr/bin/env python
# coding: utf-8

import numpy as np
import deeppy as dp


def preprocess_imgs(imgs):
    imgs = imgs.astype(dp.float_)
    imgs -= np.mean(imgs, axis=0, keepdims=True)
    return imgs


def run():
    # Prepare data
    dataset = dp.dataset.CIFAR10()
    x, y = dataset.data()
    x = x.astype(dp.float_)
    y = y.astype(dp.int_)
    train_idx, test_idx = dataset.split()
    x_train = x[train_idx]
    y_train = y[train_idx]

    batch_size = 128
    train_input = dp.SupervisedInput(x_train, y_train, batch_size=batch_size)

    # Setup neural network
    pool_kwargs = {
        'win_shape': (3, 3),
        'strides': (2, 2),
        'border_mode': 'same',
        'method': 'max',
    }
    net = dp.NeuralNetwork(
        layers=[
            dp.Convolution(
                n_filters=32,
                filter_shape=(5, 5),
                border_mode='same',
                weights=dp.Parameter(dp.NormalFiller(sigma=0.0001),
                                     weight_decay=0.004),
            ),
            dp.Activation('relu'),
            dp.Pool(**pool_kwargs),
            dp.Convolution(
                n_filters=32,
                filter_shape=(5, 5),
                border_mode='same',
                weights=dp.Parameter(dp.NormalFiller(sigma=0.01),
                                     weight_decay=0.004),
            ),
            dp.Activation('relu'),
            dp.Pool(**pool_kwargs),
            dp.Convolution(
                n_filters=64,
                filter_shape=(5, 5),
                border_mode='same',
                weights=dp.Parameter(dp.NormalFiller(sigma=0.01),
                                     weight_decay=0.004),
            ),
            dp.Activation('relu'),
            dp.Pool(**pool_kwargs),
            dp.Flatten(),
            dp.FullyConnected(
                n_out=64,
                weights=dp.Parameter(dp.NormalFiller(sigma=0.1),
                                     weight_decay=0.004),
            ),
            dp.Activation('relu'),
            dp.FullyConnected(
                n_out=dataset.n_classes,
                weights=dp.Parameter(dp.NormalFiller(sigma=0.1),
                                     weight_decay=0.004),
            ),
        ],
        loss=dp.MultinomialLogReg(),
    )

    dp.misc.profile(net, train_input)


if __name__ == '__main__':
    run()
