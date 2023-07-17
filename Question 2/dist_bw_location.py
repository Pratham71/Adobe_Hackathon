from geopy.distance import geodesic as gd


def dist_bw_location(transactions):
    dist_above_20 = []
    for i in transactions:
        for j in transactions:
            if i == j:
                continue
            if gd(i[3], j[3]).km >= 20 and i[1] == j[1]:
                if ((i, j) not in dist_above_20) and ((j, i) not in dist_above_20):
                    dist_above_20.append((i, j))
    return dist_above_20
