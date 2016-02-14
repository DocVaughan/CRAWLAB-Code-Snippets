# coding: utf-8
import numpy as np

error_array = np.linspace(-5,5,501)

for error in error_array:
    print("Error: {}".format(error))


for index, error in enumerate(error_array):
    print("\nindex : {}".format(index))
    print("Error: {}".format(error))