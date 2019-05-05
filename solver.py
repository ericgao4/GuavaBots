import networkx as nx
from operator import itemgetter
import math
import random


def solve(client):
    client.end()
    client.start()

    # SETUP

    # record the nodes that you know have been used remote(u,v)  on (add u and v ).
    remoted_nodes = []

    # Contains all the nodes that the majority of votes returned false when scout was used on that node.
    majority_false = []

    # Students
    students_metadata = generate_student_dic(client)


    # shortest paths dict {node: path from node to H}
    shortest_paths = djisktras(client.G, client.h)

    # Reserve shortest path list s -> H.
    reverse_lists_in_shortest_paths(shortest_paths, client.h)  # necessary

    # dict (node_value, shortest_path_value)
    sp_lengths = djisktras_length(client.G, client.h)
    sp_lengths.pop(client.h)  # Gets rid of home node in list

    # ordered list of [node, shortest path weight] dec order
    sp_ordered_list = convert_dict_to_list(sp_lengths)
    sp_ordered_list.reverse()
    print(sp_ordered_list)
    # max students
    biggest_liar = [-1, -1]

    # COMPUTATION
    # bots that were remoted to h
    bots_to_h = 0
    for node, sp_weight in sp_ordered_list:
        # Scout
        remote_boolean = True
        if node not in remoted_nodes:
            student_results = scout_k(node, client, biggest_liar)
            yes = 0
            no = 0
            for value in student_results.items():
                s = value[0]
                r = value[1]
                if r:
                    yes += students_metadata.get(s)[0]
                else:
                    no += students_metadata.get(s)[0]
            remote_boolean = (yes >= no)
        # Remote
        if remote_boolean:
            # find neighbor in shortest paths
            # value = [node neighbor ... h]
            neighbor = shortest_paths.get(node)[1]
            # remote
            number_bots_remoted = client.remote(node, neighbor)
            # update_student_metadata
            biggest_liar = update_student_metadata(students_metadata,
                                                   student_results, number_bots_remoted == 0,
                                                   biggest_liar)

            # check if remote to h.
            if neighbor == client.h:
                bots_to_h += number_bots_remoted
            remoted_nodes.append(neighbor)
            remoted_nodes.append(node)
        else:
            # add to majority_false list.
            majority_false.append([node, sp_weight])
    if bots_to_h < client.l:
        majority_false.sort(key=itemgetter(1), reverse=True)
        max_path_length = len(shortest_paths.get(majority_false[0][0]))
        elements_with_bots = []
        bots_undiscovered = client.l - bots_to_h
        while bots_undiscovered > 0:
            if len(majority_false) >= 1:
                check_index = random.randint(0, len(majority_false) - 1)
            else:
                check_index = 0
            x = majority_false[check_index]
            node = x[0]
            neighbor = shortest_paths.get(node)[1]
            remoted_value = client.remote(node, neighbor)
            if remoted_value != 0:
                bots_undiscovered -= 1
                elements_with_bots.append(node)
            majority_false.remove(x)
        for y in range(1, max_path_length):
                for x in elements_with_bots:
                    remote_path(x, client, shortest_paths, y)
        print(elements_with_bots)
    print(bots_to_h)
    print(client.bot_count[client.h])
    print(client.l)
    print(majority_false)
    client.end()


def update_student_metadata(students_metadata, students_votes, majority_liar, biggest_liar):
    if majority_liar:
        for value in students_votes.items():
            student = value[0]
            response = value[1]
            if response:
                # update voting power and number of wrong
                students_metadata[student][0] *= 0.8
                students_metadata[student][1] += 1
            else:
                # update voting power
                students_metadata[student][0] += 1
            if biggest_liar[1] < students_metadata[student][1]:
                biggest_liar = [student, students_metadata[student][1]]
    else:
        for value in students_votes.items():
            student = value[0]
            response = value[1]
            if not response:
                # update voting power and number of wrong
                students_metadata[student][0] *= 0.8
                students_metadata[student][1] += 1
            else:
                # update voting power
                students_metadata[student][0] += 1
            if biggest_liar[1] < students_metadata[student][1]:
                biggest_liar = [student, students_metadata[student][1]]
    return biggest_liar


# Remote from s->H
def remote_path(node, client, shortest_paths, cur_bots_index):
    sp = shortest_paths.get(node)
    if cur_bots_index < len(sp) - 1:
        from_node = sp[cur_bots_index]
        to_node = sp[cur_bots_index + 1]
        client.remote(from_node, to_node)

# Scout
def scout_k(node, client, biggest_liar):
    if biggest_liar[1] >= math.floor(client.n/2):
        return client.scout(node, [biggest_liar[0]])
    else:
        return client.scout(node, [s for s in range(1, client.k + 1)])


# convert dict of key = node, value = total shortest path weight -> sorted list based on value.
def convert_dict_to_list(dict):
    dict_list = [[key, value] for key, value in dict.items()]
    return dict_list



# GIVEN A GRAPH G, FIND SHORTEST PATH FROM Home TO EACH vertex
# INPUT IS A NETWORKX GRAPH OBJECT I.E. CLIENT.G AND THE HOME VERTEX
def djisktras(G, H):
    return nx.single_source_dijkstra_path(G, H)


# gives length of each shortest path (Useful when sorting length edges)
def djisktras_length(G, H):
    return nx.single_source_dijkstra_path_length(G, H)

#
def generate_student_dic(client):
    students = {}
    for i in range(1,  client.k + 1):
        value = [1, 0]
        students[i] = value
    return students

#
def reverse_lists_in_shortest_paths(d, H):
    for i in d.keys():
        d[i] = list(reversed(d[i]))
    d.pop(H)




