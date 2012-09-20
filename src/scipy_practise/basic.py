'''
Created on 2012-7-10

@author: guoxc
'''
import scipy as sp
import scipy.linalg
import math
a = sp.array([1,2,3,4])
#print a
#c = sp.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
#print c
#print a.shape
#print c.shape
#print c.reshape((2,-1))
#print sp.arange(0,1,10)
#print sp.linspace(0,1,10)
def choose_from_de(value,distribution,mean_less=1):
    BASE = 10000000
    assert len(value) == len(distribution)
    r = int(BASE * sum(distribution))
    x = sp.random.randint(r)
    j = 0
    for i in range(0,len(value)):
        x -= distribution[i] * BASE 
        if x < 0:
            j = i
            break
    else:
        j = i
    return value[j]
def sigmoid(y):
    return 1.0 / (1 + math.exp(-y))
def tanh(y):
    if abs(y) > 400:
        return 1.0
    return (math.exp(y) - math.exp(-y)) / (math.exp(y) + math.exp(-y))

sigmoid_ufunc = sp.frompyfunc(sigmoid, 1, 1)
tanh_ufunc = sp.frompyfunc(tanh, 1, 1)
class EchoNetwork(object):

    def __init__(self, unit_type_ufunc=None, input_unit_amount=1, internal_unit_amount=100, output_unit_amount=1,
                 has_feedback=False,
                 state=None, input_matrix=None, 
                 internal_matrix=None, feedback_matrix=None,):
        if state:
            self.state = sp.array(state).T
        else:
            self.state = sp.rand(internal_unit_amount,1)
        self.unit_type_ufunc = unit_type_ufunc
        self.internal_unit_amount = internal_unit_amount
        self.input_unit_amount = input_unit_amount
        self.output_unit_amount = output_unit_amount
        self.has_feedback = has_feedback
        self._config(input_matrix, internal_matrix, feedback_matrix)
        self.state_history = []
        self.output_history = []
#        print "state.shape=" + str(self.state.shape)

    def _config(self, input_matrix=None, internal_matrix=None, feedback_matrix=None):
        if input_matrix:
            self.input_matrix = input_matrix
        else:
            if self.input_unit_amount != 0:
                self.input_matrix = sp.rand(self.internal_unit_amount,self.input_unit_amount)
            else:
                self.input_matrix = None
        if internal_matrix != None:
            self.internal_matrix = internal_matrix
        else:
            self.internal_matrix = sp.rand(self.internal_unit_amount,self.internal_unit_amount)
        if self.has_feedback:
            if feedback_matrix != None:
                self.feedback_matrix = feedback_matrix
            else:
                self.feedback_matrix = sp.rand(self.internal_unit_amount, self.output_unit_amount)
        else:
            self.feedback_matrix = None
        if self.feedback_matrix != None:
            self.output = sp.zeros((1,self.output_unit_amount))
        self.output_matrix = sp.randn(self.internal_unit_amount+self.input_unit_amount,self.output_unit_amount)

    def update_step(self, input_signal=None, teaching_signal=None):
        """update the network with the given input and teach_output, input_signal and teaching_signal must be a column vector
        notice that input_signal is u(n+1) and output is output(n+1) 
        this step makes state(n) -> state(n+1)
        the x_history is a list of state's state_history , every item is a row vector like (100L,)"""

        if input_signal != None:
            assert input_signal.shape == (self.input_unit_amount, 1)
        if teaching_signal != None:
            assert teaching_signal.shape == (self.output_unit_amount, 1)

        if self.feedback_matrix != None and self.input_matrix != None:
            self.state = self.unit_type_ufunc(sp.dot(self.input_matrix, input_signal) + sp.dot(self.internal_matrix, self.state) + sp.dot(self.feedback_matrix, self.output))
            if teaching_signal == None:
                self.output = sp.dot(self.output_matrix, sp.append(input_signal.T,self.state.T).T)
            else:
                self.output = teaching_signal
        elif self.feedback_matrix != None:
            self.state = self.unit_type_ufunc(sp.dot(self.internal_matrix, self.state) + sp.dot(self.feedback_matrix, self.output))
            if teaching_signal == None:
                self.output = sp.dot(self.output_matrix, self.state)
            else:
                self.output = teaching_signal
        else:
            self.state = self.unit_type_ufunc(sp.dot(self.input_matrix, input_signal) + sp.dot(self.internal_matrix, self.state))
        if input_signal != None:
            self.state_history.append(sp.append(input_signal.T, self.state.T))
        else:
            self.state_history.append(self.state.reshape(-1))
        self.output_history.append(self.output)

    def func_learn(self,input_func,teaching_func,steps=500,threshold=100):
        """input_func and y_teach must return a column vector (shape is like (100L,1L))
        even if there's only one input/output the function must return a vector which shape is like (1L,1L)"""
        assert input_func.shape == (self.input_unit_amount, 1) and teaching_func == (self.output_unit_amount, 1)
        assert threshold < steps

        print "updating"
        for i in range(0,steps):
            u_in = sp.array([input_func(i)]).T
            y_teach= sp.array([teaching_func(i)]).T
            self.update_step(u_in, y_teach)
        x_history = sp.array(self.state_history[threshold:])
        print "learning"
        y_teach = sp.array([teaching_func(i) for i in range(threshold,steps)])
        self.output_matrix = scipy.linalg.lstsq(x_history,y_teach)[0].T
