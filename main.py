import pygame
import json

pygame.quit()
pygame.init()

all_nodes = []
all_sq = []
path = []

start, end = (0, 0), (24, 24)

with open('grid.json', 'r') as f:
    layout = json.loads(f.read())

marg = 50
disX = disY = 800 + (2*marg)
dis = pygame.display.set_mode((disX, disY))
block = (disX - (2*marg)) // (len(layout))

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255) 


class Node:
    def __init__(self, current=None, parent=None, startB=False, endB=False):
        self.start = startB
        self.end = endB
        self.current = current
        self.parent = parent
        self.manhattan = ((current[0] - end[0])**2) + ((current[1] - end[1])**2) \
            + ((current[0] - start[0])*2) + ((current[1] - start[1])*2)


class Board:
    def __init__(self, start=(0, 0), end=(9, 9)):    
        self.start = start
        self.end = end
        self.layout = layout

        all_nodes.append(Node(current=self.start, startB=True))

    def manhattan(self, all_sq=[start]):
        open_sq = [[], []]

        reset()

        for xy in all_sq:
            for xyc in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                xyn = (xy[0] + xyc[0], xy[1] + xyc[1])
                if len(self.layout) > xyn[0] > -1 and len(self.layout[0]) > xyn[1] > -1:
                    if xyn not in all_sq and self.layout[xyn[1]][xyn[0]] != 1:
                        open_sq[0].append(Node(xyn))
                        open_sq[1].append(Node(xyn).manhattan)
                        if xyn == end:
                            all_nodes.append(Node(xyn, xy, endB=True))
                            return create_path(Node(xyn, xy))
                        all_nodes.append(Node(xyn, xy))                     
        
        smallest_manhattan = min(open_sq[1])

        while open_sq[1].count(smallest_manhattan) > 0:
            all_sq.append(open_sq[0][open_sq[1].index(min(open_sq[1]))].current)
            # print(min(open_sq[1]), open_sq[0][open_sq[1].index(min(open_sq[1]))].current)
            open_sq[1].remove(min(open_sq[1]))
            open_sq[0].pop(open_sq[1].index(min(open_sq[1])))

        all_sq = list(dict.fromkeys(all_sq))

        # print('new\n')

        return grid.manhattan(all_sq)


def main():
    global all_nodes, all_sq, path
    buttons = create_buttons()

    while True:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()

                        if event.type == pygame.MOUSEBUTTONUP:
                            main()

                        else:
                            xy = pygame.mouse.get_pos()
                            for buttons_lis in buttons:
                                for button in buttons_lis:
                                    if button.collidepoint(xy):
                                        grid.layout[buttons.index(buttons_lis)][buttons_lis.index(button)] = 1
                        
                        reset()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    all_nodes = [Node(current=grid.start, startB=True)]
                    all_sq = []
                    path = []
                    path = grid.manhattan()

                if event.key == pygame.K_c:
                    all_nodes = [Node(current=grid.start, startB=True)]
                    all_sq = []
                    path = []

                    with open('grid.json', 'r') as f:
                        grid.layout = json.loads(f.read())
        reset()

def create_path(node):
    for xy in all_nodes:
        if node.start:
            path.append(start)
            return path[::-1]
        if node.parent == xy.current:
            path.append(node.current)
            return create_path(xy) 
    
    return path[::-1]


def create_buttons():
    buttons = []
    
    for y in range(len(grid.layout)):
        buttons_t = []
        for x in range(len(grid.layout[y])):
            if grid.layout[y][x] != start or grid.layout[y][x] != end:
                buttons_t.append(pygame.Rect(marg + (x*block), marg + (y*block), block, block))
        buttons.append(buttons_t)

    return buttons

def reset():
    dis.fill(WHITE)

    for node in all_nodes:
        if not node.start and not node.end:
            pygame.draw.rect(dis, BLUE, (marg + (node.current[0]*block), marg + (node.current[1]*block), block, block))

    for xy in path:
        pygame.draw.rect(dis, PURPLE, (marg + (xy[0]*block), marg + (xy[1]*block), block, block))

    for y in range(len(grid.layout)):
        for x in range(len(grid.layout[y])):
            if grid.layout[y][x] == 1:
                pygame.draw.rect(dis, BLACK, (marg + (x*block), marg + (y*block), block, block))

    pygame.draw.rect(dis, RED, (marg + (start[0]*block), marg + (start[1]*block), block, block))
    pygame.draw.rect(dis, RED, (marg + (end[0]*block), marg + (end[1]*block), block, block))

    pygame.draw.line(dis, BLACK, (marg, marg - 2), (marg, disY-marg + 2), 5)
    pygame.draw.line(dis, BLACK, (marg - 2, marg), (disX-marg + 2, marg), 5)
    pygame.draw.line(dis, BLACK, (disX-marg, marg - 2), (disX-marg, disY-marg + 2), 5)
    pygame.draw.line(dis, BLACK, (marg - 2, disY-marg), (disX-marg + 2, disY-marg), 5)
    for x in range(marg, disX-marg, block):
        pygame.draw.line(dis, BLACK, (x, marg), (x, disY-marg), 1)
    for y in range(marg, disY-marg, block):
        pygame.draw.line(dis, BLACK, (marg, y), (disX-marg, y), 1)   

    pygame.display.update()


if __name__ == '__main__':
    grid = Board(start, end)
    main()
