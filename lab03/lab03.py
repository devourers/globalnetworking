import random
from numpy.random import choice
from matplotlib import pyplot as plt
import networkx as nx
import hashlib


def trim(list, k=10):
    trimmed_list = list.copy()
    if len(trimmed_list) > k:
        length = len(trimmed_list) - 1
        for i in range(len(trimmed_list) - k):
            trimmed_list.remove(trimmed_list[length - i])
    return trimmed_list


def filter(list, level):
    for i in range(len(list)):
        if i >= len(list):
            break
        for j in range(len(list)):
            if j >= len(list):
                break
            if nodeIDs[list[i]][:level] == nodeIDs[list[j]][:level] and i != j:
                list.remove(list[i])
                i -= 1
                j -= 1


def find_root(ownerID, GUID):
    node = ownerID
    file_pointers[node].append((GUID, ownerID))
    for level in range(1, 40):
        if GUID == neighbor_maps[node][0]:
            break
        for neighbor in neighbor_maps[node][level]:
            if neighbor[:level] == GUID[:level]:
                node = nodeIDs.index(neighbor)
                file_pointers[node].append((GUID, ownerID))
                break
    return node


def find_file(nodeID, GUID):
    node = nodeID
    steps = 0
    for level in range(1, 40):
        for pointer in file_pointers[node]:
            if pointer[0] == GUID:
                steps += 1
                return [pointer[1], steps]
        for neighbor in neighbor_maps[node][level]:
            if neighbor[:level] == GUID[:level]:
                node = nodeIDs.index(neighbor)
                steps += 1
                break


def publish_file(ownerID, GUID=None):
    if GUID is None:
        GUID = hashlib.sha1(str(random.random()).encode()).hexdigest()
    files[ownerID] = GUID
    find_root(ownerID, GUID)


def publish_node(node):
    prefix = find_prefix(node, nodeIDs)
    neighbor_set = acknowledged_multicast(prefix, nodeIDs[node], nodeIDs)

    for part in backpointers:
        for backpointer in part:
            for pointer in backpointer:
                if pointer == node:
                    backpointer.remove(pointer)

    for neighbor in neighbor_set:
        if nodeIDs[neighbor][:len(prefix)+1] != any(neighbor_maps[node][len(prefix)+1][:len(prefix)+1]):
            neighbor_maps[node][len(prefix) + 1].append(nodeIDs[neighbor])
            backpointers[neighbor][len(prefix) + 1].append(node)

    for p in range(len(prefix), 0, -1):
        new_neighbor_set = []
        closest_nodes = trim(neighbor_set)
        for node in closest_nodes:
            for backpointer in backpointers[node][p]:
                new_neighbor_set.append(backpointer)

        new_neighbor_set = list(set(new_neighbor_set))
        neighbor_set = new_neighbor_set.copy()
        filter(new_neighbor_set, p)

        for neighbor in new_neighbor_set:
            if nodeIDs[neighbor][:p] != any(neighbor_maps[node][p][:p]):
                neighbor_maps[node][p].append(nodeIDs[neighbor])
                backpointers[neighbor][p].append(i)


def find_prefix(node, hash):
    for length in range(40, 0, -1):
        for i in range(len(hash)):
            if node != i and hash[node][:length] == hash[i][:length]:
                return hash[node][:length]
    return ''


def acknowledged_multicast(prefix, sender_nodeID, nodeIDs):
    recipients = []
    for nodeID in nodeIDs:
        if nodeID[:len(prefix)] == prefix and nodeID != sender_nodeID:
            recipients.append(nodeIDs.index(nodeID))
    return recipients


def add_neighbor(nodeID, neighbor_map, prefix_length):
    neighbor_map[prefix_length + 1].append(nodeID)


def insert_node(i):
    nodeIDs.append(hashlib.sha1(str(i).encode()).hexdigest())

    neighbor_map = [[] for i in range(40)]
    neighbor_map[0] = nodeIDs[i]

    prefix = find_prefix(i, nodeIDs)
    neighbor_set = acknowledged_multicast(prefix, nodeIDs[i], nodeIDs)

    for node in neighbor_set:
        if nodeIDs[node][:len(prefix)+1] != any(neighbor_map[len(prefix)+1][:len(prefix)+1]):
            add_neighbor(nodeIDs[i], neighbor_maps[node], len(prefix))
            backpointers[i][len(prefix)+1].append(node)

    for p in range(len(prefix), 0, -1):
        new_neighbor_set = []
        closest_nodes = trim(neighbor_set)
        for node in closest_nodes:
            for backpointer in backpointers[node][p]:
                new_neighbor_set.append(backpointer)
        new_neighbor_set = list(set(new_neighbor_set))
        neighbor_set = new_neighbor_set.copy()
        filter(new_neighbor_set, p)
        for neighbor in new_neighbor_set:
            if nodeIDs[neighbor][:p] != any(neighbor_map[p][:p]):
                neighbor_map[p].append(nodeIDs[neighbor])
                backpointers[neighbor][p].append(i)

    neighbor_maps.append(neighbor_map)

    if i >= initial_nodes:
        G.add_node(i)

    connected = []
    while len(connected) != edges:
        connected = choice(G.nodes(), edges)
        for node in connected:
            if G.degree()[node] > 10:
                list(connected).remove(node)

    for node in connected:
        if i == node:
            node += 1
        G.add_edge(i, node)


