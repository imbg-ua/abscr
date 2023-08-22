import numpy as np
import math

def moving_average(array, num_avg):
    '''
    Smoothes numerical 1D array applying moving average methods.

        Parameters:
            array (np.ndarray): array of numerical data
            num_avg (int): number of following elements to calculate average (moving average parameter)

        Returns:
            res (np.ndarray): array of smoothed data
    '''
    res = []
    # array_extended = array + array[:num_avg - 1]
    array_extended = np.append(array, array[:num_avg - 1])
    for i in range(len(array)):
        res.append(sum(array_extended[i:i + num_avg]) / num_avg)
    return np.array(res)

def scale_outlines(outlines_file, factor):
    '''
    Scales outlines read from a .txt file with a given factor.

        Parameters:
            outlines_file (str): path to a file containing mask outlines
            factor (int): scaling factor

        Returns:
            outlines_scaled (list): list of scaled outlines
    '''
    outlines_scaled = []

    with open(outlines_file) as f:
        outlines = f.readlines()
        for o in outlines:
            coords_flat = np.fromstring(o, sep=',').astype(int)
            outlines_scaled.append(coords_flat * factor)

    outlines_scaled = np.array(outlines_scaled, dtype=object)
    return outlines_scaled

def scale_outlines_from_array(outlines, factor):
    '''
    Scales outlines read from a list with a given factor.

        Parameters:
            outlines (list-like): outlines
            factor (int): scaling factor

        Returns:
            outlines_scaled (list): list of scaled outlines
    '''
    outlines_scaled = []

    for coords_flat in outlines:
        outlines_scaled.append(coords_flat * factor)

    outlines_scaled = np.array(outlines_scaled, dtype=object)
    return outlines_scaled

def save_outlines_to_txt(outlines, savename):
    '''
    Saves array of outlines into a file

        Parameters:
            outlines (list-like): outlines
            savename (str): file name
    '''
    with open(savename, 'w') as f:
        for o in outlines:
            f.write(','.join(map(lambda x: str(x), o)) + '\n')

def smooth_outlines_moving_avg(outlines_file, num_avg=5):
    '''
    Smoothes outlines stored in a .txt file using moving average technique.

        Parameters:
            outlines_file (str): path to a file containing mask outlines
            num_avg (int): moving average parameter

        Returns:
            smoothed (list): list of smoothed outlines
    '''
    smoothed = []
    with open(outlines_file, 'r') as f:
        outlines = f.readlines()
        for o in outlines:
            coords_flat = np.fromstring(o, sep=',').astype(int)
            coords_flat[::2] = moving_average(coords_flat[::2], num_avg)
            coords_flat[1::2] = moving_average(coords_flat[1::2], num_avg)
            smoothed.append(coords_flat)
    return smoothed

def smooth_outlines_moving_avg_from_array(outlines, num_avg=5):
    '''
    Smoothes outlines stored in list using moving average technique.

        Parameters:
            outlines (list-like): outlines
            num_avg (int): moving average parameter

        Returns:
            smoothed (list): list of smoothed outlines
    '''
    smoothed = []
    for coords_flat in outlines:
        coords_flat[::2] = moving_average(coords_flat[::2], num_avg)
        coords_flat[1::2] = moving_average(coords_flat[1::2], num_avg)
        smoothed.append(coords_flat)
    return smoothed

def iterative_scaling_moving_avg(outlines_file, num_avg=5, factor=8, scale_step=2):
    '''
    Iteratively scales outlines read from a .txt file by alternating smoothing and scaling steps.
    Provided parameters factor and scale_step must satisfy the requirement that log_{scale_step}(factor) is an integer.

        Parameters:
            outlines_file (str): path to a file containing mask outlines
            num_avg (int): moving average parameter
            factor (int): total scaling factor
            scale_step (int): size of a single scaling step

        Returns:
            smoothed (list): list of smoothed outlines
    '''
    num_iter = math.log(factor, scale_step)
    assert num_iter % 1 == .0, 'Iterative scaling requires an integer number of scaling steps'

    smoothed = smooth_outlines_moving_avg(outlines_file, num_avg)
    for i in range(1, int(num_iter) + 1):
        scaled = scale_outlines_from_array(smoothed, 2)
        smoothed = smooth_outlines_moving_avg_from_array(scaled)

    return smoothed

def iterative_scaling_moving_avg_from_array(outlines, num_avg=5, factor=8, scale_step=2):
    '''
    Iteratively scales outlines stored in a list by alternating smoothing and scaling steps.
    Provided parameters factor and scale_step must satisfy the requirement that log_{scale_step}(factor) is an integer.

        Parameters:
            outlines_file (str): path to a file containing mask outlines
            num_avg (int): moving average parameter
            factor (int): total scaling factor
            scale_step (int): size of a single scaling step

        Returns:
            smoothed (list): list of smoothed outlines
    '''
    num_iter = math.log(factor, scale_step)
    print(num_iter % 1)
    assert num_iter % 1 == .0, 'Iterative scaling requires an integer number of scaling steps'

    smoothed = smooth_outlines_moving_avg_from_array(outlines, num_avg)
    for i in range(1, int(num_iter) + 1):
        scaled = scale_outlines_from_array(smoothed, 2)
        smoothed = smooth_outlines_moving_avg_from_array(scaled)

    return smoothed
