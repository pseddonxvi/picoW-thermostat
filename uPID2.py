import time
import json

class uPID:
    def __init__(self, setT, dt=1.0, Kp=1.0, Ki=0, Kd=100):
        self.state = {}
        self.state["setT"] = setT
        self.state["Kp"] = Kp
        self.state["Ki"] = Ki
        self.state["Kd"] = Kd 

        self.state["dt"] = dt
        self.state["startTime"] = -1
        self.state["T_data"] = []
        # number of current data points to keep
        self.state["nCurrent"] = 300 
        self.state["T_long"] = []
        # timestep for long term records (continue recording indefinitely)
        self.state["longDt"] = self.nCurrent * self.dt 
        self.state["status"] = "None"

        self.clock = 0
        self.longClock = 0
        
        self.err = 0
        self.prp = 0
        self.int = 0
        self.dif = 0
        self.ctrl = 0
        
        self.initialized = False

        self.stateFileName = "state.json"


    def getError(self,T):
        return self.state["setT"] - T

    def check(self, T):
        if (not self.initialized): # initialize 
            self.state["T_data"].append([0,T])
            self.state["T_long"].append([0,T])
            self.state["startTime"] = time.monotonic()
            self.err = self.getError(T)
            self.clock = time.monotonic()
            self.longClock = time.monotonic()
            self.initialized = True
            self.state["status"] = "Initialized"

        else: 
            runtime = round(time.monotonic() - self.state["startTime"], 1)
            self.state["T_data"].append((runtime, T))
            if len(self.state["T_data"]) > self.state["nCurrent"]:
                oldT = self.state["T_data"].pop(0)
                if (self.longClock + self.state["longDt"]) < time.monotonic():
                    self.state['T_long'].append(oldT)
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
        with open(self.stateFileName, "w") as f:
            f.write(json.dumps(self.state))

    def loadState(self):
        try:
            with open(self.stateFileName, "r") as f:
                self.state = json.loads(f.read())
        except Exception as e:
            print(f'Error loading state file ({self.stateFileName}): {e}')



