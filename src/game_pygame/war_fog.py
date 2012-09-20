import pygame
import random
FOG_SIZEX = 20
FOG_SIZEY = 20
MAP_SIZEX = 500
MAP_SIZEY = 500
GRID_SIZEX = MAP_SIZEX / FOG_SIZEX
GRID_SIZEY = MAP_SIZEY / FOG_SIZEY

class FogLayer(object):
    """docstring for FogLayer"""
    def __init__(self, array=None):
        super(FogLayer, self).__init__()
        if array:
            self.array = array
        else:
            self.array = [[2 for i in range(FOG_SIZEX)]for j in range(FOG_SIZEY)]

    def light_up(self, coordinate):
        self.array[coordinate[1]][coordinate[0]] = 0

    def input_new(self, another):
        for j in range(FOG_SIZEY):
            for i in range(FOG_SIZEX):
                if self.array[j][i] == 0:
                    self.array[j][i] = 1
                self.array[j][i] = min(self.array[j][i], another.array[j][i])

    def merge_new(self, another):
        for i in range(FOG_SIZEY):
            for j in range(FOG_SIZEX):
                self.array[i][j] = min(self.array[i][j], another.array[i][j])

    @staticmethod
    def merge_fog(one, another):
        new_fog = FogLayer()
        for i in range(FOG_SIZEY):
            for j in range(FOG_SIZEX):
                new_fog.array[i][j] = min(one.array[i][j], another.array[i][j])
        return new_fog

class Player(object):
    """docstring for Player"""
    def __init__(self, avatar, fog_history, stage):
        super(Player, self).__init__()
        self.avatar = avatar
        self.fog_history = fog_history
        self.stage = stage

    def update_sight(self, terrain):
        self.fog_history.input_new(self.avatar.get_sight(terrain=terrain))

    def get_view(self):
        return self.stage.get_team_history(self.avatar.team)

class VObj(object):
    def __init__(self, coordinate, sight_range, team=1, vtype=0, ltime=0):
        self.coordinate = coordinate
        self.sight_range = sight_range
        self.team = team
        self.vtype = vtype
        self.ltime = ltime

    def random_move(self):
        randint = random.randrange(-50, 50)
        coa = self.coordinate[0] + randint
        if coa >= MAP_SIZEX or coa < 0:
            coa = self.coordinate[0]
        randint = random.randrange(-50, 50)
        cob = self.coordinate[1] + randint
        if cob >= MAP_SIZEX or cob < 0:
            cob = self.coordinate[1]
        self.coordinate = (coa, cob)

    def move(self, vec , step=1):
        coa = self.coordinate[0] + step * vec[0]
        if coa >= MAP_SIZEX or coa < 0:
            coa = self.coordinate[0]
        cob = self.coordinate[1] + step * vec[1]
        if cob >= MAP_SIZEX or cob < 0:
            cob = self.coordinate[1]
        self.coordinate = (coa, cob)

    def get_sight(self, terrain=None):
        x, y = self._get_grid_coordinate()
        sight_left = max(0, int(x - self.sight_range))
        sight_up = max(0, int(y - self.sight_range))
        sight_right = min(FOG_SIZEX - 1, int(x + self.sight_range))
        sight_down = min(FOG_SIZEY - 1, int(y + self.sight_range))
        fog = FogLayer()
        def distance(ax, ay):
            return ((ax - x) ** 2 + (ay - y) ** 2) ** 0.5
        def bresenham(ax, ay):
            # k = float(ay - y)  / float(ax - x)
            line = []
            bx = x
            by = y
            dx = abs(ax - x)
            dy = abs(ay - y)
            sx = ax - x > 0
            sy = ay - y > 0
            if dy < dx:
                e = 2 * dy - dx
                for i in range(0, dx):
                    line.append((bx, by))
                    if(e >= 0):
                        by += 1 if sy else -1
                        e -= 2 * dx
                    bx += 1 if sx else -1
                    e += 2 * dy
                return line
            else:
                e = 2 * dx - dy
                for i in range(0, dy):
                    line.append((bx, by))
                    if(e >= 0):
                        bx += 1 if sx else -1
                        e -= 2 * dy
                    by += 1 if sy else -1
                    e += 2 * dx
                return line
        for j in range(sight_up, sight_down + 1):
            for i in range(sight_left, sight_right + 1):
                if distance(i, j) <= self.sight_range:
                    if self.vtype == 0:
                        for rl in bresenham(i, j):
                            if terrain[rl[1]][rl[0]] > terrain[y][x]:
                                break
                        else:
                            fog.light_up((i, j))
                    else:
                        fog.light_up((i, j))
        return fog

    def _get_grid_coordinate(self):
        return (self.coordinate[0] / GRID_SIZEX, self.coordinate[1] / GRID_SIZEY)

