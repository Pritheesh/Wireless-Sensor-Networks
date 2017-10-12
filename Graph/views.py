import operator

from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
import json
import numpy as np
import timeit
import math

N = 2000
degree = 32
R = math.sqrt(degree / (N * math.pi))
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


def determine_adj_list(cells, points_dict, max_index):
    edges = 0
    degree_dict = dict()
    adj_list = [[0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]
    for cell_key in range(0, max_index + 1):
        for i in adj_list:
            cell = cell_key + i[0] * blocks + i[1]
            if 0 <= cell < blocks_square and cells.get(cell_key) is not None:
                for key1 in cells.get(cell_key):
                    point1 = points_dict[key1]
                    if cells.get(cell) is not None:
                        for key2 in cells.get(cell):
                            point2 = points_dict[key2][0]
                            if abs(point1[0][0] - point2[0]) < R and key1 != key2 and int(key2) not in point1:
                                distance = (point1[0][0] - point2[0]) ** 2 + (point1[0][1] - point2[1]) ** 2
                                if distance <= dist_square:
                                    check = points_dict.get(key2)
                                    if int(key1) not in check:
                                        degree_dict[key1] = degree_dict.get(key1, 0) + 1
                                        degree_dict[key2] = degree_dict.get(key2, 0) + 1
                                        points_dict.get(key1).append(int(key2))
                                        edges += 1
                    degree_dict.setdefault(key1, 0)
                    # print(key)
    return edges, degree_dict


def generate_points_for_square(num):
    x = np.random.uniform(0, 1, num)
    y = np.random.uniform(0, 1, num)
    nums = map(str, range(num + 1))
    points = map(list, zip(x, y))
    points = [[x] for x in points]
    points_dict = dict(zip(nums, points))
    return points_dict


def calculate_min_max(degree_dict):
    for_min = 9999999
    for_max = 0
    sum1 = 0
    min_max = dict()

    for item in degree_dict.items():
        deg = item[1]
        sum1 += deg
        if deg > for_max:
            for_max = deg
            min_max["max"] = int(item[0])
        if deg < for_min:
            for_min = deg
            min_max["min"] = int(item[0])

    avg = sum1 / N

    return for_min, for_max, avg, min_max


def set_adjacency_list(adj_dict, min_max):
    min_list = [int(key) for key, value in adj_dict.items() if min_max["min"] in value]
    adj_dict[str(min_max["min"])].extend(min_list)
    max_list = [int(key) for key, value in adj_dict.items() if min_max["max"] in value]
    adj_dict[str(min_max["max"])].extend(max_list)


def get_points(request):
    start = timeit.default_timer()
    points_dict = generate_points_for_square(N)
    cell_dict, max_index = assign_point_to_cell(points_dict)
    # print(len(cell_dict))
    edges, degree_dict = determine_adj_list(cell_dict, points_dict, max_index)
    for_min, for_max, avg, min_max = calculate_min_max(degree_dict)
    set_adjacency_list(points_dict, min_max)
    min_max = json.dumps(min_max)
    points_dict = json.dumps(points_dict)
    print("Max degree: ", for_max)
    print("Min degree: ", for_min)
    print("Average degree: ", avg)
    print("Edges: ", edges)
    stop = timeit.default_timer()
    print("Time taken: ", stop - start)
    # print(degree_dict)
    # for point in points_dict.items():
    #     print(point)

    # return render(request, 'plot.html')
    return render(request, 'plot.html', {'adj_dict': points_dict, 'min_max': min_max})
