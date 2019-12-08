# Carpool Algorithm
Problem Statement
Professor Rao and his army of TAs are working in Soda Hall late at night, writing the final exam for CS 170. Rao
offers to drive and drop TAs off closer to their homes so that they can all get back safe despite the late hours. However,
the roads are long, and Rao would also like to get back to Soda as soon as he can. Can you plan transportation so that
everyone can get home as efficiently as possible?
Formally, you are given an undirected graph G = (L,E) where each vertex in L is a location. You are also given a
starting location s, and a list H of unique locations that correspond to homes. The weight of each edge (u, v) is the
length of the road between locations u and v, and each home in H denotes a location that is inhabited by a TA. Traveling along a road takes energy, and the amount of energy expended is proportional to the length of the road. For every
unit of distance traveled, the driver of the car expends 2
3
units of energy, and a walking TA expends 1 unit of energy.
The car must start and end at s, and every TA must return to their home in H.
You must return a list of vertices vi
that is the tour taken by the car (cycle with repetitions allowed), as well as a list
of drop-off locations at which the TAs get off. You may only drop TAs off at vertices visited by the car, and multiple
TAs can be dropped off at the same location.
We’d like you to produce a route and sequence of drop-offs that minimizes total energy expenditure, which is the
sum of Rao’s energy spent driving and the total energy that all of the TAs spend walking. Note TAs do not expend
any energy while sitting in the car. You may assume that the TAs will take the shortest path home from whichever
location they are dropped off at.

1. Describe briefly what you implemented for your solver (describe at least one and at most three approaches you considered/attempted).

We used the Traveling Salesman Problem (TSP) as a starting point for brainstorming algorithms. The premise of the DTH problem is really similar to TSP; we are trying to minimize distance in a similar fashion. The difference is that we do not actually have to visit every single vertex. TSP has many different solving algorithms, and we saw two different main classes, brute force algorithms that would find exact solutions, and approximate solutions. The graph is metric, which means that the nearest-neighbors greedy solution to TSP is a pretty good approximation, on average within 25% of the optimal solution (https://cse442-17f.github.io/Traveling-Salesman-Algorithms/). Using the nearest-neighbors algorithm, we first constructed a path that merely went through every home. In order to get the distances between each home, we ran the Floyd Warshall algorithm included in networkx, which runs in polynomial time, to get all pairs of shortest paths. This solution had us dropping every TA off at their home, meaning no TAs would walk. We noticed some patterns in the outputs, such as retraversing edges in clusters of homes, and driving back and forth among vertices. So we decided to try clustering the homes using the k-cluster algorithm from the DSP textbook. We dropped off all the TAs in a given cluster at a single home within the cluster. These were the centers of the clusters produced by the algorithm. This algorithm was awful. It performed worse than the simple greedy nearest-neighbors approach. Then, we decided we could transform the graph into a minimum spanning tree that only contained homes and vertices needed to reach those homes. In that tree, all the leaves are homes, so we could find optimal drop-off locations from the predecessors of the leaves. We found an algorithm in networkx to find this tree, which is called a “Steiner Tree”. Then we pruned all the leaves (which were all homes) and dropped the TAs off at each given leaf’s parents. This gave us a solution that performed better than the nearest-neighbor algorithm on a little less than half of the inputs. So, we ran both algorithms on an input and returned the output that had the more optimal cost. Afterwards, we ran the pruning algorithm a second time. If a leaf in our one-time-pruned Steiner Tree was also a home we pruned it again. This helped optimize just a bit, and we chose whichever of the 3 solutions had the lowest cost!

2. Explain which of your approaches worked best, and why you believe it did so.

The combination of our Steiner Tree approach and the Nearest-Neighbors approach was best. This is because we were able to combine the approaches by checking to see which had a lower cost on an input-by-input basis. We think this worked because our algorithms were lightweight and extremely fast, as they were polynomial time and didn’t have that many instructions. They were honestly pretty simple! At the end we did a second pruning of the steiner tree, which worked better for some inputs as well, so we did a third check to see if this algorithm was the best, and always returned the lowest cost output.

3. Explain how you'd refine your current algorithm to improve its performance, if you had more time.

We could have tried to the brute force solution to specifically find the best path, but this takes a long time to run. We could have also experimented with an Integer Linear Programming approach, with either a brute force solution or a rounded Linear Program solution. This probably would have yielded better results, but the mathematical constraints proved difficult for us to find in the given timespan, and our approximation algorithms were easy and flexible.
