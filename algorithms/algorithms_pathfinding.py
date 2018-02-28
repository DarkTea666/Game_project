import math

def tile_score(map_layer, i, j, t_i, t_j):
        if abs(t_i - i) > abs(t_j - j):
            est_distance = abs(t_i - i)
        else:
            est_distance = abs(t_j - j)
        scored_tile = {'i': i, 'j': j, 'value': map_layer[i][j],
                       'g': 0, 'h': est_distance}
        return scored_tile

def in_list(tile, a_list):
        result = False
        for l in a_list:
            if l['i'] == tile['i'] and l['j'] == tile['j']:
                result = l
        return result

def find_min_score(open_list):
        minimum_score = math.inf
        minimum_tile = False
        for tile in open_list:
            if tile['g'] + tile['h'] < minimum_score:
                minimum_score = tile['g'] + tile['h']
                minimum_tile = tile
        return minimum_tile

def tile_do(tile, map_layer, open_list, closed_list, t_i, t_j, blocked_tiles): #for each new
        if tile in open_list:
                open_list.remove(tile)                            
                closed_list.append(tile)
                for neighbor_tile in map_layer.neighbor_tiles(tile['i'],
                                                              tile['j']):
                    if neighbor_tile[2] == 0 and (neighbor_tile[0], neighbor_tile[1]) not in blocked_tiles:
                        ''' and not check_for_mob(mobs, map_layer,neighbor_tile[1],neighbor_tile[0]):'''
                        n_tile = tile_score(map_layer,
                                            neighbor_tile[0],
                                            neighbor_tile[1],
                                            t_i,t_j)
                        if in_list(n_tile,closed_list) == False:
                            t = tile_score(map_layer, n_tile['i'],
                                           n_tile['j'],
                                           t_i,t_j)
                            t['g'] = tile['g'] + 1
                            if in_list(n_tile, open_list) == False:
                                open_list.append(t)
                            elif in_list(n_tile, open_list) != False:
                                old_tile = in_list(n_tile, open_list)
                                if old_tile['g'] > t['g']:
                                    open_list.remove(old_tile)
                                    open_list.append(t)

def pathfind_to_target(map_layer, s_i, s_j, t_i, t_j, blocked_tiles):

        target_tile = tile_score(map_layer, t_i, t_j, t_i, t_j)
        neighbors = map_layer.neighbor_tiles(s_i, s_j)

        open_list = [tile_score(map_layer, tile[0], tile[1], t_i, t_j)
                     for tile in neighbors if tile[2] == 0 and (tile[0], tile[1]) not in blocked_tiles]
        '''and not check_for_mob(mobs, map_layer, tile[1], tile[0])]'''

        closed_list = [tile_score(map_layer, s_i, s_j, t_i, t_j)]

        while in_list(target_tile, open_list) == False and open_list != []:
                min_tile = find_min_score(open_list)
                tile_do(min_tile, map_layer, open_list, closed_list, t_i, t_j, blocked_tiles)

        return trace_back_path(map_layer, s_i, s_j, t_i, t_j, open_list, closed_list)

def trace_back_path(map_layer, s_i, s_j, t_i, t_j, open_list, closed_list):
        for tile in open_list:
            if tile['h'] == 0:
                g = tile['g']
        path_list = []
        io = t_i
        jo = t_j
        if open_list != []:
            while g != 0:
                    for tile in closed_list:
                        if tile['g'] == g - 1 and (io,jo,0) in map_layer.neighbor_tiles(tile['i'],tile['j']):
                            key_first = False
                            g = tile['g']
                            io = tile['i']
                            jo = tile['j']
                            path_list.insert(0, (tile['i'], tile['j']))
            path_list.append((t_i, t_j))
        return path_list

