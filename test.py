import json

class testNot:
    
    def __init__(self):
        self.a = 5
        self.b = "hello"
    
    stv = ["a",
           "b"]

    def writeState(self):
        state = {}
        for v in self.stv:
            c = f"self.{v}"
            print(eval(f"self.{v}"))
            print(c)
            state[v] = eval(c)
        print("State:", state)
        with open("test.json", "w") as f:
            f.write(json.dumps(state))

    def loadState(self):
        with open("test.json", "r") as f:
            vin = json.loads(f.read())
        print("vin:", vin)
        for k,v in vin.items():
            print(k, v)
            eval(f'self.{k}') = v
            
            

x = testNot()
v = "a"
print(eval(f'x.{v}'))
# x.writeState()
x.loadState()