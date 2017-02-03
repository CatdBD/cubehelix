#!/opt/local/bin/python

import math

import numpy

_recipe_list = {'september_issue': {
                    'start_color': 2.0,
                    'rotations': 1.5},
                'red': {
                    'start_color': 1.0,
                    'rotations': 0.},
                'green': {
                    'start_color': 2.0,
                    'rotations': 0},
                'blue': {
                    'start_color': 3.0,
                    'rotations': 0},
                'tim': {
                    'start_color': 1.3,
                    'rotations': -0.9},
                'cat': {
                    'start_color': 0.5,
                    'rotations': 2.3}}

def compute_transform(intensity, start_color, rotations, hue, gamma):
    # Define transform scalars
    phi = 2. * math.pi * (start_color / 3. + rotations * intensity)
    amp = hue * intensity**gamma * (1. - intensity**gamma) / 2.

    # Define transform vectors/matrices
    offset_vector = numpy.array([intensity**gamma] * 3)
    transform_matrix = numpy.array([[-0.14861, +1.78277],
                                    [-0.29227, -0.90649],
                                    [+1.97249, +0.00000]])
    rotation_vector = numpy.array([math.cos(phi), math.sin(phi)])

    # Perform transformation
    transformed_color = offset_vector + amp * numpy.dot(transform_matrix, rotation_vector)

    # Clip returned results to [0, 1]
    return numpy.clip(transformed_color, 0., 1.)


def make_rgb_list(start_color, rotations, hue, gamma, N, reverse):
        # Clip some of the passed values into ranges that make sense.
    start_color = numpy.clip(start_color, 0., 3.)
    N = numpy.clip(N, 1, 2**10)

    # Create list from the cubehelix transform with N quantizations
    color_list = numpy.array([compute_transform(x / (N - 1.), start_color, rotations, hue, gamma) for x in xrange(N)])

    # Reverse the color list if requested
    if reverse:
        color_list = color_list[::-1]

    return color_list


def make_lut(start_color=0.5, rotations=-1.5, hue=1.0, gamma=1.0, N=256, reverse=False):
    color_list = make_rgb_list(start_color, rotations, hue, gamma, N, reverse)

    # Convert to 256 division RGBA list with opaque alpha channel
    color_list = 255 * numpy.insert(color_list, 3, 1., axis=1)

    # Convert to a list of integers and return
    return color_list.astype(numpy.uint8)


def make_cmap(start_color=0.5, rotations=-1.5, hue=1.0, gamma=1.0, N=256, reverse=False):
    color_list = make_rgb_list(start_color, rotations, hue, gamma, N, reverse)

    try:
        import matplotlib
    except ImportError:
        # If matplotlib is not available print about its absence and return the color_list
        print 'matplotlib package not found, returning rgb_list instead of colormap.'
        return color_list
    else:
        # Create and return the corresponding cmap
        return matplotlib.colors.ListedColormap(color_list)


def get_cmap(name='default', reverse=False):
    recipe = _recipe_list.get(name.lower(), {})
    return make_cmap(reverse=reverse, **recipe)


def get_lut(name='default', reverse=False):
    recipe = _recipe_list.get(name.lower(), {})
    return make_lut(reverse=reverse, **recipe)
