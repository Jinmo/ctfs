import random

def rand():
    return random.randint(0, 9)

memory = [0] * 100
memory[:] = list(range(100))

memory = [
#2-  4-  3   2-  2   4   1   3-  2   2-
 1 , 2 , 3 , 4 , 5 , 6 , 10, 8 , 9 , 7 , # 2-
 10, 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , # 2-
 10, 9 , 8 , 7 , 6 , 5 , 4 , 3 , 2 , 1 , # 2
 10, 9 , 8 , 7 , 6 , 5 , 4 , 3 , 2 , 1 , # 2
 10, 9 , 8 , 7 , 6 , 5 , 4 , 3 , 2 , 1 , # 2
 10, 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , # 2-
 10, 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , # 3-
 10, 9 , 8 , 7 , 6 , 5 , 4 , 3 , 2 , 1 , # 3
 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10, # 1-
 10, 9 , 8 , 7 , 6 , 5 , 4 , 3 , 2 , 1 , # 3
]

_memory = [
#2-  4-  3   2-  2   4   1   3-  2   2-
 4 , 3 , 8 , 2 , 6 , 1 , 10, 5 , 7 , 9 , # 2-
 6 , 7 , 9 , 5 , 1 , 4 , 2 , 3 , 10, 8 , # 2-
 5 , 2 , 10, 8 , 9 , 6 , 7 , 4 , 3 , 1 , # 2
 10, 4 , 5 , 1 , 2 , 3 , 9 , 7 , 8 , 6 , # 2
 8 , 10, 1 , 4 , 3 , 2 , 5 , 6 , 9 , 7 , # 2
 3 , 6 , 4 , 9 , 7 , 5 , 8 , 10, 1 , 2 , # 2-
 1 , 9 , 7 , 6 , 8 , 10, 3 , 2 , 5 , 4 , # 3-
 2 , 8 , 3 , 7 , 10, 9 , 4 , 1 , 6 , 5 , # 3
 7 , 1 , 2 , 3 , 5 , 8 , 6 , 9 , 4 , 10, # 1-
 9 , 5 , 6 , 10, 4 , 7 , 1 , 8 , 2 , 3 , # 3
]

ops = [20, 0, 8, 2, 0, 2, 3, 0, 5, 4, 0, 4, 2, 0, 6, 1, 1, 0, 2, 1, 3, 2, 1, 1, 4, 1, 7, 3, 1, 9, 2, 2, 3, 2, 2, 4, 2, 2, 9, 3, 2, 7, 3, 2, 2, 2, 3, 1, 2, 3, 6, 3, 3, 5, 2, 3, 0, 2, 3, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 147, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def validate(memory):
    pc = 1
    count = ops[0]
    score = 0
    for i in range(count):
        op0, op1, op2 = ops[pc:pc + 3]
        pc += 3
        vm = [
            (10, op1),
            (-10, 90 + op1),
            (1, 10 * op1),
            (-1, 10 * (op1 + 1) - 1),
        ]
        delta, offset = vm[op0]
        l = [memory[offset + delta * j] for j in range(10)]
        max = -1
        count = 0
        for x in l:
            if x > max:
                count += 1
                max = x
        score += abs(count - op2)
    return score

table = memory[:]

def flip(memory):
    row = rand()
    while True:
        a, b = rand(), rand()
        if a == b:
            continue
        break

    memory[row * 10 + a], memory[row * 10 + b] = memory[row * 10 + b], memory[row * 10 + a]

def uniqueness(memory):
    return sum(len(set(memory[i * 10 + j] for i in range(10))) for j in range(10))

def fitness(memory):
    # reward: uniqueness of row-wise numbers; sum(len(set(row)) for row in rows)
    u = uniqueness(memory)
    v = -validate(memory)
    penalty = 0
    if memory[89] != 10:
        penalty -= 100000
    if memory[6] != 10:
        penalty -= 100000
    return penalty + v + u * 8


def print_rows(memory):
    print('[')
    print('#2-  4-  3   2-  2   4   1   3-  2   2-')
    for i in range(10):
        print(' ', end='')
        for j in range(10):
            print('%-2d' % memory[i * 10 + j], end=', ')
        print('# %s%s' % ([2, 2, 2, 2, 2, 2, 3, 3, 1, 3][i], '--   -- - '[i].strip()))
    print(']')

def print_score(memory):
    print(fitness(memory), uniqueness(memory), validate(memory))

generation = [table[:] for i in range(8)]
score = [0] * 100 # saturation checker

for i in range(8000000):
    original = [table[:] for table in generation]
    initial_fitness = fitness(generation[0])
    # mutation
    for cur in generation:
        r = random.randint(0, 2)
        if r == 0:
            for _ in range(rand()):
                flip(cur)
        else:
            continue

    new_generation = sorted(generation, key=lambda memory: -fitness(memory))
    if fitness(new_generation[0]) < initial_fitness:
        generation = original
        continue

    # print scores
    if i % 20000 == 1999:
        print_score(new_generation[0])
        print_rows(new_generation[0])

    # terminated?
    if validate(generation[0]) == 0 and uniqueness(generation[0]) == 100:
        print('Solved!')
        break

    # stuck in local minima; TODO: check if it's really stuck for N times
    # index = (i // 1000) % 100
    # score[index] = fitness(new_generation[0])
    # if score[index] == score[(index + 1) % 100] and uniqueness(new_generation[0]) >= 90:
    #     break

    # prepare the next generation
    generation = new_generation[:4] * 2
    generation = [table[:] for table in generation]

print_rows(generation[0])
