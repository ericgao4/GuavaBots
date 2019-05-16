Problem¶
Your group runs an autonomous food delivery company called Guavabot. Everything is going great - you just raised $10 million in VC funding, and you've deployed to three locations worldwide - Singapore, Tel Aviv, and Toronto. Unfortunately your intern ran rm -rf / on your production servers, losing the locations of all your bots! The bots took quite a while to develop and the prototypes are valuable, so you want to locate them and move them home. Thankfully, you have a worldwide network of students who report the locations of the bots to you via app, but these customers are not always right and may incorrectly inform you about bots' locations.

Statement¶
You have some number of bots lost in the city. Your goal is to find these bots and move them home in the shortest time. You have two operations, both that take some time: remote and scout. A remote moves all bots from a vertex to a neighbour of that vertex. A scout sends a student to a vertex and has the student report if a bot is there.

Formally, your delivery system is for a specific city, i.e. a connected weighted undirected graph 
G
=
(
V
,
E
)
such that all edge weights 
w
e
>
0
, with a designated home vertex 
h
∈
V
. The Guavabots live at a set of locations 
L
⊆
V
 with exactly one Guavabot in each starting location; but you do not know this set of starting locations. In addition, you have a set of 
k
 students that you can send to vertices on the graph to inform you if Guavabots are present there; however, the students are unreliable and are incorrect on a fixed, unknown subset of vertices.

You are given and know the graph 
G
, edge weights 
w
e
, home vertex 
h
, number of Guavabots 
|
L
|
, and the number of students 
k
. All graphs are complete, have 
|
L
|
=
5
 bots, 
n
=
100
 vertices, and 
k
∈
{
10
,
20
,
40
}
 students.

You do not know the starting locations of the Guavabots 
L
 or the opinions of the students (until you ask for them by scouting).

Actions¶
You get the bots home by performing a series of actions of your choice. Your available actions are:

scout on 
(
i
,
v
)
, where 
i
 is a student and 
v
∈
V
. In this case, student 
i
 visits the vertex and reports to you whether they see Guavabots at the vertex (they give this as a yes/no answer). However, their report may be incorrect. You have to wait for the student to move to the vertex and report you the answer, which takes 1 time.

For more information on how student reports work, see students.

remote on the directed edge 
(
u
,
v
)
, provided that 
{
u
,
v
}
∈
E
. This tells you how many Guavabots there were at 
u
 that received the command, then all the Guavabots at 
u
 move to 
v
. Regardless of the presence of Guavabots at 
u
, it takes 
w
u
v
 time to wait and see if your command has moved any Guavabots.

As the graph is undirected, you can remote along either direction on any edge.

You can only perform one action at a time, and you cannot "undo" an action.

We call an instance of this problem and the sequence of actions you take a "rescue".

Constraints¶
After you remote along an edge 
{
u
,
v
}
 in the direction 
u
→
v
, any future scouts on 
u
 or 
v
 will fail (as you already know about the existence of Guavabots at either vertex). The only exception is if no bots were remoted along the edge, in which case you can scout on 
v
 in the future.
You cannot perform a scout at the home vertex 
h
, ever.
Students¶
Each student 
i
 can give you a report on any vertex so long you haven't used it in a remote already. If a student is incorrect on a vertex, they will always report the opposite of the truth; students are incorrect a fixed, but unknown number of times. This means that for each student 
i
, there is a fixed, unknown subset 
S
i
⊆
V
 of vertices that they will be wrong at. These sets 
S
1
,
…
,
S
k
 are fixed for the input, meaning they are completely determined before your rescue even starts; in other words, the student opinions will not change depending on how your algorithm runs.

There are no guarantees on how correct the students will be beyond the fact that 
|
S
i
|
≤
|
V
|
/
2
 for all students 
i
. It is up to you to come up with an algorithm that uses the student reports as effectively as possible.

Time¶
Time is measured as follows:

When you start, the current time is zero.
There is a fixed time every scout action takes; after every scout your time is incremented by 1.
After a remote on the edge 
{
u
,
v
}
, your time is incremented by 
w
u
v
, regardless of the direction you remote on 
{
u
,
v
}
The scout cost 
1
 is much smaller than most edge weights 
w
e
.

Goal¶
You are given a score once you end the rescue. If the time taken so far is 
t
 and the number of Guavabots that are home is 
g
, this score is:

100
|
L
|
+
1
(
g
+
α
α
+
t
)
where 
α
∼
10
3
 is a constant among all inputs which is yet to be determined, but is within an order a magnitude of 
10
3
 and is about the raw time of an average solver that gets all the bots home.

You want to get as high a score as possible. The minimum score for any instance is 
0
, and the maximum score for any instance is 
100
 (neither side is necessarily attainable, your score will fall in between).

This scoring function was designed such that returning more bots is always better than spending less time. For example, say that we have 5 bots scattered on a graph:

If we return 5 bots and take 10000 time, our score is 
≈
84.8
If we return 2 bots and take 100 time, our score is 
≈
48.5
If we return 1 bot and take 10 time, our score is 
≈
33.17
Another way to see it: treat your score as a tuple 
(
g
,
t
)
. Scores will be ordered by 
g
 descending first, then by 
t
ascending.


