"""
COMP 614
Homework 1: Circles
"""

import math
import comp614_module1 as circles


def distance(point0x, point0y, point1x, point1y):
    """
    Given the x- and y-coordinates of two points, computes and returns the 
    distance between them.
    """
    return math.sqrt((point1x - point0x)**2 + (point1y - point0y)**2)


def midpoint(point0x, point0y, point1x, point1y):
    """
    Given the x- and y-coordinates of two points, computes and returns the
    midpoint of the line segment between them.
    """
    x_point =  ((point1x + point0x ) / 2)
    y_point =  ((point1y + point0y) / 2)
    return x_point, y_point


def slope(point0x, point0y, point1x, point1y):
    """
    Given the x- and y-coordinates of two points, computes and returns the
    slope of the line segment from (point0x, point0y) to (point1x, point1y).
    """
    return (point1y - point0y) / (point1x - point0x)


def perp(lineslope):
    """
    Given the slope of a line, computes and returns the slope of a line 
    perpendicular to the input slope.
    """
    return -1/lineslope


def intersect(slope0, point0x, point0y, slope1, point1x, point1y):
    """
    Given two lines, where each is represented by its slope and a point
    that it passes through, computes and returns the intersection point
    of the two lines. 
    """
    x_point = ((slope0 * point0x) - (slope1 * point1x) + (point1y - point0y)) / (slope0 - slope1)
    y_point = (slope0 * (x_point - point0x)) + point0y
    return x_point, y_point


def make_circle(point0x, point0y, point1x, point1y, point2x, point2y):
    """
    Given the x- and y-coordinates of three points, computes and returns
    three real numbers: the x- and y-coordinates of the center of the circle
    that passes through all three input points, and the radius of that circle.
    """
    slope0 = slope(point0x, point0y, point1x, point1y)
    x_midpoint0, y_midpoint0 = midpoint(point0x, point0y, point1x, point1y)
    perp0 = perp(slope0)

    slope1 = slope(point0x, point0y, point2x, point2y)
    x_midpoint1, y_midpoint1 = midpoint(point0x, point0y, point2x, point2y)
    perp1 = perp(slope1)

    x_mid,y_mid=intersect(perp0,x_midpoint0,y_midpoint0,perp1,x_midpoint1,y_midpoint1)

    radius = distance(x_mid, y_mid, point0x, point0y)
    return x_mid, y_mid, radius


# Run GUI - uncomment the line below after you have
#           implemented make_circle
circles.start(make_circle)