#        print "x_histroy=" + str(x_history)
#        print "y_teach="+str(y_teach.T)
#        print "output_matrix=" + str(self.output_matrix) + "shape" + str(self.output_matrix.shape)
#        print "err=" + str(y_teach - sp.dot(self.output_matrix,x_history.T).T)

    def func_feedback_learn(self,teaching_func,steps=500,threshold=100):
        print "updating"
        for i in range(0,steps):
            y_teach= sp.array([teaching_func(i)]).T
            self.update_step(teaching_signal=y_teach)
        x_history = sp.array(self.state_history[threshold:])
        print "learning"
        y_teach = sp.array([teaching_func(i) for i in range(threshold,steps)])
        self.output_matrix = scipy.linalg.lstsq(x_history,y_teach)[0].T
#        print "output_matrix=" + str(self.output_matrix) + "shape" + str(self.output_matrix.shape)
#        print "err=" + str(y_teach - sp.dot(self.output_matrix,x_history.T).T)

    def check(self,input_signal,teaching_signal):
        if input_signal != None:
            input_signal = sp.array([input_signal])
        teaching_signal = sp.array([teaching_signal])
        self.update_step(input_signal=input_signal,teaching_signal=None)
#        print teaching_signal.shape,self.output_matrix.shape, input_signal.T.shape,self.state.T.shape
#        if input_signal != None:
#            print "err=" + str(teaching_signal - sp.dot(self.output_matrix,sp.append(input_signal.T,self.state.T).T))
#        else:
#            print "err=" + str(teaching_signal - sp.dot(self.output_matrix,self.state))
            
        
    def biggest_eigenvalue_w(self):
        return abs(max(scipy.linalg.eig(self.internal_matrix)[0]))
        
class LeakyEchoNetwork(EchoNetwork):
    
    def __init__(self, decay_rate=0.94, time_constant=0.5, step_size=1, *args, **kargs):
        EchoNetwork.__init__(self, *args, **kargs)
        self.decay_rate = decay_rate
        self.time_constant = time_constant
        self.step_size = step_size
        
    def update_step(self, input_signal=None, teaching_signal=None):
        if self.feedback_matrix != None and self.input_matrix != None:
            self.state = (1 - self.step_size * self.time_constant * self.decay_rate) * self.state \
                    + self.step_size * self.time_constant * self.unit_type_ufunc(sp.dot(self.input_matrix, input_signal) + sp.dot(self.internal_matrix, self.state) + sp.dot(self.feedback_matrix, self.output))
            if teaching_signal == None:
                self.output = sp.dot(self.output_matrix, sp.append(input_signal.T,self.state.T).T)
            else:
                self.output = teaching_signal
        elif self.feedback_matrix != None:
            self.state = (1 - self.step_size * self.time_constant * self.decay_rate) * self.state \
                    + self.step_size * self.time_constant * self.unit_type_ufunc(sp.dot(self.internal_matrix, self.state) + sp.dot(self.feedback_matrix, self.output))
            if teaching_signal == None:
                self.output = sp.dot(self.output_matrix, self.state)
            else:
                self.output = teaching_signal
        else:
            self.state = (1 - self.step_size * self.time_constant * self.decay_rate) * self.state \
                    + self.step_size * self.time_constant * self.unit_type_ufunc(sp.dot(self.input_matrix, input_signal) + sp.dot(self.internal_matrix, self.state))
        if input_signal != None:
            self.state_history.append(sp.append(input_signal.T, self.state.T))
        else:
            self.state_history.append(self.state.reshape(-1))
        self.output_history.append(self.output)
        
        
def main_1():
    x = sp.rand(100).reshape(-1,1)
    w_in = sp.rand(100).reshape(-1,1) / 10
    w = sp.array([[choose_from_de([0,0.4,-0.4],[0.95,0.025,0.025]) for i in range(100)] for j in range(100)])
    w_out = sp.randn(101)
    u_in = lambda x:math.sin(x *1.0 / 5)
    x_histroy = []
    y_teach_func = lambda x: 0.5 * ( math.sin(x *1.0 / 5) ** 7 )
    y_teach = sp.array([y_teach_func(item) for item in range(500)])
    unit_type_ufunc = tanh_ufunc
    for i in range(0,500):
        x = unit_type_ufunc(w_in * u_in(i) + sp.dot(w,x) )
        x_histroy.append(sp.copy(sp.append(sp.array(u_in(i)) , x.reshape(-1))))
    print "------------------------------------------------------"
    x_histroy = sp.array(x_histroy[100:])
    print x_histroy
    print x_histroy.shape
    print y_teach[100:].shape
        
    w_out = scipy.linalg.lstsq(x_histroy,y_teach[100:].T)[0]
    print w_out
    print y_teach[100:] - sp.dot(w_out,x_histroy.T)
    
