import random
import math
from scipy.optimize import minimize

#optinize the parameters of a dynamic hash table
class HashTableOpt:
    def __init__(self):
        self.table = {}
        self.rehashcount = 0
        self.collisioncount = 0

    def initialize(self, initialsize, a, b, loadfactorthreshold):
        self.table = {}
        self.size = initialsize
        self.a = a
        self.b = b
        self.loadfactorthreshold = loadfactorthreshold
        self.rehashcount = 0
        self.collisioncount = 0

    def insert(self, key, value):
        index = (self.a * key + self.b) % self.size
        if index in self.table:
            self.collisioncount += 1
        self.table[index] = value
        if len(self.table) / self.size > self.loadfactorthreshold:
            self.rehash()

    def rehash(self):
        self.rehashcount += 1
        oldtable = self.table
        self.size *= 2
        self.table = {}
        for key, value in oldtable.items():
            self.insert(key, value)

    def costmetrics(self):
        return {
            "rehashcount": self.rehashcount,
            "collisionrate": self.collisioncount / len(self.table) if self.table else 0
        }

    def cost(self, a, b, m, keys):
        #Initialize the hash table with given parameters
        self.initialize(initialsize=m, a=a, b=b, loadfactorthreshold=0.75)
        #Insert keys into the hash table
        for key in keys:
            self.insert(key, f"Value-{key}")
        #Get the cost metrics
        metrics = self.costmetrics()
        return metrics["rehashcount"] + metrics["collisionrate"]

#Function to adjust parameters randomly with step size
def adjustparams(params, stepsize=1):
    return {
        "a": params["a"] + random.choice([-stepsize, stepsize]),
        "b": params["b"] + random.choice([-stepsize, stepsize]),
        "m": max(params["m"] + random.choice([-stepsize, stepsize]), 2),
    }

def hillclimbing(optimizer, keys, iterations=1000, stepsize=1):

    #Initialize best parameters randomly
    bestparams = {"a": random.randint(1, 10), "b": random.randint(1, 10), "m": random.randint(8, 32)}
    #Compute the cost for the initial parameters
    bestcost = optimizer.cost(bestparams["a"], bestparams["b"], bestparams["m"], keys)

    #Iterate to find better parameters
    for _ in range(iterations):
        # Generate new parameters by adjusting the current best parameters
        newparams = adjustparams(bestparams, stepsize)
        #Compute the cost for the new parameters
        newcost = optimizer.cost(newparams["a"], newparams["b"], newparams["m"], keys)
        #If the new cost is better, update the best parameters and cost
        if newcost < bestcost:
            bestparams = newparams
            bestcost = newcost

    return bestparams, bestcost

def simulatedannealing(optimizer, keys, iterations=1000, initialtemp=100, coolingrate=0.95):

    #Initialize current parameters randomly
    currentparams = {"a": random.randint(1, 10), "b": random.randint(1, 10), "m": random.randint(8, 32)}
    #Compute the cost for the current parameters
    currentcost = optimizer.cost(currentparams["a"], currentparams["b"], currentparams["m"], keys)
    #Initialize best parameters and cost
    bestparams, bestcost = currentparams.copy(), currentcost
    #Set the initial temperature
    temperature = initialtemp

    #Iterate to find better parameters
    for _ in range(iterations):
        #Generate new parameters by adjusting the current parameters
        newparams = adjustparams(currentparams, 1)
        #Compute the cost for the new parameters
        newcost = optimizer.cost(newparams["a"], newparams["b"], newparams["m"], keys)
        #Calculate the change in cost
        delta = newcost - currentcost

        #Accept the new parameters if they are better or with a certain probability
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            currentparams, currentcost = newparams, newcost

        #Update the best parameters and cost if the current cost is better
        if currentcost < bestcost:
            bestparams, bestcost = currentparams.copy(), currentcost

        #Reduce the temperature
        temperature *= coolingrate

    return bestparams, bestcost

def neldermead(optimizer, keys):
    #Define the objective function to minimize
    def objective(params):
        a, b, m = params
        #Ensure m is at least 2
        m = max(int(m), 2)
        return optimizer.cost(a, b, m, keys)

    #Initialize the initial guess
    initialguess = [random.randint(1, 10), random.randint(1, 10), random.randint(8, 32)]
    #mininize function with the Nelder-Mead method
    result = minimize(objective, initialguess, method="Nelder-Mead", options={"disp": True})
    #Extract the best parameters from the result
    bestparams = {"a": int(result.x[0]), "b": int(result.x[1]), "m": int(result.x[2])}
    return bestparams, result.fun

def main():
    keys = [random.randint(1, 1000) for _ in range(100)]
    optimizer = HashTableOpt()

    print("Hill Climbing:")
    hcparams, hccost = hillclimbing(optimizer, keys)
    print(f"Parameters: {hcparams}, Cost: {hccost}")

    print("Simulated Annealing:")
    saparams, sacost = simulatedannealing(optimizer, keys)
    print(f"Parameters: {saparams}, Cost: {sacost}")

    print("Nelder-Mead:")
    nmparams, nmcost = neldermead(optimizer, keys)
    print(f"Parameters: {nmparams}, Cost: {nmcost}")

if __name__ == "__main__":
    main()


