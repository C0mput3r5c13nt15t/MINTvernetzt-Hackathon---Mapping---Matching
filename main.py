from cProfile import label
import networkx as nx
import matplotlib.pyplot as plt
import random


#---Definitions---#


states = ['A', 'B', 'C']
districts = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
topics = ['t1', 't2', 't3', 't4', 't5', 't6', 't7']

maxTopicDistance = 100
minTopicDistance = 10
relatedTopicsTreshold = minTopicDistance + \
    (maxTopicDistance - minTopicDistance) * 0.2
topicImportance = 0.5

# Users are a dictionary with stings of numbers as keys and a dictionary of user data as values
users = {}
for number in range(30):
    users['u' + str(number)] = {'topic': random.choice(topics),
                                'district': random.choice(districts),
                                'max_distance': random.randint(20, 200)}

# Projects are a dictionary with stings of numbers as keys and a dictionary of the project data as values
projects = {}
for number in range(30):
    projects['p' + str(number)] = {'topic': random.choice(topics),
                                   'district': random.choice(districts)}


#---Graph of the states, districts and users---#


# Generate a complete graph from the states
G = nx.complete_graph(states)

# Add random weights to the edges
for (u, v) in G.edges():
    G.edges[u, v]['weight'] = random.randint(100, 400)

edges = G.edges()

# Add districts to the graph
for district in districts:
    G.add_node(district)
    G.add_edge(district, random.choice(states), weight=random.randint(20, 100))

# Add users to the graph
for index in users.keys():
    G.add_node(index)
    G.add_edge(index, users[index]['district'], weight=15)

# Add projects to the graph
for index in projects.keys():
    G.add_node(index)
    G.add_edge(index, projects[index]['district'], weight=15)

# Draw the graph
plt.figure(1)
pos = nx.kamada_kawai_layout(G)

nx.draw_networkx_nodes(
    G, pos, node_size=300, nodelist=states, node_color='y')
nx.draw_networkx_nodes(G, pos, node_size=200,
                       nodelist=districts, node_color='g')
nx.draw_networkx_nodes(G, pos, node_size=100,
                       nodelist=users, node_color='b')
nx.draw_networkx_nodes(G, pos, node_size=100,
                       nodelist=projects, node_color='r')
nx.draw_networkx_edges(G, pos, edgelist=edges, width=2)

nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6)


#---Graph of the topics---#


# Create a complete graph from the topics
G_topics = nx.complete_graph(topics)

# Add random weights to the edges
for (u, v) in G_topics.edges():
    G_topics.edges[u, v]['weight'] = random.randint(
        minTopicDistance, maxTopicDistance)

# Draw the graph
plt.figure(2)
pos_topics = nx.shell_layout(G_topics)
nx.draw_networkx_nodes(G_topics, pos_topics, node_size=500,
                       nodelist=topics, node_color='y')
nx.draw_networkx_edges(G_topics, pos_topics,
                       edgelist=G_topics.edges(), width=2)
nx.draw_networkx_labels(G_topics, pos_topics,
                        font_size=8, font_family="sans-serif")
edge_labels_topics = nx.get_edge_attributes(G_topics, "weight")
nx.draw_networkx_edge_labels(
    G_topics, pos_topics, edge_labels_topics, font_size=6)

#---Find matches---#


def getMatchScore(user, project, G):
    # Checks if two users match based on their topic and distance
    shortestPathLength = nx.dijkstra_path_length(
        G, user['district'], project['district'])
    topicPathLength = nx.dijkstra_path_length(
        G_topics, user['topic'], project['topic'])
    if topicPathLength > relatedTopicsTreshold:
        return 0
    return max((user['max_distance'] - shortestPathLength) * (1-topicImportance) + (maxTopicDistance - topicPathLength) * topicImportance, 0)


#---main---#


if __name__ == "__main__":
    print(users['u0'])
    print(projects['p0'])
    print(getMatchScore(users['u0'], projects['p0'], G))

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
