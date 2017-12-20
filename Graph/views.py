import copy
import csv
import heapq
import operator
from collections import Counter
from queue import Queue

import pandas as pd
import xlsxwriter
import xlwt
from django.shortcuts import render, render_to_response

# Create your views here.
import json
import numpy as np
import timeit
import math

from django.template.context_processors import csrf

from Graph.forms import InputForm

# N = 8000
# degree = 64
# arr_x = []


def assign_point_to_cell(xy, R, blocks):
    my_dict = dict()
    count = 0
    for key in xy.keys():
        point = xy[key]
        column = math.ceil(point[0] / R)
        row = math.ceil(point[1] / R)
        block = int((row - 1) * blocks + (column - 1))
        if block > count:
            count = block
        my_dict.setdefault(block, []).append(key)
    return my_dict, count


def iterate_cells(cells, points_dict, degree_dict, cell, cell_key, edges, dist_square, R, adj_list):
    for key1 in cells.get(cell_key):
        point1 = points_dict[key1]
        # adj_list[key1] = []
        for key2 in cells.get(cell):
            point2 = points_dict[key2]
            if abs(point1[0] - point2[0]) < R and key1 != key2 and int(key2) not in adj_list.get(key1, []):
                distance = (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2
                if distance <= dist_square and int(key1) not in points_dict.get(key2):
                    adj_list[key1].append(int(key2))
                    adj_list[key2].append(int(key1))
                    degree_dict[key1] = degree_dict.get(key1, 0) + 1
                    degree_dict[key2] = degree_dict.get(key2, 0) + 1
                    edges += 1
        degree_dict.setdefault(key1, 0)
    return edges


def determine_adj_list(cells, points_dict, max_index, blocks, R, adj_list):
    edges = 0
    blocks_square = blocks ** 2
    dist_square = R ** 2
    degree_dict = dict()
    for_adj = [[0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]
    for cell_key in range(0, max_index + 1):
        for i in for_adj:
            cell = cell_key + i[0] * blocks + i[1]
            if 0 <= cell < blocks_square and cells.get(cell) is not None and cells.get(cell_key) is not None:
                edges = iterate_cells(cells, points_dict, degree_dict, cell, cell_key,
                                      edges, dist_square, R, adj_list)

    return edges, degree_dict


def generate_points_for_square(num, degree):
    R = np.sqrt(degree/(num * np.pi))
    blocks = math.ceil(1/R)
    x = np.random.uniform(0, 1, num)
    y = np.random.uniform(0, 1, num)
    nums = map(str, range(num + 1))
    points = map(list, zip(x, y))
    # points = [x for x in points]
    points_dict = dict(zip(nums, points))
    return R, blocks, points_dict


def generate_points_for_circle(num, degree):
    R = np.sqrt(degree/num)
    blocks = math.ceil(2 / R)
    r = np.sqrt(np.random.uniform(0, 1, num))
    theta = 2 * np.pi * np.random.uniform(0, 2, num)
    x = 1 + r * np.cos(theta)
    y = 1 + r * np.sin(theta)
    nums = map(str, range(num + 1))
    points = map(list, zip(x, y))
    # points = [[x] for x in points]
    points_dict = dict(zip(nums, points))
    return R, blocks, points_dict


def calculate_min_max(degree_dict, nodes):
    for_min = min(degree_dict.items(), key=lambda x: x[1])
    for_max = max(degree_dict.items(), key=lambda x: x[1])
    avg = sum(degree_dict.values()) / nodes
    all_maxes = [k for k, v in degree_dict.items() if v == for_max[1]]
    all_mins = [k for k, v in degree_dict.items() if v == for_min[1]]
    min_max = dict()
    min_max["max"] = []
    for node in all_maxes:
        min_max["max"].append(int(node))
    min_max["min"] = []
    for node in all_mins:
        min_max["min"].append(int(node))
    return for_min[1], for_max[1], avg, min_max

#
#
# def set_adjacency_list(adj_dict, min_max):
#     for node in min_max["min"]:
#         min_list = [int(key) for key, value in adj_dict.items() if node in value]
#         adj_dict[str(node)].extend(min_list)
#     for node in min_max["max"]:
#         max_list = [int(key) for key, value in adj_dict.items() if node in value]
#         adj_dict[str(node)].extend(max_list)


def generate_csv(degree_dict):
    variable = Counter(degree_dict.values())
    print(variable)
    book = xlwt.Workbook(encoding='utf-8')
    sheet1 = book.add_sheet("Sheet1")
    i = 0
    for var in variable.items():
        sheet1.write(i, 0, var[0])
        sheet1.write(i, 1, var[1])
        i += 1
    book.save("degree_distri2.xls")


def form_view(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            nodes = form.cleaned_data.get('nodes')
            degree = form.cleaned_data.get('degree')
            topology = form.cleaned_data.get('topology')
            points, adj_list, min_max, edges, for_max, for_min, avg, rad, color, num_colors, tuple1 = \
                get_points(int(nodes), int(degree), int(topology))

            backbone1_edges = tuple1[0]
            backbone2_edges = tuple1[1]

            backbone1_vertices = tuple1[2]
            backbone2_vertices = tuple1[3]

            backbone1 = tuple1[4]
            backbone2 = tuple1[5]

            domination1 = tuple1[6][0]
            domination2 = tuple1[6][1]

            context = {
                'form'              : form,
                'points'            : points,
                'adj_list'          : adj_list,
                'min_max'           : min_max,
                'for_max'           : for_max,
                'for_min'           : for_min,
                'edges'             : edges,
                "avg"               : avg,
                'radius'            : rad,
                "color"             : color,
                'num_colors'        : num_colors,
                'backbone1_edges'   : backbone1_edges,
                'backbone2_edges'   : backbone2_edges,
                'backbone1_vertices': backbone1_vertices,
                'backbone2_vertices': backbone2_vertices,
                'backbone1'         : backbone1,
                'backbone2'         : backbone2,
                'domination1'       : domination1,
                'domination2'       : domination2,
                # 'nodes': nodes,
                # 'degree': degree,
                # 'topology': topology
            }
            context.update(csrf(request))
            return render_to_response('plot.html', context=context)

    form = InputForm()
    context = dict()
    context['form'] = form
    context.update(csrf(request))
    return render(request, 'plot.html', context=context)


# def smallest_last_order(points_dict, degree_dict):
#     order = []
#     copy_of_degree = {k: v for k, v in degree_dict.items()}
#     while len(copy_of_degree) != 0:
#         min_degree_point = min(copy_of_degree.items(), key=lambda x: x[1])
#         for point in points_dict[min_degree_point[0]][1:]:
#             if str(point) in copy_of_degree:
#                 copy_of_degree[str(point)] -= 1
#         order.append(min_degree_point[0])
#         del copy_of_degree[min_degree_point[0]]
#     return order


def generate_random_color():
    r = np.random.random_integers(50, 250)
    g = np.random.random_integers(50, 250)
    b = np.random.random_integers(50, 250)
    return r, g, b


def get_value(color_list):
    if len(color_list) == 0:
        return 0
    for i in range(max(color_list) + 1):
        if i not in color_list:
            return i
    return max(color_list) + 1


def allot(point, points_dict, color_dict):
    color_list = []
    for adj in points_dict[point]:
        adj = str(adj)
        if adj in color_dict.keys():
            color_list.append(color_dict[adj])
    color_list = sorted(list(set(color_list)))
    # print(color_list)
    # return get_value(color_list)
    return next(i for i, e in enumerate(color_list + [None], 0) if i != e)


def find_color(order, points_dict):
    temp = dict()
    color_list = []
    color_dict = dict()
    # color_dict2 = dict()
    color_count = dict()
    while order:
        point = order.pop()
        next_val = allot(point, points_dict, temp)
        if next_val >= len(color_list):
            color_list.append(generate_random_color())
        temp[point] = next_val
        color_dict[point] = color_list[next_val]
        color_count[color_list[next_val]] = color_count.get(color_list[next_val], 0) + 1

    # print(points_dict)
    # print(temp)
    # print(color_dict)
    print("Max color class: ", max(v for v in color_count.values()))
    # book = xlsxwriter.Workbook("color_class2.xlsx")
    # sheet1 = book.add_worksheet("Sheet1")
    # sheet1.write(0, 0, 'Color')
    # sheet1.write(0, 1, 'Count')
    # i = 1
    # for col, count in color_count.items():
    #     sheet1.write(i, 0, i)
    #     sheet1.write(i, 1, count)
    #     i += 1
    # book.save("degree2.xlsx")
    max_four = {k: v for k, v in color_count.items() if v in heapq.nlargest(4, color_count.values())}
    max_four = sorted(max_four.items(), key=lambda x: x[1], reverse=True)[:4]
    max_four = {i: j for (i, j) in max_four}
    return max_four, color_dict, len(color_list)


def decrease_degree(copy_points, copy_temp, point, degree_dict):
    if point in copy_points.keys():
        adj = copy_points[point]
        for i in adj:
            i = str(i)
            copy_points[i].remove(int(point))
            degree = degree_dict[i]
            copy_temp[degree].remove(i)
            if not copy_temp[degree]:
                del copy_temp[degree]
            degree_dict[i] -= 1
            copy_temp.setdefault(degree_dict[i], []).append(i)


def write_excel(min_degree_list, avg_degree_list, original_degree_list):
    book = xlsxwriter.Workbook("sequential_ordering2.xlsx")
    sheet1 = book.add_worksheet("Sheet1")
    i = 1
    sheet1.write(0, 0, '#')
    sheet1.write(0, 1, 'Minimum')
    sheet1.write(0, 2, 'Average')
    sheet1.write(0, 3, 'Original')

    for min1, avg, org in zip(min_degree_list, avg_degree_list, original_degree_list):
        sheet1.write(i, 0, i)
        sheet1.write(i, 1, min1)
        sheet1.write(i, 2, avg)
        sheet1.write(i, 3, org)
        i += 1
    # book.save("plot2.xlsx")


# def get_degree_list(degree_dict, max_degree):
#     degree_list = [[] for _ in range(max_degree + 1)]
#     for key, value in degree_dict.items():
#         degree_list[value].append(key)
#     return degree_list
#
#
# def find_order(temp_dict, points_dict, degree_dict, avg):
#     order = []
#     temp = get_degree_list(degree_dict)

def get_avg_degree(copy_degree):
    return float(sum(copy_degree.values())) / len(copy_degree)


def find_order(temp_dict, adj_list, degree_dict, avg):
    order = []
    copy_temp = temp_dict
    # copy_degree = degree_dict
    # copy_temp = copy.deepcopy(temp_dict)
    copy_points = copy.deepcopy(adj_list)
    copy_degree = copy.deepcopy(degree_dict)
    min_degree_list = []
    avg_degree_list = []
    original_degree_list = []
    # counter2 = 0
    # time = 0
    flag = True
    while len(copy_points) != 0:
        min_degree_points = min(copy_temp.items(), key=lambda x: x[0])
        min_degree_list.append(min_degree_points[0])
        point = min_degree_points[1].pop()
        original_degree_list.append(degree_dict[point])
        if not min_degree_points[1]:
            del copy_temp[min_degree_points[0]]
        # start = timeit.default_timer()
        decrease_degree(copy_points, copy_temp, point, copy_degree)
        avg = get_avg_degree(copy_degree)
        avg_degree_list.append(avg)
        # stop = timeit.default_timer()
        # time += stop - start
        if len(temp_dict) == 1 and flag is True:
            print("Terminal clique size = ", len(list(temp_dict.values())[0]))
            flag = False
        del copy_points[point]
        order.append(point)
    # print(order)
    # print("Maximun class size: ", max(len())
    print("Max degree when deleted: ", max(min_degree_list))
    # print("Time for decrease degree: ", time)
    # write_excel(min_degree_list, avg_degree_list, original_degree_list)
    return order


def get_degree_dict(degree_dict):
    temp_dict = dict()
    for key, value in degree_dict.items():
        temp_dict.setdefault(value, []).append(key)
    return temp_dict


def get_dict(color, max_four):
    temp_dict = dict()
    for key, value in color.items():
        if value in max_four.keys():
            temp_dict.setdefault(value, []).append(key)
    return temp_dict


def connected_components(graph):
    visited = set()

    def component(n):
        nodes = {n}
        while nodes:
            n = nodes.pop()
            visited.add(n)
            nodes |= graph[n] - visited
            yield n
    for node in graph:
        if node not in visited:
            yield component(node)


# def BFS(list1, list2, adj_list):
#     combined = list1 + list2
#     visited = [False] * len(combined)
#     queue = list()
#     queue.append(combined[0])
#     visited[0] = True
#
#     while queue:
#         current = queue.pop(0)
#         for i in range(len(combined)):
#             if is_adj(combined[i], current, adj_list) and not visited[i]:
#                 visited[i] = True
#                 queue.append(combined[i])
#
#     return visited.count(True)

# def is_adj(vertex1, vertex2, adj_list):
#     return int(vertex1) in adj_list[vertex2]


def get_bipartite_adj_list(list1, list2, adj_list):
    combined = list1 + list2
    adj_list2 = dict()
    for i in combined:
        for neighbor in adj_list[i]:
            if str(neighbor) in combined:
                adj_list2.setdefault(i, []).append(str(neighbor))
    new_graph = {node: set(str(edge) for edge in edges) for node, edges in adj_list2.items()}
    components = []
    for component in connected_components(new_graph):
        c = set(component)
        components.append({key: adj_list2[key] for key in c})

    max_component = \
        max({components.index(comp): len(comp) for comp in components}.items(), key=operator.itemgetter(1))[0]
    bipartite_component = components[max_component]
    component_copy = copy.deepcopy(bipartite_component)

    while True:
        flag = True
        for node in component_copy:
            try:
                if len(bipartite_component[node]) < 2:
                    key = bipartite_component[node][0]
                    bipartite_component[key].remove(node)
                    bipartite_component.pop(node)
                    flag = False
            except Exception:
                pass
        if flag:
            break

    return bipartite_component


def backbone(color, adj_list, max_four, nodes):
    color_dict = get_dict(color, max_four)
    values = list(color_dict.values())
    bipartite_adj_list = []
    domination = []

    for i in range(4):
        for j in range(i+1, 4):
            bipartite_adj_list.append(get_bipartite_adj_list(values[i], values[j], adj_list))

    backbone_edge_count = {}
    for i in range(0, 6):
        size = len(bipartite_adj_list[i])
        backbone_edge_count[i] = size

    backbone_index = sorted(backbone_edge_count, key=backbone_edge_count.get, reverse=True)[:2]

    for index in range(0, 2):
        edges = set()
        for key in bipartite_adj_list[backbone_index[index]]:
            for edge in adj_list[key]:
                edges.add(edge)
            edges.add(int(key))
        domination.append(format((len(edges) / float(nodes)) * 100, '.2f'))

    backbone1_edges = sum([len(lst) for lst in bipartite_adj_list[backbone_index[0]].values()]) / 2
    backbone2_edges = sum([len(lst) for lst in bipartite_adj_list[backbone_index[1]].values()]) / 2

    backbone1_vertices = len(bipartite_adj_list[backbone_index[0]].keys())
    backbone2_vertices = len(bipartite_adj_list[backbone_index[1]].keys())

    backbone1 = json.dumps(bipartite_adj_list[backbone_index[0]])
    backbone2 = json.dumps(bipartite_adj_list[backbone_index[1]])

    return backbone1_edges, backbone2_edges, backbone1_vertices, backbone2_vertices, backbone1, backbone2, domination


def get_points(nodes, degree, topology):
    adj_list = {}
    for i in range(nodes):
        adj_list[str(i)] = []
    start1 = timeit.default_timer()
    if topology == 1:
        R, blocks, points = generate_points_for_square(nodes, degree)
        factor = 800
    else:
        R, blocks, points = generate_points_for_circle(nodes, degree)
        factor = 400

    cell_dict, max_index = assign_point_to_cell(points, R, blocks)
    edges, degree_dict = determine_adj_list(cell_dict, points, max_index, blocks, R, adj_list)
    for_min, for_max, avg, min_max = calculate_min_max(degree_dict, nodes)

    stop1 = timeit.default_timer()
    temp = get_degree_dict(degree_dict)
    # temp_list = get_degree_list(degree_dict, for_max)
    start2 = timeit.default_timer()
    order = find_order(temp, adj_list, degree_dict, avg)
    stop2 = timeit.default_timer()
    max_four, color, num_colors = find_color(order, adj_list)
    stop3 = timeit.default_timer()
    tuple1 = backbone(color, adj_list, max_four, nodes)
    stop4 = timeit.default_timer()
    # print("Time for order = ", stop2 - start2)
    # print("Time for color = ", stop3 - stop2)
    print("colors: ", num_colors)
    color = pd.Series(color).to_json()
    # set_adjacency_list(points_dict, min_max)
    min_max['factor'] = factor
    min_max = json.dumps(min_max)
    points = json.dumps(points)
    adj_list = json.dumps(adj_list)
    # color = json.dumps(color)
    # generate_csv(degree_dict)
    # print("Max degree: ", for_max)
    # print("Min degree: ", for_min)
    # print(min_max)
    # print("Average degree: ", avg)
    # print("Edges: ", edges)
    # stop = timeit.default_timer()
    print("Time taken for part1: ", stop1 - start1)
    print("Time taken for part2: ", stop2 - start2)
    print("Time taken for part3: ", stop4 - stop3)
    return points, adj_list, min_max, edges, for_max, for_min, avg, R, color, num_colors, tuple1