#    print state
    
#    print sd
def main_2():
    u_in_func = lambda x:sp.array([math.sin(x *1.0 / 5)])
    prices = [(float(x)-2000)/500 for x in open("../../data/shpriceindex1.dat").readlines()]
    y_teach_func = lambda x: sp.array([prices[x],])
    
#    y_teach_func = lambda x: sp.array([0.5 * ( math.sin(x *1.0 / 5) ** 7 )])+(sp.rand(1)*0.00001)
    unit_type_ufunc = sigmoid_ufunc
    w = sp.array([[choose_from_de([0,0.15,-0.15],[0.9,0.05,0.05]) for i in range(400)] for j in range(400)])
    net1 = LeakyEchoNetwork(unit_type_ufunc=unit_type_ufunc,
                       input_unit_amount=0,
                       has_feedback=True,
                       internal_unit_amount =400,
                       output_unit_amount=1,
                       internal_matrix=w,
                       )
    net1.func_feedback_learn(y_teach_func, 82, 10)
    for i in range(82,84):
        net1.update_step()
#        net1.check(input_signal=None, teaching_signal=y_teach_func(i))
    print net1.biggest_eigenvalue_w()
    import matplotlib.pyplot as plt
    range_x = (0,84)
    x = sp.arange(range_x[0],range_x[1])
#    y = sp.sin(state * 1.0 / 5)
    y = sp.array([item[2] for item in net1.state_history])[range_x[0]:range_x[1]]
    z = sp.array([item[0] for item in net1.output_history])[range_x[0]:range_x[1]]
    print z[79]*500+2000
    print z[80]*500+2000
    print z[81]*500+2000
    print z[82]*500+2000
    print z[83]*500+2000
    plt.figure(figsize=(8,4))
    plt.subplot(211)
    plt.plot(x,y,label="internal unit",color="red")
    plt.subplot(212)
    plt.plot(x,z,label="output")
    plt.xlabel("Time(s)")
    plt.ylabel("State")
    plt.title("Result")
    plt.show()

def guimain():
    import Tkinter
    top = Tkinter.Tk()
    top.geometry("400x300")
    
    def callback():
        input_amount,internal_amount,output_amount,has_feedback=eval("("+init_config_entry.get()+")")
        eval_tuple = eval(internal_matrix_entry.get())
        print type(eval_tuple)
        internal_matrix = sp.array([[choose_from_de(eval_tuple[0],eval_tuple[1]) for i in range(internal_amount)] for j in range(internal_amount)])
        print input_amount,internal_amount,output_amount,has_feedback,internal_matrix
        teach_func = lambda x : sp.array([eval(output_amount_entry.get())])+(sp.rand(1)*0.00001)
        unit_type_ufunc = tanh_ufunc
        net1 = EchoNetwork(unit_type_ufunc=unit_type_ufunc,
                       input_unit_amount=input_amount,
                       has_feedback=has_feedback,
                       internal_unit_amount=internal_amount,
                       output_unit_amount=output_amount,
                       internal_matrix=internal_matrix,
                       )
        print teach_func(23)
        net1.func_feedback_learn(teach_func, 500, 100)
        for i in range(500,1000):
            net1.check(input_signal=None, teaching_signal=teach_func(i))
        print net1.biggest_eigenvalue_w()
        import matplotlib.pyplot as plt
        range_x = (0,1000)
        x = sp.arange(range_x[0],range_x[1])
#        y = sp.sin(state * 1.0 / 5)
        y = sp.array([item[2] for item in net1.state_history])[range_x[0]:range_x[1]]
        z = sp.array([item[0] for item in net1.output_history])[range_x[0]:range_x[1]]
        plt.figure(figsize=(8,4))
        plt.subplot(211)
        plt.plot(x,y,label="internal unit",color="red")
        plt.legend()
        plt.subplot(212)
        plt.plot(x,z,label="output")
        plt.xlabel("Time(s)")
        plt.ylabel("State")
        plt.title("Result")
        plt.legend()
        plt.show()
    
    menubar = Tkinter.Menu(top)
    filemenu = Tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open",command=None)
    menubar.add_cascade(menu=filemenu,label="File")
    
    init_config_entry = Tkinter.Entry(top)
    internal_matrix_entry = Tkinter.Entry(top)
    output_amount_entry = Tkinter.Entry(top)
    set_button = Tkinter.Button(top,text="OK", command=callback)
    
    init_config_entry.insert(0,"0,100,1,True")
    internal_matrix_entry.insert(0,"[0,0.4,-0.4],[0.95,0.025,0.025]")
    output_amount_entry.insert(0,"0.5 * ( math.sin(x *1.0 / 5) ** 1/2 )")
    init_config_entry.pack(fill=Tkinter.X)
    internal_matrix_entry.pack(fill=Tkinter.X)
    output_amount_entry.pack(fill=Tkinter.X)
    set_button.pack() 
    
    top.config(menu=menubar)
    top.mainloop()
    
if __name__ == "__main__":
#    main_2()
    guimain()