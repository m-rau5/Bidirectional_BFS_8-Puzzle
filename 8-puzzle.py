from collections import deque


def getStateSuccessors(currState):
    # currState is a touple of touples
    # To make moves we transform them into lists
    currState = list(list(x) for x in currState)
    successors = []

    # Search in the matrix for 0
    emptyRow, emptyCol = None, None
    for i, row in enumerate(currState):
        for j, val in enumerate(row):
            if val == 0:
                emptyRow, emptyCol = i, j
                break
        if emptyRow is not None:
            break

    # X,Y coords for L,R,U,D directions
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for move in moves:
        newRow, newCol = emptyRow + move[0], emptyCol + move[1]

        # If we are not over/under a 3x3 matrix, swap the pieces:
        if 0 <= newRow < 3 and 0 <= newCol < 3:
            newState = [row[:] for row in currState]

            # Swap 0 with neighbor
            newState[emptyRow][emptyCol], newState[newRow][newCol] = newState[newRow][newCol], newState[emptyRow][emptyCol]

            successors.append(newState)

    # Once done, we make a list of tuples with all the moves that were made
    successors = [tuple(tuple(inner) for inner in outer)
                  for outer in successors]

    return successors


def bidirBFS(queue, visited, otherVisited):
    while queue:
        currState, path = queue.popleft()

        if currState not in visited:
            visited[currState] = path

        for successor in getStateSuccessors(currState):
            if successor not in visited:
                queue.append((successor, path + [successor]))
            if successor in otherVisited:
                return path + otherVisited[successor]

    return None


def printMatrix(currState):
    for row in currState:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    # Other example game-states
    # beginState = [[8, 6, 7], [2, 5, 4], [3, 0, 1]]  # -> 31 moves
    # beginState = [[0, 1, 3], [4, 2, 5], [7, 8, 6]]  # -> 4 moves
    # beginState = [[1, 4, 3], [2, 7, 5], [0, 8, 6]]  # -> 18 moves

    beginState = [[7, 2, 4], [5, 0, 6], [8, 3, 1]]  # -> 20 moves
    endState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    beginState = tuple(map(tuple, beginState))
    endState = tuple(map(tuple, endState))

    beginQueue = deque([(beginState, [beginState])])
    endQueue = deque([(endState, [endState])])

    visitedBegin = {beginState: [beginState]}
    visitedEnd = {endState: [endState]}

    solution = None

    # Alternate between search from the beginning and end (goal) state
    while beginQueue and endQueue:
        if len(beginQueue) <= len(endQueue):
            solution = bidirBFS(beginQueue, visitedBegin, visitedEnd)
        if len(beginQueue) > len(endQueue):
            solution = bidirBFS(endQueue, visitedEnd, visitedBegin)
        if solution:
            break

    # stores the begin/end state in the beginning, so we remove them and append endState at the right position
    solution = solution[2:]
    solution.append(endState)

    if solution:
        print("Solution found")
        print("---Initial 8-puzzle---")
        printMatrix(beginState)
        print("---Solution---")
        for step, state in enumerate(solution):
            print(f"Step {step + 1}:")
            printMatrix(state)
    else:
        print("Puzzle is not solvable.")
