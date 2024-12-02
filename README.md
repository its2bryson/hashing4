# Optimization Techniques Comparison Report

This report compares the results of three optimization techniques used to optimize the parameters of a dynamic hash table. The techniques compared are:

1. Hill Climbing
2. Simulated Annealing
3. Nelder-Mead

## Hash Table Optimization

We want to find the best values for the parameters a, b, and m in the hash table so that we get the lowest "cost." The cost is calculated based on two factors: the number of times the table needs to be resized (rehashes) and how often keys collide.

## Techniques

### Hill Climbing

Hill Climbing is a simple method where we start with random values for a, b, and m and make small changes to try and improve them. It keeps going until no better solution can be found.

### Simulated Annealing

Simulated Annealing is a more flexible method. It sometimes accepts worse solutions to escape from local minima. Over time, it gets more precise about accepted solutions.

### Nelder-Mead

Nelder-Mead is a technique that doesn't need gradients. It tries different values for a, b, and m and keeps improving them until it finds the best solution.

## Results

The results of the optimization techniques are as follows:

### Hill Climbing

- **Parameters:** `a = 9`, `b = 2`, `m = 28`
- **Cost:** `2.381`

### Simulated Annealing

- **Parameters:** `a = 3`, `b = 19`, `m = 25`
- **Cost:** `2.887`

### Nelder-Mead

- **Parameters:** `a = 3`, `b = 8`, `m = 17`
- **Cost:** `3.0`

## Conclusion

From the results, we can see that each method has its strengths. Hill Climbing is quick but might get stuck in a bad spot. Simulated Annealing does a good job of exploring different possibilities. Nelder-Mead works well for problems where we don’t have gradients.

The best technique for optimizing the hash table in this case is Hill Climbing because it gave the lowest cost.
