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

        self.clock = 0
        self.T = []
        self.longT = []
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
        if self.initialized:
            self.T.append(T)
            if len(self.T) > self.nCurrent:
                self.T.pop(0)
            if (self.longClock + self.longDt) < time.monotonic():
                self.longT.append(self.T[0])
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
            self.dTdt = (self.T[-1] - self.T[-2])/self.dt
            self.dif = self.Kd * self.dTdt 

            self.ctrl = self.prp + self.int + self.dif

            print(f'T={T} | e={self.err} | P={self.prp} | I={self.int} | dT/dt={self.dTdt} | D={self.dif} | C={self.ctrl}')
            
        else: # initialize 
            self.T.append(T)
            self.err = self.getError(T)
            self.startTime = time.monotonic()
            self.clock = time.monotonic()
            self.longClock = time.monotonic()
            self.initialized = True

        return self.ctrl




