import time


# Check for lasers given in the input so the board can be updated
def checkForLaser(grid):
    for row in range(n):
        for col in range(n):
            if grid[row][col] == 1:
                player = 1
                score, grid = updateBoard(row, col, grid, player)
                grid[row][col] = player
            if grid[row][col] == 2:
                player = 2
                score, grid = updateBoard(row, col, grid, player)
                grid[row][col] = player
    return grid


# Takes the grid as input and pretty-prints for readability
def print_input_grid(grid):
    for row in range(n):
        for col in range(n):
            if grid[row][col] == 0:
                print '-',
            elif grid[row][col] == 1:
                print 'R',
            elif grid[row][col] == 2:
                print 'B',
            elif grid[row][col] == 3:
                print 'W',
            else:
                print grid[row][col],
        print


# Takes the row and col at which the laser is placed and
# updates the grid to mark blue, red and violet boxes
def updateBoard(r, c, grid, player):
    score = 0
    block = 3
    emitter_range = 4
    if player == 1:
        color = 'r'
        same_color = 'r'
        diff_color = 'b'
        other_player = 2
    else:
        color = 'b'
        same_color = 'b'
        diff_color = 'r'
        other_player = 1

    # North
    for i in xrange(emitter_range):
        if (r - i) >= 0 and grid[r - i][c] != block and grid[r - i][c] != other_player:
            if grid[r - i][c] == same_color or grid[r - i][c] == 'v':
                continue
            elif grid[r - i][c] == diff_color:
                grid[r - i][c] = 'v'
                score += 1
            else:
                grid[r - i][c] = color
                score += 1
        else:
            break  # If there is a wall or a block or other player's Laser

    # South
    for i in xrange(emitter_range):
        if (r + i) < n and grid[r + i][c] != block and grid[r + i][c] != other_player:
            if grid[r + i][c] == same_color or grid[r + i][c] == 'v':
                continue
            elif grid[r + i][c] == diff_color:
                grid[r + i][c] = 'v'
                score += 1
            else:
                grid[r + i][c] = color
                score += 1
        else:
            break

    # West
    for i in xrange(emitter_range):
        if (c - i) >= 0 and grid[r][c - i] != block and grid[r][c - i] != other_player:
            if grid[r][c - i] == same_color or grid[r][c - i] == 'v':
                continue
            elif grid[r][c - i] == diff_color:
                grid[r][c - i] = 'v'
                score += 1
            else:
                grid[r][c - i] = color
                score += 1
        else:
            break

    # East
    for i in xrange(emitter_range):
        if (c + i) < n and grid[r][c + i] != block and grid[r][c + i] != other_player:
            if grid[r][c + i] == same_color or grid[r][c + i] == 'v':
                continue
            elif grid[r][c + i] == diff_color:
                grid[r][c + i] = 'v'
                score += 1
            else:
                grid[r][c + i] = color
                score += 1
        else:
            break

    # Diagonal Top-Right
    for i in xrange(emitter_range):
        if (r - i) >= 0 and c + i < n and grid[r - i][c + i] != block and grid[r - i][c + i] != other_player:
            if grid[r - i][c + i] == same_color or grid[r - i][c + i] == 'v':
                continue
            elif grid[r - i][c + i] == diff_color:
                grid[r - i][c + i] = 'v'
                score += 1
            else:
                grid[r - i][c + i] = color
                score += 1
        else:
            break

    # Diagonal Top-Left
    for i in xrange(emitter_range):
        if (r - i) >= 0 and c - i >= 0 and grid[r - i][c - i] != block and grid[r - i][c - i] != other_player:
            if grid[r - i][c - i] == same_color or grid[r - i][c - i] == 'v':
                continue
            elif grid[r - i][c - i] == diff_color:
                grid[r - i][c - i] = 'v'
                score += 1
            else:
                grid[r - i][c - i] = color
                score += 1
        else:
            break

    # Diagonal Bottom-Right
    for i in xrange(emitter_range):
        if (r + i) < n and (c + i) < n and grid[r + i][c + i] != block and grid[r + i][c + i] != other_player:
            if grid[r + i][c + i] == same_color or grid[r + i][c + i] == 'v':
                continue
            elif grid[r + i][c + i] == diff_color:
                grid[r + i][c + i] = 'v'
                score += 1
            else:
                grid[r + i][c + i] = color
                score += 1
        else:
            break

    # Diagonal Bottom-Left
    for i in xrange(emitter_range):
        if (r + i) < n and (c - i) >= 0 and grid[r + i][c - i] != block and grid[r + i][c - i] != other_player:
            if grid[r + i][c - i] == same_color or grid[r + i][c - i] == 'v':
                continue
            elif grid[r + i][c - i] == diff_color:
                grid[r + i][c - i] = 'v'
                score += 1
            else:
                grid[r + i][c - i] = color
                score += 1
        else:
            break
    return score, grid