class SObj(object):
    def __init__(self, coordinate):
        self.coordinate = coordinate

    def random_move(self):
        randint = random.randrange(-50, 50)
        coa = self.coordinate[0] + randint
        if coa >= MAP_SIZEX or coa < 0:
            coa = self.coordinate[0]
        randint = random.randrange(-50, 50)
        cob = self.coordinate[1] + randint
        if cob >= MAP_SIZEX or cob < 0:
            cob = self.coordinate[1]
        self.coordinate = (coa, cob)

    def move(self, vec , step=10):
        coa = self.coordinate[0] + step * vec[0]
        if coa >= MAP_SIZEX or coa < 0:
            coa = self.coordinate[0]
        cob = self.coordinate[1] + step * vec[1]
        if cob >= MAP_SIZEX or cob < 0:
            cob = self.coordinate[1]
        self.coordinate = (coa, cob)
    
    
class Stage(object):
    """docstring for Stage"""
    def __init__(self, vobjs=[], sobjs=[]):
        super(Stage, self).__init__()
        self.vobjs = vobjs
        self.sobjs = sobjs
        self.team_history = {}
        self.bind = []
    
    def add_new_obj(self, coordinate, sight_range=4, team=1):
        sobj = SObj(coordinate)
        vobj = VObj(coordinate, sight_range, team=team)
        self.sobjs.append(sobj)
        self.vobjs.append(vobj)
        self.bind.append((sobj,vobj))
        return sobj
    
    def add_new_vobj(self, vobj):
        self.vobjs.append(vobj)
        sobj = SObj(vobj.coordinate)
        self.sobjs.append(sobj)
        self.bind.append((sobj,vobj))
        return sobj

    def init_team_history(self, team=1):
        if team in self.team_history:
            return
        else:
            self.team_history[team] = self.get_team_sight(team)

    def get_team_sight(self, team=1):
        team_sight = FogLayer()
        for vobj in self.vobjs:
            if vobj.team == team or vobj.team == 0:
                team_sight.merge_new(vobj.get_sight(terrain=terrain))
        return team_sight

    def update(self):
        for team in range(1,3):
            self.update_team_history(team)
        for sobj,vobj in self.bind:
            vobj.coordinate = sobj.coordinate

    def update_team_history(self, team=1):
        if team not in self.team_history:
            self.init_team_history(team)
        self.team_history[team].input_new(self.get_team_sight(team))

    def get_team_history(self, team):
        if team not in self.team_history:
            self.init_team_history(team)
        return self.team_history[team]



def coordinate2grid(coordinate):
    gridx = coordinate[0] / GRID_SIZEX
    gridy = coordinate[1] / GRID_SIZEY
    return (gridx, gridy)

def grid2coordinate(gridxy):
    coordinate1 = gridxy[0] * GRID_SIZEX
    coordinate2 = gridxy[1] * GRID_SIZEY
    return (coordinate1, coordinate2)

