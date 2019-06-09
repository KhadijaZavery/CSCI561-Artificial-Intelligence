import heapq
from collections import OrderedDict

f_in = open('input_test.txt', 'r')

# Reading the Airport constraints LGT
airport_constraints_row = (f_in.readline().split())

landing_limit = int(airport_constraints_row[0])
gate_limit = int(airport_constraints_row[1])
takeoff_limit = int(airport_constraints_row[2])

# Reading the number of planes
num_planes = int(f_in.readline())

# List comprehension for initialising the 3D List
constraint_grid = [[[0 for col in range(2)] for col in range(3)] for row in range(num_planes)]

# Initialising the Planes Grid using input.txt
planes_dict = {}
for row in range(num_planes):
    (r, m, s, o, c) = map(int, f_in.readline().split())
    planes_dict[row] = (r, m, s, o, c)

# Check for all L,G,T values greater than or equal to planes
f_out = open('output.txt','w')
if landing_limit >= num_planes and gate_limit >= num_planes and takeoff_limit >= num_planes:
    for each in xrange(num_planes):
        l_time = 0
        t_time = planes_dict[each][1] + planes_dict[each][2] # M+S
        f_out.write(str(l_time) + " " + str(t_time))
        f_out.write("\n")
    quit()

planes_sorted = OrderedDict(sorted(planes_dict.items(), key=lambda x: x[1]))

# Store the mapping of flights
plane_order = list(planes_sorted.keys())
# print plane_order

plane_pos = []
for i in xrange(num_planes):
    plane_pos.append(plane_order.index(i))

# Initialising the Planes Grid using input.txt
for index in range(num_planes):
    remaining_fuel = planes_sorted[plane_order[index]][0]
    mins_to_land = planes_sorted[plane_order[index]][1]
    service_time = planes_sorted[plane_order[index]][2]
    takeoff_time = planes_sorted[plane_order[index]][3]
    complain_time = planes_sorted[plane_order[index]][4]
    final_landing_start = remaining_fuel
    lower_takeoff_start = mins_to_land + service_time
    upper_takeoff_start = mins_to_land + complain_time + remaining_fuel
    lower_takeoff_end = mins_to_land + service_time + takeoff_time
    upper_takeoff_end = remaining_fuel + mins_to_land + complain_time + takeoff_time
    for c in range(3):
        for d in range(2):
            if c == 0 and d == 0:
                constraint_grid[index][c][d] = 0
            if c == 0 and d == 1:
                constraint_grid[index][c][d] = final_landing_start
            if c == 1 and d == 0:
                constraint_grid[index][c][d] = lower_takeoff_start
            if c == 1 and d == 1:
                constraint_grid[index][c][d] = upper_takeoff_start
            if c == 2 and d == 0:
                constraint_grid[index][c][d] = lower_takeoff_end
            if c == 2 and d == 1:
                constraint_grid[index][c][d] = upper_takeoff_end

# print constraint_grid

assign_planes = []
for row in xrange(num_planes):
    assign_planes.append(0)

landing_list = []
service_list = []
takeoff_list = []


def planes_assigned(planes):
    for i in xrange(num_planes):
        if planes[i] == 0:
            return True
    return False

