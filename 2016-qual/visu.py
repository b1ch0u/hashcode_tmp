import matplotlib.pyplot as plt


def visualize(d, name):
    wxs, wys = [w['row'] for w in d['warehouses']], [w['col'] for w in d['warehouses']]
    plt.scatter(wxs, wys, s=16)

    oxs, oys = [o['row'] for o in d['orders']], [o['col'] for o in d['orders']]
    plt.scatter(oxs, oys, s=4)

    plt.title(name)
    plt.show()