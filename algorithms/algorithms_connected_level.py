def connected_level(map_layer):
    floor_count = 0
    for i in range(len(map_layer.map)):
        for j in range(len(map_layer[0])):
            if map_layer[i][j] == 0:
                floor_count += 1
                last_tile = (i,j)
    new_list = [last_tile]
    old_list = []
    next_list = []
    key = True
    while key:    
        for tile in new_list:
            i,j = tile
            this_next_list = new_tile_do(i, j, map_layer, old_list, new_list)
            for t in this_next_list:
                next_list.append(t)
            old_list.append(t)
        if next_list == []:
            key = False
        new_list = []
        for t in next_list:
            new_list.append(t)
            old_list.append(t)
        next_list = []
        old_list = list(set(old_list))
    print('floor_count:',floor_count)
    print(old_list)
    print('len old_list:', len(old_list))
    return old_list


def new_tile_do(i, j, map_layer, old_list, new_list):
    next_list = []
    for tile in map_layer.neighbor_tiles(i, j):
        i,j,val = tile
        if (i,j) not in old_list and (i,j) not in new_list and val == 0:
            next_list.append((i,j))
    return next_list




