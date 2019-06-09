import time

walls = []
terminals = []
inputFile = open('input.txt', 'r')
gridSize = int(inputFile.readline().strip())
wallNum = int(inputFile.readline().strip())
for i in range(wallNum):
    walls.append(inputFile.readline().rstrip('\n').split(','))
for s in walls:
    s[0] = int(s[0])
    s[1] = int(s[1])
    s[0] = s[0] - 1
    s[1] = s[1] - 1
terminalNum = int(inputFile.readline())
for i in range(terminalNum):
    terminals.append(inputFile.readline().rstrip('\n').split(','))
for s in terminals:
    s[0] = int(s[0])
    s[1] = int(s[1])
    s[0] = s[0] - 1
    s[1] = s[1] - 1
probability = float(inputFile.readline().strip())
rewardsNonTerminal = float(inputFile.readline().strip())
gamma = float(inputFile.readline().strip())
actlist = ['U', 'D', 'L', 'R']


def checkWalls(s):
    for (x, y) in walls:
        if x == s[0] and y == s[1]:
            return True
    return False


def checkTerminal(s):
    for (x, y, z) in terminals:
        if x == s[0] and y == s[1]:
            return True
    return False


class MDP:
    def __init__(self, terminal, gamma, transition={}):
        self.terminal = terminal
        self.gamma = gamma
        self.transition = transition
        self.states = sorted(transition.keys())

    '''def R(self, state):
        return self.reward[state]'''

    def T(self, state, action):
        if (self.transition == {}):
            raise ValueError("Model missing")
        else:
            return self.transition[state][action]

    def actions(self, state):
        if state in self.terminal:
            return ['E']
        else:
            return self.transition[state].keys()

    def value_iteration(self, epsilon):
        states = self.states
        T = self.T
        actions = self.actions
        U1 = {s: 0.0 for s in states}
        for (x, y, z) in self.terminal:
            U1[(x, y)] = float(z)
        for (i, j) in walls:
            U1[(i, j)] = 0.0
        count = 0
        while True:
            count += 1
            U = U1.copy()
            delta = 0
            for s in states:
                # Bellman update, update the utility values
                U1[s] = rewardsNonTerminal + gamma * max([sum([p * U[s1] for (p, s1) in T(s, a)]) for a in actions(s)])
                delta = max(delta, abs(U1[s] - U[s]))

                # check for convergence, if values converged then return V
                if delta < epsilon * (1 - self.gamma) / self.gamma:
                    return U
                if time.time() - start > 28:
                    return U

    def best_policy(self, U):
        states = self.states
        actions = self.actions
        policy = {}
        for s in states:
            policy[s] = max(actions(s), key=lambda a: self.expected_utility(a, s, U))
        return policy

    def expected_utility(self, a, s, U):
        return sum([p * U[s1] for (p, s1) in self.T(s, a)])


