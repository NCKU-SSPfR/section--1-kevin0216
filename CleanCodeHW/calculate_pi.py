import random

# Constant settings
RADIUS = 1
NUM_POINTS = 1000000
AREA_FACTOR = 4
SQUARE_EXPONENT = 2
POINT_COUNT_INCREMENT = 1

centre_point = 0

# Randomly generate points and count those inside the circle
for _ in range(NUM_POINTS):
    x = random.uniform(-RADIUS, RADIUS)
    y = random.uniform(-RADIUS, RADIUS)
    if x**SQUARE_EXPONENT + y**SQUARE_EXPONENT <= RADIUS**SQUARE_EXPONENT:
        centre_point += POINT_COUNT_INCREMENT

# Estimate pi based on the number of points inside the circle
estimated_pi = (centre_point / NUM_POINTS) * AREA_FACTOR

print(f"Estimated value of pi is: {estimated_pi}")
