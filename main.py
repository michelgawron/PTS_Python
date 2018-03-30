import load_data as ld
import argparse

h, w, names, coordinates, distances = ld.get_data_to_dict(ld.load_file("./metro.gr"))



parser = argparse.ArgumentParser(description='Find the shortest and longest path between two stations')
parser.add_argument('--stations', help='List stations and their ids', action="store_true")
parser.add_argument('station1', help='First station\'s id', type=int)
parser.add_argument('station2', help='Second station\'s id', type=int)
args = parser.parse_args()

if args.stations:
    print("Here is the list of stations:")
    print()
    for station in names:
        print("{id}: {name}".format(id=station, name=names[station]))
else:
    ld.draw_subway(h, w, coordinates, distances)
    p, d = ld.dijkstra(distances, args.station1, args.station2)
    pl, dl = ld.longest_path(distances, args.station1, args.station2)
    print("Shortest path:")
    print(list(map(lambda x: names[x], p)))
    print()
    print("Longest path:")
    print(list(map(lambda x: names[x], pl)))
    ld.draw_subway(h, w, coordinates, distances, path=p, file_name="shortest_path{station1}_{station2}.svg"
                   .format(station1=names[args.station1], station2=names[args.station2]))
    ld.draw_subway(h, w, coordinates, distances, path=pl, file_name="longest_path{station1}_{station2}.svg"
                   .format(station1=names[args.station1], station2=names[args.station2]))
