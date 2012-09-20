import Tkinter
import copy
class model(object):
    """docstring for model"""
    def __init__(self, origin=[0,1,2,3,4,5,6,7,8], target=[1,2,3,4,5,6,7,8,0]):
        super(model, self).__init__()
        self.v = origin
        xy = self.v.index(0)
        self.x = xy%3
        self.y = xy/3
        self.target = target
    def act(self, direction="left"):
        if direction == "left":
            if self.x == 0:
                error()
                return False
            else:
                self.v[self.x + self.y * 3], self.v[self.x + self.y * 3 - 1] = \
                self.v[self.x + self.y * 3 - 1], self.v[self.x + self.y * 3]
                self.x -= 1
                return True
        elif direction == "right":
            if self.x == 2:
                error()
                return False
            else:
                self.v[self.x + self.y * 3], self.v[self.x + self.y * 3 + 1] = \
                self.v[self.x + self.y * 3 + 1], self.v[self.x + self.y * 3]
                self.x += 1
                return True
        elif direction == "up":
            if self.y == 0:
                error()
                return False
            else:
                self.v[self.x + self.y * 3], self.v[self.x + (self.y - 1) * 3] = \
                self.v[self.x + (self.y - 1) * 3], self.v[self.x + self.y * 3]
                self.y -= 1
                return True
        elif direction == "down":
            if self.y == 2:
                error()
                return False
            else:
                self.v[self.x + self.y * 3], self.v[self.x + (self.y + 1) * 3] = \
                self.v[self.x + (self.y + 1) * 3], self.v[self.x + self.y * 3]
                self.y += 1
                return True

    def act_test(self, direction="left"):
        if direction == "left":
            if self.x == 0:
                return False
            else:
                return True
        elif direction == "right":
            if self.x == 2:
                return False
            else:
                return True
        elif direction == "up":
            if self.y == 0:
                return False
            else:
                return True
        elif direction == "down":
            if self.y == 2:
                return False
            else:
                return True

    def show(self):
    	for i in range(3):
    		print self.v[i * 3:(i + 1)*3]
    	print "x,y = " + str(self.x)+ ","+str(self.y)

    def check(self):
    	if self.v == self.target:
    		return True
    	else:
    		return False

    def getstr(self):
        return "".join([str(item) for item in self.v])

    @staticmethod
    def construct(state_str):
        origin =[int(i) for i in state_str]
        xandy = state_str.find("0")
        xandy = xandy%3,xandy/3
        return model(origin=origin, xy=xandy)

    def distance_mahaton(self):
        re = 0
        for i in range(9):
            should = self.target.index(self.v[i])
            dis = abs(i/3 - should/3) + abs(i%3 - should%3)
            re += dis
        return re

class node(object):
    """node class for tree_search"""
    def __init__(self, state=model(), parent_node=None, action="", path_cost=0, depth=0):
        super(node, self).__init__()
        self.state = state
        self.parent_node = parent_node
        self.action = action
        self.path_cost = path_cost
        self.depth = depth

    def expand(self):
        new_nodes = []
        for act in ["left","right","up","down"]:
            if self.state.act_test(direction=act):
                m = copy.deepcopy(self.state)
                m.act(act)
                new_nodes.append(node(state=m, parent_node=self, action=act, path_cost=self.path_cost+1, depth=self.depth+1))
        return new_nodes



def error(msg=None):
    if msg != None:
        print msg
    else:
        print "ERROR"

def find_dfs_solution(start=None):
    """the start arg is a model object which shows the state"""
    def temp(node,gone,step,intend=0,limit=10):
        if intend >= limit:
            return False
        if node.state.check():
            step.append(node.action)
            return True
        for item in node.expand():
            if item.state.getstr() in gone: 
                if item.depth >= gone[item.state.getstr()]:
                    continue
                else:
                    gone[item.state.getstr()] = item.depth
            else:
                gone[item.state.getstr()] = item.depth
            if temp(item,gone,step,intend=intend+1,limit=limit):
                step.append(node.action)
                return True
        return False

    def warptemp(m,limit=10):
        gone = {}
        root = node(state=m, parent_node=None, action="")
        gone[m.getstr()] = 0 
        n = root
        step = []
        if temp(n,gone,step,limit=limit) == True:
            return step
        else:
            return None

    if start != None:
        m = start
    else:
        m = model()
    limit_1 = 5
    while limit_1 <= 30:
        step = warptemp(m,limit=limit_1);
        if step != None:
            break
        limit_1 += 5
    print "limit=%s" % (limit_1,)
    step.reverse()
    return step[1:]

def find_bfs_solution(start=None):
    if start != None:
        m = start
    else:
        m = model()
    



def guimain(q=None,a=None):
    top = Tkinter.Tk()
    labels = []
    strvars = []
    reverse = {"up":"down","down":"up","left":"right","right":"left"}
    if q == None:
        m = model()
    else:
        m = q
    print m.v
    for i in range(9):
        strvar = Tkinter.StringVar()
        strvar.set(str(m.v[i]))
        label = Tkinter.Label(top,textvariable=strvar)
        label.grid(row=i/3, column=i%3)
        strvars.append(strvar)
        labels.append(label)
    strvar = Tkinter.StringVar()
    strvar.set("mahaton distance = %s" % m.distance_mahaton())
    label = Tkinter.Label(top,textvariable=strvar)
    label.grid(row=3, columnspan=3)
    if q != None:
        solution_list = Tkinter.Listbox(top)
        solution_list.grid(row=4,columnspan=3)
        for i in a:
            solution_list.insert(Tkinter.END, reverse[i])

    def show(model):
        for index,letter in enumerate(model.getstr()):
            strvars[index].set(letter)
            if letter == "0":
                strvars[index].set("")
        strvar.set("mahaton distance = %s" % m.distance_mahaton())
    def callback(event):
        mvd = {"s":"up","w":"down","a":"right","d":"left"}
        if event.char in mvd:
            m.act(direction=mvd[event.char])
        else:
            print event.char
        show(m)
        if m.check():
            top.destroy()
    top.bind("<Key>", callback)
    top.mainloop()

	# while m.check != True: 
    #   m.show() a = input("direction=")
	# 	if a == 0:
	# 		m.act(direction="right")
	# 	elif a == 1:
	# 		m.act(direction="down")
	# 	elif a == 2:
	# 		m.act(direction="up")
	# 	elif a == 3:
	# 		m.act(dircetion="left")
	# 	else:
	# 		error()

def main():
    pass

def best_first_search():
    pass
    
if __name__ == '__main__':
    start = model(origin=[2,0,3,1,8,5,4,7,6],target=[1,2,3,4,5,6,7,8,0])
    step = find_dfs_solution(start)
    guimain(q=start,a=step)
	# guimain()