def calculate_score(grid, r, c, player):
    score = 0
    block = 3
    emitter_range = 4
    if player == 1:
        same_color = 'r'
        diff_color = 'b'
        other_player = 2
    else:
        same_color = 'b'
        diff_color = 'r'
        other_player = 1

    # North
    for i in xrange(emitter_range):
        if (r - i) >= 0 and grid[r - i][c] != block and grid[r - i][c] != other_player:
            if grid[r - i][c] == same_color or grid[r - i][c] == 'v':
                continue
            elif grid[r - i][c] == diff_color:
                score += 1
            else:
                score += 1
        else:
            break  # If there is a wall or a block or other player's Laser

    # South
    for i in xrange(emitter_range):
        if (r + i) < n and grid[r + i][c] != block and grid[r + i][c] != other_player:
            if grid[r + i][c] == same_color or grid[r + i][c] == 'v':
                continue
            elif grid[r + i][c] == diff_color:
                score += 1
            else:
                score += 1
        else:
            break

    # West
    for i in xrange(emitter_range):
        if (c - i) >= 0 and grid[r][c - i] != block and grid[r][c - i] != other_player:
            if grid[r][c - i] == same_color or grid[r][c - i] == 'v':
                continue
            elif grid[r][c - i] == diff_color:
                score += 1
            else:
                score += 1
        else:
            break

    # East
    for i in xrange(emitter_range):
        if (c + i) < n and grid[r][c + i] != block and grid[r][c + i] != other_player:
            if grid[r][c + i] == same_color or grid[r][c + i] == 'v':
                continue
            elif grid[r][c + i] == diff_color:
                score += 1
            else:
                score += 1
        else:
            break

    # Diagonal Top-Right
    for i in xrange(emitter_range):
        if (r - i) >= 0 and c + i < n and grid[r - i][c + i] != block and grid[r - i][c + i] != other_player:
            if grid[r - i][c + i] == same_color or grid[r - i][c + i] == 'v':
                continue
            elif grid[r - i][c + i] == diff_color:
                score += 1
            else:
                score += 1
        else:
            break

    # Diagonal Top-Left
    for i in xrange(emitter_range):
        if (r - i) >= 0 and c - i >= 0 and grid[r - i][c - i] != block and grid[r - i][c - i] != other_player:
            if grid[r - i][c - i] == same_color or grid[r - i][c - i] == 'v':
                continue
            elif grid[r - i][c - i] == diff_color:
                score += 1
            else:
                score += 1
        else:
            break

    # Diagonal Bottom-Right
    for i in xrange(emitter_range):
        if (r + i) < n and (c + i) < n and grid[r + i][c + i] != block and grid[r + i][c + i] != other_player:
            if grid[r + i][c + i] == same_color or grid[r + i][c + i] == 'v':
                continue
            elif grid[r + i][c + i] == diff_color:
                score += 1
            else:
                score += 1
        else:
            break

    # Diagonal Bottom-Left
    for i in xrange(emitter_range):
        if (r + i) < n and (c - i) >= 0 and grid[r + i][c - i] != block and grid[r + i][c - i] != other_player:
            if grid[r + i][c - i] == same_color or grid[r + i][c - i] == 'v':
                continue
            elif grid[r + i][c - i] == diff_color:
                score += 1
            else:
                score += 1
        else:
            break
    return score


def create_availability_list(grid, player, depth):
    r_list = list(())
    max_depth = 8
    if depth-1 >= max_depth:
        depth_new = max_depth
    else:
        depth_new = n

    for row in range(depth_new):
        for col in range(depth_new):
            if grid[row][col] == 0:

                # Compute Score
                score = calculate_score(grid, row, col, player)

                r_tuple = list((row, col, score))
                r_list.append(r_tuple)
    r_list.sort(key=lambda x: x[2], reverse=True)
    # print r_list
    return r_list


