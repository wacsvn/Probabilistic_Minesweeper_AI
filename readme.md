**I. Minimal AI**

Our initial Minimal AI algorithm covers a few basic components such as board representation, state updating, safe tile detection, and action prioritization, all within one class. At this stage, the algorithm was limited to uninformed search techniques. 

When one cell is being considered, the function *get\_neighbors* checks boundary cells (if they exist). Each revealed cell imposes constraints on its neighboring cells. The AI simply uses these local constraints to determine whether all mines around a cell have been identified, in which case it will mark it as safe, flagging the mines (*is\_safe* and *should\_flag*). The *getAction* function serves as the main driver of the search process, both updating the board as tiles are uncovered and marked as well as maintaining the priority queue for performing actions on tiles. 

In terms of creative freedoms for our initial AI, we opted to use sets for tracking revealed and flagged tiles, as it allowed for quick lookups and less redundant checks. We also ensured that the neighbor function adapts to boundary conditions, so that there wouldn’t need to be separate logic for special edge and corner cases. Lastly, by utilizing the priority queue for action selection, we implicitly implemented a simple heuristic since the order that tiles are added to the queue encodes information about which tiles would be explored next. This basis would be built upon in later iterations of the AI. 

**I.B Minimal AI algorithm's performance:**

| Board Size | Sample Size | Score  | Worlds Complete |
| :---- | :---- | :---- | :---- |
| **5x5** | 1000 | 392 | 392 |
| **8x8** | 1000 | 0 | 0 |
| **16x16** | 1000 | 0 | 0 |
| **16x30** | 1000 | 0 | 0 |
| **Total Summary** | 4000 | 392 | 392 |

**II. Final AI**

The core search process of our Final AI is still driven by a constraint propagation function (*assess* within the *Tile* class). However, the search strategy has evolved to include the *NavigationStack* class, an OrderedDict that serves as the frontier for a depth-first search of unexplored tiles, and the *operations* deque, which prioritizes actions based on inferred safety. Additionally, the *sweep* function extends local inference to the entire board. 

We rewrote the board representation to instead use NumPy arrays, which allows for vectorized operations and improved performance for larger board sizes. The *Field* class builds upon this by providing the functions for board manipulation. 

A completely new addition was the *probe\_random* function, which implements some probabilistic reasoning into the decision making process that wasn’t present before. When faced with an uncertain choice, the AI makes an informed guess based on surrounding tile values in order to keep the game going. It will alternate between using logical deductions (*assess* and *sweep*) and calculated risk taking (*probe\_random)* based on the situation, which allows the AI to handle a wider range of board states. Error handling was also introduced in *getAction* to account for unexpected states. 

**II.B Final AI algorithm's performance:**

| Board Size | Sample Size | Score  | Worlds Complete |
| :---- | :---- | :---- | :---- |
| **5x5** | 1000 | 1000 | 1000 |
| **8x8** | 1000 | 603 | 603 |
| **16x16** | 1000 | 976 | 488 |
| **16x30** | 1000 | 0 | 0 |
| **Total Summary** | 4000 | 2579 | 2091 |

**III. Suggestions for improving the performance of system**  
The first technique that we considered was implementing an A\* search algorithm to guide the board exploration. For this, we could have a heuristic function that estimates the risk of uncovering a given cell, which would consider the number of surrounding revealed cells as well as the number of remaining mines on the board. This would potentially reduce the amount of random probes required. 

We also could have utilized Bayesian networks; in this system, the state of each node would be binary (mine or no mine), and revealed numbers would be used as evidence to update the probabilities of surrounding cells containing mines. Once probabilities are propagated across the entire board, the AI would simply have to choose the cell with the lowest probability.

One last suggestion would be to use a Monte Carlo Tree Search, where each possible move is randomly simulated in order to estimate the probability of winning for each. Nodes would store the number of visits and win rates, which would then be used in determining the best move. This would likely be most useful during the late game, when the number of remaining mines are lower and exhaustive search becomes less practical. 