def choose_from_de(value, distribution, mean_less=1):
    BASE = 10000000
    assert len(value) == len(distribution)
    r = int(BASE * sum(distribution))
    x = random.randrange(r)
    j = 0
    for i in range(0, len(value)):
        x -= distribution[i] * BASE 
        if x < 0:
            j = i
            break
    else:
        j = i
    return value[j]

terrain = [[choose_from_de([0, 1, 2, 3], [0.9, 0.1, 0, 0]) for i in range(FOG_SIZEX)] for j in range(FOG_SIZEY)]

def load_resource(res_list=[]):
    res = {}
    for item in res_list:
        res[item[0]] = pygame.image.load(item[1]).convert()
        if len(item) >= 3:
            res[item[0]].set_alpha(item[2])
    return res

def draw_fog(screen, resource, fog):
    for j in range(FOG_SIZEY):
        for i in range(FOG_SIZEX):
            if terrain[j][i] == 1:
                screen.blit(resource["red"], grid2coordinate((i, j)), (0, 0, GRID_SIZEX, GRID_SIZEY))
            if fog.array[j][i] == 1:
                screen.blit(resource["black_alpha"], grid2coordinate((i, j)), (0, 0, GRID_SIZEX, GRID_SIZEY))
            elif fog.array[j][i] == 2:
                screen.blit(resource["black"], grid2coordinate((i, j)), (0, 0, GRID_SIZEX, GRID_SIZEY))
            else:
                pass

def draw_background(screen, resource):
    screen.blit(resource["background"], (0, 0))

def draw_obj(screen, resource, fog, stage):
    for sobj in stage.sobjs:
        i, j = coordinate2grid(sobj.coordinate)
        if fog.array[j][i] == 0:
            screen.blit(resource["player_pic"], sobj.coordinate, (0, 0, 10, 10))

def main():
    # c = FogLayer.merge_fog(a,b)
    r = VObj((0, 0), 6)
    x = r.get_sight(terrain=terrain).array
    for line in x:
        print line

def game_main():
    from pygame.locals import QUIT,K_UP,K_DOWN,K_RIGHT,K_LEFT
    pygame.init()
    screen = pygame.display.set_mode((MAP_SIZEX, MAP_SIZEY), 0, 32)
    res_list = [("background", "resource/landscape.jpg"),
                ("player_pic", "resource/player.bmp"),
                ("black", "resource/black.jpg", 200),
                ("black_alpha", "resource/black.jpg", 100),
                ("red", "resource/red.jpg", 200)]
    resource = load_resource(res_list)
    clock = pygame.time.Clock()
    player_avatar = VObj((200, 200), 4)
    stage = Stage()
    sobj2 = stage.add_new_obj((200, 250), 3)
    sobj1 = stage.add_new_obj((400, 350), 2, team=2)
    player_sobj = stage.add_new_vobj(player_avatar)
    time_passed = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        pressed_keys = pygame.key.get_pressed()
        move_vec = [0, 0]
        if pressed_keys[K_UP]:
            move_vec[1] += -1 
        if pressed_keys[K_DOWN]:
            move_vec[1] += 1 
        if pressed_keys[K_LEFT]:
            move_vec[0] += -1 
        if pressed_keys[K_RIGHT]:
            move_vec[0] += 1 
        player_sobj.move(move_vec)
        stage.update()
        # player.update_sight(terrain)

        time_passed += clock.tick(10)
        if time_passed >= 1000:
            sobj1.random_move()
            sobj2.random_move()
            time_passed = 0
        draw_background(screen, resource)
        # new_sight = player.avatar.get_sight(terrain=terrain)
        # player.fog_history.input_new(new_sight)
        draw_fog(screen, resource, stage.get_team_history(1))
        draw_obj(screen, resource, stage.get_team_history(1), stage)
        # screen.blit(resource["player_pic"],(player.avatar.coordinate[0]-GRID_SIZEX/2,
                    # player.avatar.coordinate[1] - GRID_SIZEY/2),(0,0,GRID_SIZEX,GRID_SIZEY))

        pygame.display.update()

if __name__ == '__main__':
    game_main()            
        
