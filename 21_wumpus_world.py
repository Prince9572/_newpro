# Experiment: Wumpus World
# Question: Simulate a logic-based agent for the Wumpus World.
# Preferably in Python.

world = [
    ['S', '', 'P'],
    ['', 'W', ''],
    ['', '', 'G']
]

r, c = 0, 0

while True:
    print("Agent at:", (r, c))

    if world[r][c] == 'G':
        print("Gold Found!")
        break
    elif world[r][c] == 'W':
        print("Wumpus! Game Over")
        break
    elif world[r][c] == 'P':
        print("Pit! Game Over")
        break

    if c < 2:
        c += 1
    elif r < 2:
        r += 1
        c = 0
    else:
        print("Goal Not Found")
        break