def information_on_node(node):
    count = 0
    for level in neighbor_maps[node]:
        count += len(level)
    for level in backpointers[node]:
        count += len(level)
    for pointer in file_pointers[node]:
        count += 2
    return count

#Create folder 'graph_images' into project folder!
def visualize_search(nodeID, GUID):
    color_map = ['black' for node in G.nodes()]
    color_map[nodeID] = 'red'
    node_map = [2 for node in G.nodes()]
    node_map[nodeID] = 15
    options = {
        "node_color": color_map,
        "node_size": node_map,
        "edge_color": edge_map,
        "width": .2,
        "with_labels": True,
        "font_size": 3
    }
    nx.draw(G, pos, **options)
    plt.savefig('graph_images/img0.png', dpi=300, bbox_inches='tight')

    node = nodeID
    for level in range(1, 40):
        plt.clf()
        for pointer in file_pointers[node]:
            if pointer[0] == GUID:
                node = pointer[1]
                color_map = ['black' for node in G.nodes()]
                color_map[node] = 'green'
                node_map = [2 for node in G.nodes()]
                node_map[node] = 15
        for neighbor in neighbor_maps[node][level]:
            if neighbor[:level] == GUID[:level]:
                node = nodeIDs.index(neighbor)
                color_map = ['black' for node in G.nodes()]
                color_map[node] = 'red'
                node_map = [2 for node in G.nodes()]
                node_map[node] = 15
                break

        options = {
            "node_color": color_map,
            "node_size": node_map,
            "edge_color": edge_map,
            "width": .2,
            "with_labels": True,
            "font_size": 3
        }
        nx.draw(G, pos, **options)
        plt.savefig('graph_images/img{0}.png'.format(level), dpi=1200, bbox_inches='tight')
        #print(node)
        if color_map[node] == 'yellow':
            return True



initial_nodes = 3
edges = 2
number_of_nodes = 1000
G = nx.empty_graph()

nodeIDs = []
neighbor_maps = []
backpointers = [[[] for i in range(40)] for j in range(number_of_nodes)]

for i in range(initial_nodes):
    G.add_node(i)

for i in range(number_of_nodes):
    insert_node(i)

for j in range(1):
    for i in range(number_of_nodes):
        publish_node(i)

files = ['' for node in G.nodes()]

file_pointers = [[] for node in G.nodes()]

server = random.randint(0, number_of_nodes - 1)
publish_file(server)
for i in range(10):
    publish_file(random.randint(0, number_of_nodes - 1), files[server])

pos = nx.spring_layout(G)
edge_map = range(G.number_of_edges())

visualize_search(0, files[server])


path_lengths = [[0]*(len(G.nodes())) for i in range(len(G.nodes()))]
for i in G.nodes:
    for j in range(i + 1, len(G.nodes())):
        if i != j:
            path_lengths[i][j] = nx.shortest_path_length(G, i, j)
            path_lengths[j][i] = path_lengths[i][j]

max = path_lengths[0][1]
min = path_lengths[0][1]
count = 0
for i in range(len(path_lengths)):
    for j in range(len(path_lengths)):
        if i != j:
            if path_lengths[i][j] > max:
                max = path_lengths[i][j]
            elif path_lengths[i][j] < min:
                min = path_lengths[i][j]
            count += path_lengths[i][j]
avg = count / (number_of_nodes ** 2 - number_of_nodes)
print('Path length:\n'
      '{0}/{1}/{2}'.format(min, avg, max))

max = 0
min = 40
count = 0
errors = 0
for node in G.nodes():
    path = find_file(node, files[server])
    if path is not None:
        if path[1] > max:
            max = path[1]
        elif path[1] < min:
            min = path[1]
        count += path[1]
    elif path is None:
        errors += 1
if number_of_nodes == errors:
    pass
else:
    avg = count / (number_of_nodes - errors)
    print('Edges, used in search:\n'
          '{0}/{1}/{2}'.format(min, avg, max))


max = information_on_node(0)
min = information_on_node(0)
count = 0
for node in G.nodes():
    information = information_on_node(node)
    if information > max:
        max = information
    elif information < min:
        min = information
    count += information
avg = count / number_of_nodes
print('Number of entries:\n'
      '{0}/{1}/{2}'.format(min, avg, max))

