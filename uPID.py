import time

class uPID:
    def __init__(self, setT, dt=1.0, Kp=1.0, Ki=0, Kd=100):
        self.setT = setT
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd 
        self.dt = dt

        self.err = 0
        self.prp = 0
        self.int = 0
        self.dif = 0
        self.ctrl = 0
        
        self.T_data = [] #temperature
        self.clock = 0
        self.T_long = []
        self.longClock = 0
        # number of current data points to keep
        self.nCurrent = 300 
        # timestep for long term records (continue recording indefinitely)
        self.longDt = self.nCurrent * self.dt 
        # # medium term timekeeping 
        # self.nMid = 100
        # self.midDt = self.longDt / self.nMid 
        
        self.initialized = False


    def getError(self,T):
        return self.setT - T

    def check(self, T):
        if (not self.initialized): # initialize 
            self.T_data.append([0,T])
            self.err = self.getError(T)
            self.startTime = time.monotonic()
            self.clock = time.monotonic()
            self.longClock = time.monotonic()
            self.T_long.append((0,T))
            self.initialized = True

        else: 
            runtime = round(time.monotonic() - self.startTime, 1)
            self.T_data.append((runtime, T))
            if len(self.T_data) > self.nCurrent:
                oldT = self.T_data.pop(0)
                if (self.longClock + self.longDt) < time.monotonic():
                    self.T_long.append(oldT)
                    print("record long:")
                    self.longClock = time.monotonic()

            print("calculating pid")
            #error
            self.err = self.getError(T) 
            #proportional
            self.prp = self.Kp * self.err
            #integral
            self.int += self.Ki * self.err
            #differential
            self.dTdt = (self.T_data[-1][1] - self.T_data[-2][1])/self.dt
            self.dif = self.Kd * self.dTdt 

            self.ctrl = self.prp + self.int + self.dif

            print(f'T={T} | e={self.err} | P={self.prp} | I={self.int} | dT/dt={self.dTdt} | D={self.dif} | C={self.ctrl}')
            


        return self.ctrl

    def saveState(self):
        with open("state.json", "w") as f:
            state = {}
            state["startTime"] = self.startTime 
            state["T_data"] = self.T_data 
            state["T_long"] = self.T_long
            state["setT"] = self.setT 
            self.Kp = Kp
            self.Ki = Ki
            self.Kd = Kd 
            self.dt = dt




