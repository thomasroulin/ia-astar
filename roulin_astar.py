import math

__author__ = 'thomas.roulin'


class City:
    def __init__(self, name, posx, posy):
        self.name = name
        self.posx = posx
        self.posy = posy
        self.links = []

    def __repr__(self):
        return self.name

    def add_link(self, link):
        self.links.append(link)

    def get_link(self, name):
        return [link for link in self.links if link.city.name == name][0]


class Link:
    def __init__(self, city, dist):
        self.city = city
        self.dist = dist

    def __repr__(self):
        return "Link [" + self.city.__repr__() + " " + str(self.dist) + "]"


def get_city(cities, city_name):
    return [city for city in cities if city.name == city_name][0]


def init_cities(f_connections, f_positions):
    cities = []
    links = []

    for p in [pos.split(" ") for pos in f_positions]:
        cities.append(City(p[0], int(p[1]), int(p[2])))

    for c in [conn.split(" ") for conn in f_connections]:
        city1 = get_city(cities, c[0])
        city2 = get_city(cities, c[1])
        dist = int(c[2])
        city1.add_link(Link(city2, dist))
        city2.add_link(Link(city1, dist))

    return cities


# HEURISTICS
def h0(a, b):
    """ h0(n) = 0 """
    return 0


def h1(a, b):
    """ h1(n) = distance en X """
    return math.fabs(a.posx - b.posx)


def h2(a, b):
    """ h2(n) = distance en Y """
    return math.fabs(a.posy - b.posy)


def h3(a, b):
    """ h3(n) = distance euclidienne """
    return math.sqrt(h1(a, b) ** 2 + h2(a, b) ** 2)


def h4(a, b):
    """ h4(n) = distance de Manhattan """
    return h1(a, b) + h2(a, b)


# ALGORITHM
def astar(start, end, heuristic):
    closed_set = []
    open_set = [start]

    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        print(closed_set)

        current = min(open_set, key=f_score.get)

        if current == end:
            return reconstruct_path(came_from, end)

        open_set.remove(current)
        closed_set.append(current)

        for i in range(len(current.links)):
            neighbor = current.links[i].city

            if neighbor in closed_set:
                continue

            t_g_score = g_score[current] + current.links[i].dist

            if neighbor not in open_set:
                open_set.append(neighbor)
            elif t_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = t_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
    return None


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path


def show_path(path, cities):
    dist = 0
    l = len(path)
    for i in range(l):
        city = get_city(cities, str(path[l - i - 1]))
        print(">"+city.__repr__() + " (" + str(dist) + " km)")
        if i < l - 1:
            dist += (city.get_link(str(path[l - i - 2]))).dist


if __name__ == '__main__':
    file_links = open('connections.txt', 'r')
    file_positions = open('positions.txt', 'r')

    cities = init_cities(file_links, file_positions)
    heuristics = [h0, h1, h2, h3, h4]

    a = get_city(cities, "Copenhagen")
    b = get_city(cities, "Lisbon")

    for h in heuristics:
        title = a.name + " to " + b.name + " with [" + h.__doc__ + "]"
        print("=" * len(title))
        print(title)
        path = astar(a, b, h)
        show_path(path, cities)
