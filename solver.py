import networkx as nx
from operator import itemgetter
import math


def solve(client):
    client.end()
    client.start()

    # record the nodes that you know have been used remote(u,v)  on (add u and v ).
    remoted_nodes = []

    # Contains all the nodes that the majority of votes returned false when scout was used on that node.
    majority_false = []

    # Students
    students_metadata = generate_student_list(client)

    # SETUP

    # call this to populate MAJORITY_FALSE LIST
    generate_student_list(client.k)

    # shortest paths dict {node: path from node to H}
    shortest_paths = djisktras(client.G, client.h)

    # Reserve shortest path list s -> H.
    reverse_lists_in_shortest_paths(shortest_paths, client.h)  # necessary

    # dict (node_value, shortest_path_value)
    sp_lengths = djisktras_length(client.G, client.h)
    sp_lengths.pop(client.h)  # Gets rid of home node in list

    # ordered list of [node, shortest path weight] dec order
    sp_ordered_list = convert_dict_to_ordered_list(sp_lengths)

    # bots remoted to H
    bots_to_h = 0

    # max students
    biggest_liar = [-1, -1]

    # COMPUTATION
    # Phase 1
    for node, sp_weight in sp_ordered_list:
        # Scout
        if node in remoted_nodes:
            continue
        else:
            student_results = scout_k(node, client, students_metadata, biggest_liar)
            yes = 0
            no = 0
            for student, response in student_results:
                if response:
                    yes += students_metadata.get(student)[0]
                else:
                    no += students_metadata.get(student)[0]
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
                                                   student_results, number_bots_remoted == 0, biggest_liar)
            # check if remote to h.
            if neighbor == client.h:
                bots_to_h += number_bots_remoted
            remoted_nodes.append(neighbor)
            remoted_nodes.append(node)
        else:
            # add to majority_false list.
            majority_false.append([node, sp_weight])

    # Perform Phase 2
    if bots_to_h < client.l:
        majority_false.sort(key=itemgetter(1), reverse=True)
        max_path_length = len(shortest_paths.get(majority_false[0]))
        for y in range(max_path_length):
            for x in majority_false:
                remote_path(x[0], client, shortest_paths, y)

    client.end()


def update_student_metadata(students_metadata, students_votes, majority_liar, biggest_liar):
    if majority_liar:
        for student, response in students_votes:
            if response:
                # update voting power and number of wrong
                students_metadata[student][0] *= 0.9
                students_metadata[student][1] += 1
            else:
                # update voting power
                students_metadata[student][0] += 1
            if biggest_liar[1] < students_metadata[student][1]:
                biggest_liar = [student, students_metadata[student][1]]
    else:
        for student, response in students_votes:
            if not response:
                # update voting power and number of wrong
                students_metadata[student][0] *= 0.9
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
    if cur_bots_index < len(sp):
        from_node = sp[cur_bots_index]
        to_node = sp[cur_bots_index + 1]
        client.remote(from_node, to_node)


# Scout
def scout_k(node, client, students_metadata, biggest_liar):
    if biggest_liar[1] <= math.floor(client.n/2):
        return client.scout(node, [biggest_liar[0]])
    else:
        return client.scout(node, [s for s in range(1, client.k + 1)])


# convert dict of key = node, value = total shortest path weight -> sorted list based on value.
def convert_dict_to_ordered_list(dict):
    dict_list = [[key,value] for key, value in dict.items()]
    sorted(dict_list, key=itemgetter(1), reverse=True)
    return dict_list



# GIVEN A GRAPH G, FIND SHORTEST PATH FROM Home TO EACH vertex
# INPUT IS A NETWORKX GRAPH OBJECT I.E. CLIENT.G AND THE HOME VERTEX
def djisktras(G, H):
    return nx.single_source_dijkstra_path(G, H)


# gives length of each shortest path (Useful when sorting length edges)
def djisktras_length(G, H):
    return nx.single_source_dijkstra_path_length(G, H)

#
def generate_student_list(client):
    students = {}
    for i in range(1,  client.k + 1):
        value = [1, 0]
        students[i] =  value
    return students

#
def reverse_lists_in_shortest_paths(d, H):
    for i in d.keys():
        d[i] = list(reversed(d[i]))
    d.pop(H)