def max_value(grid, red_pts, blue_pts, player, depth):
    r_list = create_availability_list(grid, player, depth)
    max_time = 57

    # Reached a leaf node
    if len(r_list) == 0 or time.time() - start >= max_time:
        if red_pts - blue_pts > 0:
            return 1
        elif red_pts == blue_pts:
            return 0
        else:
            return -1

    best_max = -1000

    for avail_space in r_list:
        # Get the row and col values
        avail_row = avail_space[0]
        avail_col = avail_space[1]

        # create a temp copy of grid
        copy_grid = [row[:] for row in grid]

        # Place the laser and update the grid
        r_score, copy_grid = updateBoard(avail_row, avail_col, copy_grid, player)

        # Updating the grid to add Laser Position
        copy_grid[avail_row][avail_col] = player

        # Add the points for the player
        red_pts += r_score

        # Call minimax for player 2
        best_max = max(best_max, min_value(copy_grid, red_pts, blue_pts, 2, depth + 1))

        # Pruning
        if best_max == 1:
            return best_max

        red_pts -= r_score

    # This return statement only happens at the leaf node
    return best_max


def min_value(grid, red_pts, blue_pts, player, depth):
    r_list = create_availability_list(grid, player, depth)
    max_time = 57

    if len(r_list) == 0 or time.time() - start >= max_time:
        if red_pts - blue_pts > 0:
            return 1
        elif red_pts == blue_pts:
            return 0
        else:
            return -1

    best_min = 1000

    for avail_space in r_list:
        # Get the row and col values
        avail_row = avail_space[0]
        avail_col = avail_space[1]

        # create a temp copy of grid
        copy_grid = [row[:] for row in grid]

        # Place the laser and update the grid
        b_score, copy_grid = updateBoard(avail_row, avail_col, copy_grid, 2)

        # Updating the grid to add Laser Position
        copy_grid[avail_row][avail_col] = player

        # Add the points for the player
        blue_pts += b_score

        # Call minimax for player 1
        best_min = min(best_min, max_value(copy_grid, red_pts, blue_pts, 1, depth + 1))

        blue_pts -= b_score

        # Pruning
        if best_min == -1:
            return best_min
    return best_min


def findBestMove(grid):
    # Assigning the high score to -inf
    bestScore = -1000

    # Initialising best row and col values
    best_row = -1
    best_col = -1

    depth = 0
    player = 1

    r_list = create_availability_list(grid, player, depth)

    for avail_space in r_list:
        # Get the row and col values
        row = avail_space[0]
        col = avail_space[1]

        # Copy the grid
        copy_grid = [temp_row[:] for temp_row in grid]

        # Make the move
        r_score, copy_grid = updateBoard(row, col, copy_grid, 1)

        # Updating the grid to add Laser Position
        copy_grid[row][col] = 1

        red_pts = r_score
        player = 2
        blue_pts = 0

        # Calculate the evaluation function for the move based on return value of minimax
        score = min_value(copy_grid, red_pts, blue_pts, player, depth)

        # Don't need to undo the move as a copy is being stored

        # If value of current move is higher than best move, update best move
        if score > bestScore:
            best_row = row
            best_col = col
            bestScore = score

        # Return the moment Player 1 wins, assuming that the margin with which player 1
        # wins doesn't matter
        if score == 1:
            return best_row, best_col
    return best_row, best_col


def main():
    # Declaring global variables
    global f_in, n

    # List comprehension for initialising the 2D matrix
    laser_grid = [[0 for x in range(n)] for y in range(n)]

    # Initialising the Laser Grid using input.txt
    for r in range(n):
        row_str = f_in.readline().strip()
        c = 0
        for ch in row_str:
            laser_grid[r][c] = int(ch)
            c += 1

    # Checks whether there are 1's or 2's in the input matrix - if opponent has played
    laser_grid = checkForLaser(laser_grid)

    # Finds the best move to make in order to win
    row, col = findBestMove(laser_grid)

    # Write the output to a file named output.txt
    f_out = open('output.txt', 'w')
    f_out.write(str(row) + " " + str(col))

    # Print the result
    print row, col
    print_input_grid(laser_grid)

    # Finds the time the program takes to return a single move
    end = time.time()
    print end - start


### This is where the program starts execution ###

# Reading the input file
f_in = open('input7.txt', 'r')

# Reading the board size
n = int(f_in.readline().strip())

if __name__ == '__main__':
    start = time.time()
    main()