def createTransitions():
    transitions = {}
    swingingProb = (1 - probability) / 2

    for i in range(gridSize):
        for j in range(gridSize):
            flag = True
            for (x, y) in walls:
                if x == i and y == j:
                    flag = False
                    break
            for (x, y, z) in terminals:
                if x == i and y == j:
                    # Append to transition model
                    flag = False
                    break
            if flag:
                for act in actlist:
                    if act == 'U':
                        mainProbTuple = list(())
                        cwProbTuple = list(())
                        acwProbTuple = list(())
                        samePosTuple = list(())
                        sum_prob = 0
                        if i - 1 >= 0 and not checkWalls((i - 1, j)):
                            # Can move up
                            mainProbTuple = (probability, (i - 1, j))
                        else:
                            # Remain in same cell
                            samePosTuple = (probability, (i, j))
                            sum_prob += probability
                        if i - 1 >= 0 and j + 1 < gridSize and not checkWalls((i - 1, j + 1)):
                            cwProbTuple = (swingingProb, (i - 1, j + 1))
                        else:
                            # Remain in the same cell
                            samePosTuple = (sum_prob + swingingProb, (i, j))
                            sum_prob += swingingProb
                        if i - 1 >= 0 and j - 1 >= 0 and not checkWalls((i - 1, j - 1)):
                            acwProbTuple = (swingingProb, (i - 1, j - 1))
                        else:
                            samePosTuple = (sum_prob+swingingProb, (i, j))
                            sum_prob += swingingProb

                        transitions[(i, j)] = {}
                        transitions[(i, j)]['U'] = []
                        if mainProbTuple:
                            transitions[(i, j)]['U'].append(mainProbTuple)
                        if cwProbTuple:
                            transitions[(i, j)]['U'].append(cwProbTuple)
                        if acwProbTuple:
                            transitions[(i, j)]['U'].append(acwProbTuple)
                        if samePosTuple:
                            transitions[(i, j)]['U'].append(samePosTuple)

                    if act == 'D':
                        mainProbTuple = list(())
                        cwProbTuple = list(())
                        acwProbTuple = list(())
                        samePosTuple = list(())
                        sum_prob = 0
                        if i + 1 < gridSize and not checkWalls((i + 1, j)):
                            # Can move down
                            mainProbTuple = (probability, (i + 1, j))
                        else:
                            # Remain in same cell
                            samePosTuple = (probability, (i, j))
                            sum_prob += probability
                        if i + 1 < gridSize and j - 1 >= 0 and not checkWalls((i + 1, j - 1)):
                            cwProbTuple = (swingingProb, (i + 1, j - 1))
                        else:
                            # Remain in the same cell
                            samePosTuple = (sum_prob+swingingProb, (i, j))
                            sum_prob += swingingProb
                        if i + 1 < gridSize and j + 1 < gridSize and not checkWalls((i + 1, j + 1)):
                            acwProbTuple = (swingingProb, (i + 1, j + 1))
                        else:
                            samePosTuple = (sum_prob+swingingProb, (i, j))
                            sum_prob += swingingProb

                        transitions[(i, j)]['D'] = []
                        if mainProbTuple:
                            transitions[(i, j)]['D'].append(mainProbTuple)
                        if cwProbTuple:
                            transitions[(i, j)]['D'].append(cwProbTuple)
                        if acwProbTuple:
                            transitions[(i, j)]['D'].append(acwProbTuple)
                        if samePosTuple:
                            transitions[(i, j)]['D'].append(samePosTuple)

                    if act == 'L':
                        mainProbTuple = list(())
                        cwProbTuple = list(())
                        acwProbTuple = list(())
                        samePosTuple = list(())
                        sum_prob = 0
                        if j - 1 >= 0 and not checkWalls((i, j - 1)):
                            # Can move down
                            mainProbTuple = (probability, (i, j - 1))
                        else:
                            # Remain in same cell
                            samePosTuple = (probability, (i, j))
                            sum_prob += probability
                        if i - 1 >= 0 and j - 1 >= 0 and not checkWalls((i - 1, j - 1)):
                            cwProbTuple = (swingingProb, (i - 1, j - 1))
                        else:
                            # Remain in the same cell
                            samePosTuple = (sum_prob + swingingProb, (i, j))
                            sum_prob += swingingProb
                        if i + 1 < gridSize and j - 1 >= 0 and not checkWalls((i + 1, j - 1)):
                            acwProbTuple = (swingingProb, (i + 1, j - 1))
                        else:
                            samePosTuple = (sum_prob + swingingProb, (i, j))
                            sum_prob += swingingProb

                        transitions[(i, j)]['L'] = []
                        if mainProbTuple:
                            transitions[(i, j)]['L'].append(mainProbTuple)
                        if cwProbTuple:
                            transitions[(i, j)]['L'].append(cwProbTuple)
                        if acwProbTuple:
                            transitions[(i, j)]['L'].append(acwProbTuple)
                        if samePosTuple:
                            transitions[(i, j)]['L'].append(samePosTuple)

                    if act == 'R':
                        mainProbTuple = list(())
                        cwProbTuple = list(())
                        acwProbTuple = list(())
                        samePosTuple = list(())
                        sum_prob = 0
                        if j + 1 < gridSize and not checkWalls((i, j + 1)):
                            # Can move right
                            mainProbTuple = (probability, (i, j + 1))
                        else:
                            # Remain in same cell
                            samePosTuple = (probability, (i, j))
                            sum_prob += probability
                        if i + 1 < gridSize and j + 1 < gridSize and not checkWalls((i + 1, j + 1)):
                            cwProbTuple = (swingingProb, (i + 1, j + 1))
                        else:
                            # Remain in the same cell
                            samePosTuple = (sum_prob+swingingProb, (i, j))
                            sum_prob += swingingProb
                        if i - 1 >= 0 and j + 1 < gridSize and not checkWalls((i - 1, j + 1)):
                            acwProbTuple = (swingingProb, (i - 1, j + 1))
                        else:
                            samePosTuple = (sum_prob+swingingProb, (i, j))
                            sum_prob += swingingProb

                        transitions[(i, j)]['R'] = []
                        if mainProbTuple:
                            transitions[(i, j)]['R'].append(mainProbTuple)
                        if cwProbTuple:
                            transitions[(i, j)]['R'].append(cwProbTuple)
                        if acwProbTuple:
                            transitions[(i, j)]['R'].append(acwProbTuple)
                        if samePosTuple:
                            transitions[(i, j)]['R'].append(samePosTuple)
    return transitions


def main():
    transitions = createTransitions()
    mdp = MDP(terminal=terminals, gamma=gamma, transition=transitions)
    U = mdp.value_iteration(epsilon=0.0001)
    policy = mdp.best_policy(U)
    for i, j in walls:
        policy[(i, j)] = 'N'
    for i, j, k in terminals:
        policy[(i, j)] = 'E'
    f_out = open('output.txt', 'w')
    for i in range(gridSize):
        output_policy = ''
        for j in range(gridSize):
            output_policy += policy[(i, j)]
            if not j == gridSize - 1:
                output_policy += ','
        f_out.write(output_policy)
        f_out.write("\n")
    f_out.close()

    end = time.time()
    # print end - start


if __name__ == '__main__':
    start = time.time()
    main()