import operator

from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
import json
import numpy as np
import timeit
import math

N = 4000
degree = 32
R = math.sqrt(degree/(N * math.pi))
blocks = math.ceil(1 / R)
blocks_square = blocks ** 2
dist_square = R ** 2
arr_x = []


def assign_point_to_cell(xy):
    my_dict = dict()
    count = 0
    for key in xy.keys():
        point = xy[key][0]
        column = math.ceil(point[0] / R)
        row = math.ceil(point[1] / R)
        block = int((row - 1) * blocks + (column - 1))
        if block > count:
            count = block
        my_dict.setdefault(block, []).append(key)
    return my_dict, count


def determine_adj_list(cells, points_dict1, max_index):
    edges = 0
    degree_dict = dict()
    for key in range(0, max_index+1):
        for i in range(0, 2):
            for j in range(-1, 2):
                cell = key + i * blocks + j
                if 0 <= cell < blocks_square and cells.get(key) is not None:
                    for key1 in cells.get(key):
                        # degree_dict[key1] = 0
                        point1 = points_dict1[key1]
                        if cells.get(cell) is not None:
                            for key2 in cells.get(cell):
                                point2 = points_dict1[key2][0]
                                if abs(point1[0][0] - point2[0]) < R and key1 != key2 and int(key2) not in point1:
                                    distance = (point1[0][0] - point2[0]) ** 2 + (point1[0][1] - point2[1]) ** 2
                                    if distance <= dist_square:
                                        check = points_dict1.get(key2)
                                        if int(key1) not in check:
                                            degree_dict[key1] = degree_dict.get(key1, 0) + 1
                                            degree_dict[key2] = degree_dict.get(key2, 0) + 1
                                            edges += 1
                                            points_dict1.get(key1).append(int(key2))
                        degree_dict.setdefault(key1, 0)
        # print(key)
    return points_dict1, edges, degree_dict


def get_points(request):
    start = timeit.default_timer()
    x = np.random.uniform(0, 1, N)
    y = np.random.uniform(0, 1, N)
    nums = map(str, range(N + 1))
    points = map(list, zip(x, y))
    points = [[x] for x in points]
    points_dict = dict(zip(nums, points))
    cell_dict, max_index = assign_point_to_cell(points_dict)
    # print(len(cell_dict))
    adj_dict, edges, degree_dict = determine_adj_list(cell_dict, points_dict, max_index)
    adj_dict = json.dumps(adj_dict)

    for_min = 9999999
    for_max = 0
    sum1 = 0
    min_max = dict()

    for degr in degree_dict.items():
        deg = degr[1]
        sum1 += deg
        if deg > for_max:
            for_max = deg
            min_max["max"] = int(degr[0])
        if deg < for_min:
            for_min = deg
            min_max["min"] = int(degr[0])
    min_max = json.dumps(min_max)

    print("Max degree: ", for_max)
    print("Min degree: ", for_min)
    # print("Average degree: ", edges/N)
    print("Average degree: ", sum1/N)
    print("Edges: ", edges)
    stop = timeit.default_timer()
    print("Time taken: ", stop-start)
    # print(degree_dict)
    # for point in points_dict.items():
    #     print(point)

    # return render(request, 'plot.html')
    return render(request, 'plot.html', {'adj_dict': adj_dict, 'min_max': min_max })
