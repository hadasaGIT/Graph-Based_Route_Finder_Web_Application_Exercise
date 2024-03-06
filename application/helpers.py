import ast
# import json
import math
import os
from heapq import heappush, heappop
import simplekml

# Read the JSON file and convert it to a data structure in Python
# with open('../graph_example.json', 'r') as file:
#     graph_data = json.load(file)


def haversine(coord1, coord2):
    """
       Calculate the distance between two points using the Haversine formula.

       :param coord1: The coordinates of the first point (longitude, latitude).
       :param coord2: The coordinates of the second point (longitude, latitude).

       :return: The distance in kilometers between the two points.
    """
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    # Check the validity of the input coordinates
    if not (-180 <= lon1 <= 180) or not (-90 <= lat1 <= 90) or not (-180 <= lon2 <= 180) or not (-90 <= lat2 <= 90):
        raise ValueError("Invalid coordinates")

    # Convert coordinates from degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Calculate differences in longitude and latitude
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Apply Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of the Earth in kilometers
    return c * r


def find_closest_point(coord, graph):
    """
    Find the closest node to a given point in the graph.

    :param coord: The coordinates of the point (longitude, latitude).
    :param graph: The data structure representing the graph.

    :return: The closest node to the given point.
    """
    min_distance = float('inf')
    closest_point = None
    for point, neighbors in graph.items():
        # Calculate the distance from the given point to the current point
        distance = haversine(coord, point)
        # Check if this distance is the smallest found so far
        if distance < min_distance:
            min_distance = distance
            closest_point = point
        # For each neighboring node, check its distance from the given point
        for neighbor in neighbors:
            neighbor_distance = haversine(coord, neighbor)
            if neighbor_distance < min_distance:
                min_distance = neighbor_distance
                closest_point = neighbor

    if type(closest_point) is list:
        return tuple(closest_point)

    return closest_point


def dijkstra(graph, start, end):
    """
    Find the shortest path between two points in a graph using Dijkstra's algorithm.

    :param graph: The graph (dictionary) where relationships between nodes are defined.
    :param start: The node from which the search will begin.
    :param end: The node where the search will end.

    :return: The shortest path between the two points (a list of nodes).
    """
    # Initialize the priority queue with the start node and an empty path
    queue = [(0, start, [])]
    visited = set()
    while queue:
        # Pop the node with the lowest cost from the queue
        (cost, node, path) = heappop(queue)
        if type(node) is list:
            node = tuple(node)
        if node not in visited:
            visited.add(node)
            path = path + [node]
            if node == end:
                return path
            if node in graph.keys():
                # Explore neighbors of the current node
                for neighbor in graph[node]:
                    neighbor_cost = cost + haversine(node, neighbor)
                    heappush(queue, (neighbor_cost, neighbor, path))
    return []


def shortest_path(start_coord, end_coord, graph):
    """
    Calculate the shortest path between two points on a map.

    :param start_coord: The coordinates of the starting point, in the format (latitude, longitude).
    :param end_coord: The coordinates of the destination point, in the format (latitude, longitude).
    :param graph: A data structure representing the graph, containing coordinates and neighbors for each point.

    :return list: A list of coordinates of the shortest path between the points, in the format (latitude, longitude).
    """
    new_graph = {tuple(ast.literal_eval(key)): value for key, value in graph.items()}

    # Find the closest coordinates to the start and end points
    start_point = find_closest_point(start_coord, new_graph)
    end_point = find_closest_point(end_coord, new_graph)
    # Calculate the shortest path between the points
    shortest_path_coords = dijkstra(new_graph, start_point, end_point)
    # shortest_path = [point for point in shortest_path_coords]

    return shortest_path_coords


def generate_kml(coords_path):
    """
    Generate a KML file representing the shortest path.

    :param coords_path: A list of coordinates representing the shortest path, in the format [(latitude1, longitude1),...].

    :return str: The file path of the generated KML file.
    """

    kml = simplekml.Kml()

    # Create a path in KML
    line = kml.newlinestring(name="Shortest Path")
    line.coords = coords_path

    # Save the KML to a file
    kml_file_path = os.path.abspath("shortest_path.kml")
    kml.save(kml_file_path)

    return kml_file_path


# if __name__ == '__main__':
#     # example
    # start_coord = (30.05, 34.69)
    # end_coord = (30.12, 34.32)
    # path = shortest_path(start_coord, end_coord, graph_data)
    # print("Shortest path:", path)
