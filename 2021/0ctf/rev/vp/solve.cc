#include <algorithm> // std::shuffle
#include <random>
#include <cstdlib>
#include <cstdio>
#include <chrono> // std::chrono::system_clock
#include <cstring>

char memory[100];

int _rand()
{
  return rand() % 10;
}

int get_index(char memory[], int start)
{
  for (int i = 0; i < 10; i++)
  {
    int index = start + i;
    if (memory[index] == 10)
      return i;
  }
  exit(0);
}

void print_rows(char memory[])
{
  static int indexes[] = {2, 2, 2, 2, 2, 2, 3, 3, 1, 3};
  puts("{");
  puts("//2-  4-  3   2-  2   4   1   3-  2   2-");
  for (int i = 0; i < 10; i++)
  {
    fputc(' ', stdout);
    for (int j = 0; j < 10; j++)
      printf("%-2d,", memory[i * 10 + j]);
    printf("// %d%c\n", indexes[i], "--   -- - "[i]);
  }
  puts("}");
}

void init_memory()
{
  for (int i = 0; i < 10; i++)
    for (int j = 0; j < 10; j++)
      memory[i * 10 + j] = j + 1;

  int a = 0, b = 0;
  for (int i = 0; i < 10; i++)
  {
    bool change = false;
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::shuffle(&memory[i * 10], &memory[i * 10 + 10], std::default_random_engine(seed));
    if (i == 0)
    {
      a = get_index(memory, i * 10);
      b = 6;
      change = true;
    }
    if (i == 8)
    {
      a = get_index(memory, i * 10);
      b = 9;
      change = true;
    }
    if (change && (a != b))
    {
      std::swap(memory[i * 10 + a], memory[i * 10 + b]);
    };
  }
}

int ops[] = {20, 0, 8, 2, 0, 2, 3, 0, 5, 4, 0, 4, 2, 0, 6, 1, 1, 0, 2, 1, 3, 2, 1, 1, 4, 1, 7, 3, 1, 9, 2, 2, 3, 2, 2, 4, 2, 2, 9, 3, 2, 7, 3, 2, 2, 2, 3, 1, 2, 3, 6, 3, 3, 5, 2, 3, 0, 2, 3, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 147, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

int validate(char memory[])
{
  int pc = 1,
      count = ops[0],
      score = 0;
  for (int i = 0; i < count; i++)
  {
    char op0 = ops[pc], op1 = ops[pc + 1], op2 = ops[pc + 2];
    pc += 3;
    int vm[][2] = {
        {10, op1},
        {-10, 90 + op1},
        {1, 10 * op1},
        {-1, 10 * (op1 + 1) - 1},
    };
    int delta = vm[op0][0], offset = vm[op0][1], max = -1, count = 0;
    for (auto j = 0; j < 10; j++)
    {
      int x = memory[offset + delta * j];
      if (x > max)
      {
        count += 1;
        max = x;
      }
    }
    score += (count - op2) * (count - op2);
  }
  return score;
}

void flip(char memory[])
{
  int row = _rand();
  int a = _rand();
  int b = _rand();

  if (row == 0 && (a == 6 || b == 6))
    return;
  if (row == 8 && (a == 9 || b == 9))
    return;

  std::swap(memory[row * 10 + a], memory[row * 10 + b]);
};

int uniqueness(char memory[])
{
  int score = 0;
  for (int i = 0; i < 10; i++)
  {
    int visited[10] = {0};
    for (int j = 0; j < 10; j++)
    {
      auto c = memory[j * 10 + i] - 1;
      if (!visited[c])
      {
        visited[c] = 1;
        score++;
      }
    }
  }
  return score;
}

int fitness(char memory[])
{
  //reward : uniqueness of row - wise numbers; sum(len(set(row)) for row in rows)
  auto u = uniqueness(memory);
  auto v = -validate(memory);
  int penalty = 0;
  if (memory[89] != 10)
    penalty -= 100000;
  if (memory[6] != 10)
    penalty -= 100000;
  return penalty + v + u * 8;
}

void print_score(char memory[])
{
  printf("%d %d %d\n", fitness(memory), uniqueness(memory), validate(memory));
}

int main()
{
  char table[100];
  init_memory();
  memcpy(table, memory, 100);
#define NUM_GENERATIONS 4
  char generation[NUM_GENERATIONS][100];
  for (int i = 0; i < NUM_GENERATIONS; i++)
  {
    memcpy(generation[i], table, 100);
  }
  int score[100] = {}; // saturation checker

  int i = -1;
  while (i < 10000000)
  {
    char original[NUM_GENERATIONS][100];

    i += 1;
    memcpy(original, generation, sizeof(generation));
    int initial_fitness = fitness(generation[0]);
    //mutation
    for (int j = 0; j < NUM_GENERATIONS; j++)
    {
      char *cur = generation[j];
      int r = rand() % 2;
      if (r == 0)
        for (int _ = 0; _ < rand() % 16; _++)
          flip(cur);
      else
        continue;
    }

    int indexes[NUM_GENERATIONS] = {};
    for (int j = 0; j < NUM_GENERATIONS; j++)
    {
      indexes[j] = j;
    }
    char new_generation[NUM_GENERATIONS][100];
    std::sort(indexes, indexes + NUM_GENERATIONS, [&](int a, int b)
              { return fitness(generation[a]) > fitness(generation[b]); });
    for (int j = 0; j < NUM_GENERATIONS; j++)
    {
      memcpy(new_generation[j], generation[indexes[j]], 100);
    }
    memcpy(generation, new_generation, sizeof(generation));
    if (fitness(generation[0]) < initial_fitness)
    {
      memcpy(generation, original, sizeof(generation));
      continue;
    }

    //print scores
    if (i % 200000 == 199999)
    {
      print_score(generation[0]);
      print_rows(generation[0]);
    }

    //terminated ?
    if (validate(generation[0]) == 0 and uniqueness(generation[0]) == 100)
    {
      puts("Solved!");
      freopen("/tmp/payload", "w", stdout);
      print_rows(generation[0]);
      return 0;
    }

    //stuck in local minima; TODO : check if it's really stuck for N times
    // int index = (i / 1000) % 100;
    // score[index] = fitness(generation[0]);
    // if (score[index] == score[(index + 1) % 100] && uniqueness(generation[0]) >= 90)
    //   break;

    //prepare the next generation
    for (int i = 0; i < 2; i++)
      memcpy(generation[i + 2], generation[i], sizeof(generation[0]));
  }

  print_rows(generation[0]);
}