failed = []
while planes_assigned(assign_planes):
    flag = False
    # Getting the first index at which the plane isn't assigned
    first_index = assign_planes.index(0)
    landing_mins_orig = planes_sorted[plane_order[first_index]][1]
    conflict_num = 0
    landing_list_copy = landing_list[:]
    service_list_copy = service_list[:]
    takeoff_list_copy = takeoff_list[:]
    constraint_grid_copy = [[x[:] for x in y] for y in constraint_grid]

    # There is still space in the landing list
    if len(landing_list) < landing_limit:
        heapq.heappush(landing_list, constraint_grid[first_index][0][0] + landing_mins_orig)
    else:
        heapq.heappop(landing_list)
        heapq.heappush(landing_list, constraint_grid[first_index][0][0] + landing_mins_orig)
    available = landing_limit - len(landing_list)
    min_land_gate_free = min(landing_list)
    # Check if the current assigned plane's landing conflicts with any other
    for x in range(first_index + 1, num_planes):
        landing_mins = planes_sorted[plane_order[x]][1]
        if constraint_grid[first_index][0][0] >= constraint_grid[x][0][0]:
            conflict_num += 1
            if conflict_num > available:

                # Need to perform arc consistency, no more space
                old_value = constraint_grid[x][0][0]
                constraint_grid[x][0][0] = min_land_gate_free
                updated_value = constraint_grid[x][0][0]
                diff = updated_value - old_value

                # add the difference column wise
                constraint_grid[x][1][0] = constraint_grid[x][1][0] + diff
                constraint_grid[x][2][0] = constraint_grid[x][2][0] + diff

                # Check for back-tracking

                if constraint_grid[x][0][0] > constraint_grid[x][0][1]:
                    if plane_order[first_index] not in failed:
                        failed.append(plane_order[first_index])

                    failed_pos = []
                    for i in failed:
                        failed_pos.append(plane_order.index(i))

                    for i in xrange(num_planes):
                        if assign_planes[i] == 0 and i not in failed_pos:
                            landing_list = landing_list_copy[:]
                            service_list = service_list_copy[:]
                            takeoff_list = takeoff_list_copy[:]
                            constraint_grid = [[x[:] for x in y] for y in constraint_grid_copy]

                            plane_order[first_index], plane_order[i] = plane_order[i], plane_order[first_index]
                            constraint_grid[first_index], constraint_grid[i] = constraint_grid[i], \
                                                                               constraint_grid[first_index]

                            plane_pos[first_index], plane_pos[i] = plane_pos[i], plane_pos[first_index]
                            flag = True
                            break
            else:
                # Can accomodate the conflict
                min_land_gate_free = min(min_land_gate_free, constraint_grid[x][0][0] + landing_mins)

        if flag == True:
            break
    if flag == True:
        continue



    # Starting for second column on constraints
    conflict_num = 0
    if len(service_list) < gate_limit:
        heapq.heappush(service_list, constraint_grid[first_index][1][0])
    else:
        heapq.heappop(service_list)
        heapq.heappush(service_list, constraint_grid[first_index][1][0])
    available = gate_limit - len(service_list)
    min_land_gate_free = min(service_list)

    for x in range(first_index + 1, num_planes):
        landing_mins = planes_sorted[plane_order[x]][1]
        if constraint_grid[x][0][0] + landing_mins < min_land_gate_free:
            conflict_num += 1
            if conflict_num > available:
                # Update the domains

                old_value = constraint_grid[x][0][0]
                constraint_grid[x][0][0] = min_land_gate_free - landing_mins
                updated_value = constraint_grid[x][0][0]
                diff = updated_value - old_value

                # add the difference column wise
                constraint_grid[x][1][0] = constraint_grid[x][1][0] + diff
                constraint_grid[x][2][0] = constraint_grid[x][2][0] + diff

                # BT
                if constraint_grid[x][0][0] > constraint_grid[x][0][1]:
                    if plane_order[first_index] not in failed:
                        failed.append(plane_order[first_index])

                    failed_pos = []
                    for i in failed:
                        failed_pos.append(plane_order.index(i))

                    for i in xrange(num_planes):
                        if assign_planes[i] == 0 and i not in failed_pos:
                            landing_list = landing_list_copy[:]
                            service_list = service_list_copy[:]
                            takeoff_list = takeoff_list_copy[:]
                            constraint_grid = [[x[:] for x in y] for y in constraint_grid_copy]

                            plane_order[first_index], plane_order[i] = plane_order[i], plane_order[first_index]
                            constraint_grid[first_index], constraint_grid[i] = constraint_grid[i], \
                                                                               constraint_grid[first_index]

                            plane_pos[first_index], plane_pos[i] = plane_pos[i], plane_pos[first_index]
                            flag = True
                            break
            else:
                min_land_gate_free = min(min_land_gate_free, constraint_grid[x][1][0])
        if flag == True:
            break
    if flag == True:
        continue

    # Starting for third column on constraints
    conflict_num = 0
    if len(takeoff_list) < takeoff_limit:
        heapq.heappush(takeoff_list, constraint_grid[first_index][2][0])
    else:
        heapq.heappop(takeoff_list)
        heapq.heappush(takeoff_list, constraint_grid[first_index][2][0])
    available = takeoff_limit - len(takeoff_list)
    min_land_gate_free = min(takeoff_list)

    for x in range(first_index + 1, num_planes):
        landing_mins = planes_sorted[plane_order[x]][1]
        complain_mins = planes_sorted[plane_order[x]][4]
        if constraint_grid[x][1][0] < min_land_gate_free:
            conflict_num += 1
            if conflict_num > available:
                # Update the domains

                old_value = constraint_grid[x][1][0]
                constraint_grid[x][1][0] = min_land_gate_free
                updated_value = constraint_grid[x][1][0]
                diff = updated_value - old_value

                # add the difference column wise in the same row to next 2 columns
                constraint_grid[x][2][0] = constraint_grid[x][2][0] + diff

                # Condition for complaints
                if constraint_grid[x][1][0] - landing_mins - constraint_grid[x][0][0] > complain_mins:
                    constraint_grid[x][0][0] = constraint_grid[x][1][0] - landing_mins - complain_mins

                    # BT when complaints exceed and you update first column landing values
                    if constraint_grid[x][0][0] > constraint_grid[x][0][1]:
                        if plane_order[first_index] not in failed:
                            failed.append(plane_order[first_index])

                        failed_pos = []
                        for i in failed:
                            failed_pos.append(plane_order.index(i))

                        for i in xrange(num_planes):
                            if assign_planes[i] == 0 and i not in failed_pos:
                                landing_list = landing_list_copy[:]
                                service_list = service_list_copy[:]
                                takeoff_list = takeoff_list_copy[:]
                                constraint_grid = [[x[:] for x in y] for y in constraint_grid_copy]

                                plane_order[first_index], plane_order[i] = plane_order[i], plane_order[first_index]
                                constraint_grid[first_index], constraint_grid[i] = constraint_grid[i], \
                                                                                   constraint_grid[first_index]

                                plane_pos[first_index], plane_pos[i] = plane_pos[i], plane_pos[first_index]
                                flag = True
                                break
            else:
                min_land_gate_free = min(min_land_gate_free, constraint_grid[x][2][0])
        if flag == True:
            break
    if flag == True:
        continue
    assign_planes[first_index] = 1
    failed = []

# print constraint_grid


for each in xrange(num_planes):
    l_time = constraint_grid[plane_pos[each]][0][0]
    t_time = constraint_grid[plane_pos[each]][1][0]
    f_out.write(str(l_time)+" "+str(t_time))
    f_out.write("\n")
