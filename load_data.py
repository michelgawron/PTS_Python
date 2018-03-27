def load_file(path: str) -> list:
    """
    Load the file containing our stations
    :param path: The path of metro.gr
    :return: A list containing lines from our file
    """
    with open(path) as f:
        lines = f.read().split("\n")
    return lines


def get_data_to_dict(mylist):
    """
    Get data from the list and store it in dictionaries using an integer to iterate over it
    :param mylist: List containing lines from metro.gr
    :return:
    """

    # Getting height and width from the file and converting it to integer
    height, width = map(lambda x: int(x), mylist[0].split(" "))

    # Now we are going to get station names, which is the first part of this file, and store it in a dictionary
    i = 2
    dict_station_names = {}
    while mylist[i] != "coord sommets":
        # Getting station id by splitting up the string and taking the first element
        # Station name is
        idStation = int(mylist[i].split(" ")[0])
        nameStation = " ".join(mylist[i].split(" ")[1:])
        dict_station_names[idStation] = nameStation

        i += 1

    i += 1
    # We are now going to get coordinates for our stations and store it in a dictionary
    dict_station_coordinates = {}
    while mylist[i] != "arcs values":
        # Getting coordinates and converting it to integers
        idStation = int(mylist[i].split(" ")[0])
        stationCoordinates = list(map(lambda x: int(x), mylist[i].split(" ")[1:]))
        dict_station_coordinates[idStation] = stationCoordinates

        i += 1

    # And finally, we iterate until the end of the file in order to get arcs
    # We are going to store them as dictionaries inside a dictionary as follows:
    # dict = {idStationFrom1: {idStationTo1: distance, idStationTo2: distance}, idStationFrom2: {idStationTo3: distance}}
    i += 1
    dict_station_distance = {}
    while i < len(mylist):
        # Getting ids and distance and adding them to the dictionary
        idFrom, idTo, distance = map(lambda x: int(float(x)), mylist[i].split(" "))
        try:
            dict_station_distance[idFrom][idTo] = distance
        except KeyError:
            # If we got no distance for the station idFrom yet, then creating a sub dictionary and filling it
            dict_station_distance[idFrom] = {}
            dict_station_distance[idFrom][idTo] = distance
        i += 1
    return [height, width, dict_station_names, dict_station_coordinates, dict_station_distance]




def draw_subway(height, width, coordinates, distances, path=[], file_name="subway.svg"):
    """
    This functions draws our stations and arcs from our lists
    """
    import svgwrite

    # Create a drawing
    mydrawing = svgwrite.Drawing(filename=file_name, size=(width, height))

    # Get the list of lines to draw from the distance dictionary and drawing lines
    # Our dictionary has the following pattern:
    # dict = {idStationFrom1: {idStationTo1: distance, idStationTo2: distance}, idStationFrom2: {idStationTo3: distance}}
    for keyFrom, values in distances.items():
        # First we get the coordinates of the origin point
        x1, y1 = coordinates[keyFrom]
        for keyTo in values:
            # Then we get the coordinates of the end points and we draw the lines
            x2, y2 = coordinates[keyTo]
            mydrawing.add(
                mydrawing.line(start=(x1, height - y1), end=(x2, height - y2), stroke="black", stroke_width="2"))

    # Getting coordinates of each station and drawing circles for them
    for key, values in coordinates.items():
        mydrawing.add(mydrawing.circle(center=(values[0], height - values[1]), r=2.5, fill="white", stroke="blue"))

    i = 0
    for i in range(len(path) - 1):
        x1, y1 = coordinates[path[i]]
        x2, y2 = coordinates[path[i + 1]]
        mydrawing.add(mydrawing.line(start=(x1, height - y1), end=(x2, height - y2), stroke="red", stroke_width="2"))

    for i in range(len(path)):
        x1, y1 = coordinates[path[i]]
        mydrawing.add(mydrawing.circle(center=(x1, height-y1), r=2.5, fill="white", stroke="red"))

    # Saving the svg file
    mydrawing.save()


draw_subway(750, 750, coordinates, distances)


def dijkstra(subwayGraph, start, end, visitedStations=[], distances={}, predecessors={}):
    """
        Recursively computes the shortest path using dijkstra algorithm
        :param subwayGraph: Graph containing distances between each station
        :param start: Id of the starting station (this parameter changes when we recurse)
        :param end: Id of the ending station
        :param visitedStations: List containing all visited stations
        :param distances: Shortest distances found for the nodes from our first starting point
        :param predecessors: Dictionary containing the predecessor node with the lowest distance
        :return:
    """
    # Checking that stations exist
    if start not in subwayGraph or end not in subwayGraph:
        return

    # Return condition - if we reach our station
    if start == end:
        # We build the shortest path by getting predecessors of each node
        path = []
        pred = end
        while pred != None:
            path.append(pred)
            pred = predecessors.get(pred, None)
        return [path, distances[end]]
    else:
        # If this is the first execution of the algorithm, initializing our distance to 0
        if not visitedStations:
            distances[start] = 0

        # Visiting neighbors that hasn't been visited yet (on this run or previous ones)
        for neighbor in subwayGraph[start]:
            if neighbor not in visitedStations:
                # Computing distance from this run's starting point to the first starting point for each neighbor
                new_distance = distances[start] + subwayGraph[start][neighbor]
                # If there is no distance or if the distance found for this neighbor is shortest than a previous one,
                # storing it and setting this run's starting point as a predecessor for this neighbor
                if new_distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = start

        # Mark this node as visited
        visitedStations.append(start)

        # No that we visited all neighbors, getting nearest non visited station and recursively running dijkstra with
        # This station as a starting point
        unvisited = {}
        for k in subwayGraph:
            if k not in visitedStations:
                unvisited[k] = distances.get(k, float('inf'))
        x = min(unvisited, key=unvisited.get)
        return dijkstra(subwayGraph, x, end, visitedStations, distances, predecessors)



