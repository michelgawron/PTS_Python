import load_data as ld

h, w, names, coordinates, distances = ld.get_data_to_dict(ld.load_file("./metro.gr"))
ld.draw_subway(h, w, coordinates, distances)
p, d = ld.dijkstra(distances, 0, 350)
print(p)
print(list(map(lambda x: names[x], p)))
ld.draw_subway(h, w, coordinates, distances, path=p, file_name="trajet.svg")