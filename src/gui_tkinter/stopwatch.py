'''
Created on 2012-5-20

@author: guoxc
'''
from Tkinter import *
import time

class StopWatch(Frame):
    msec = 50
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, **kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = False
        self.timestr = StringVar()
        self.makeWidgets()
        self._pause = False
    def makeWidgets(self):
        l = Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=2, padx=2)
    def _update(self):
        self._elapsedtime = time.time() - self._start
        if not self._pause:
            self._setTime(self._elapsedtime)
        self._timer = self.after(self.msec, self._update)
    def _unseen_update(self):
        self._elapsedtime = time.time() - self._start
        self._timer = self.after(self.msec, self._unseen_update)
    def _setTime(self, elap):
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds) *100)
        self.timestr.set('%02d:%02d:%02d' % (minutes,seconds,hseconds))
    def Start(self):
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = True
        else:
            self._pause = not self._pause
    def Stop(self):
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = False
    def Reset(self):
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)
        
if __name__ == "__main__":
    def main():
        top = Tk()
        sw = StopWatch(top)
        sw.pack(side=TOP)
        start_button = Button(top, text='Start', command=sw.Start)
        start_button.pack(side=LEFT)
        Button(top, text='Stop', command=sw.Stop).pack(side=LEFT)
        Button(top, text='Reset', command=sw.Reset).pack(side=LEFT)
        Button(top, text='Quit', command=top.quit).pack(side=LEFT)
        top.mainloop()
    main()