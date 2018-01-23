def one_octant(x0, y0, x1, y1):
    result = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    error = 0
    derr = dy
    y = int(y0)
    for x in range(int(x0),int(x1)+1):
        result.append((x,y))
        error = error + derr
        if 2 * error >= dx:
            y = y + 1
            error = error - dx
    return result

def tile_line(x0, y0, x1, y1,):
    if x1>=x0 and y1>=y0 and abs(x1-x0)>=abs(y1-y0):#7
        return [(x,y) for x,y in one_octant(x0,y0,x1,y1)]#7
    elif x1>=x0 and y1>=y0 and abs(x1-x0)<=abs(y1-y0):#6
        return [(y,x) for x,y in one_octant(y0,x0,y1,x1)]#6
    elif x1>=x0 and y1<=y0 and abs(x1-x0)>=abs(y1-y0):#0
        return [(x,-y) for x,y in one_octant(x0,-y0,x1,-y1)]#0
    elif x1>=x0 and y1<=y0 and abs(x1-x0)<=abs(y1-y0):#1
        return [(y,-x) for x,y in one_octant(-y0,x0,-y1,x1)]#1
    elif x1<=x0 and y1<=y0 and abs(x1-x0)<=abs(y1-y0):#2
        return [(-y,-x) for x,y in one_octant(-y0,-x0,-y1,-x1)]#2
    elif x1<=x0 and y1<=y0 and abs(x1-x0)>=abs(y1-y0):#3
        return [(-x,-y) for x,y in one_octant(-x0,-y0,-x1,-y1)]#3
    elif x1<=x0 and y1>=y0 and abs(x1-x0)>=abs(y1-y0):#4
        return [(-x,y) for x,y in one_octant(-x0,y0,-x1,y1)]#4
    elif x1<=x0 and y1>=y0 and abs(x1-x0)<=abs(y1-y0):#5
        return [(-y,x) for x,y in one_octant(y0,-x0,y1,-x1)]#5

def distance(i0, j0, i1, j1):
    return ( (abs(i0-i1)**2 + (abs(j0-j1)**2) )**0.5 )

def border_tile_vis(w_x, w_y, j, i, map_layer):
    line_list = tile_line(w_x+0.5, w_y+0.5, j+0.5, i+0.5)
    key = True
    stop_tile = line_list[0]#in case of starting from a wall (shouldn't happen) 
    for tile in line_list:
        j, i = tile
        if map_layer[i][j] != 0 and key == True:
            key = False
            stop_tile = tile
            break
    stop_ind = line_list.index(stop_tile)
    result_list = []
    for ind in range(0,stop_ind+1):
        result_list.append(line_list[ind])
    result_list = [(y,x) for x,y in result_list] 
    return result_list


def calculate_visibility(w_i, w_j, map_layer, visualise_in_text = False):
    vis_list = []
    for j in range(0,len(map_layer[0])):#upper border
        vis_list += border_tile_vis(w_j, w_i,
                                        j, 0, map_layer)
    for j in range(0,len(map_layer[0])):#lower
        vis_list += border_tile_vis(w_j, w_i,
                                    j, len(map_layer.map)-1,
                                    map_layer)
    for i in range(0,len(map_layer.map)):#left
        vis_list += border_tile_vis(w_j, w_i,
                                    0, i, map_layer)
    for i in range(0,len(map_layer.map)):#right
        vis_list += border_tile_vis(w_j, w_i,
                                        len(map_layer[0])-1, i, map_layer)
    if visualise_in_text:
        map_layer.mark()#visualise in shell
        print('-----------------------------------------------')
        vis_list = set(vis_list)
        for i in range(len(map_layer.map)):
            row = []
            for j in range(len(map_layer[0])):
                if (i,j) == (w_i, w_j):
                    row.append('*')
                elif (i,j) in vis_list:
                    row.append(map_layer[i][j])
                else:
                    row.append('#')
            print(*row)

    return [[map_layer[i][j] if ((i,j) in vis_list) else '#' for j
             in range(0, len(map_layer[0]))] for i in range(len(map_layer.map))]

    







