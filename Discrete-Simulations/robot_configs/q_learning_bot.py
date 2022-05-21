import copy 
import numpy as np

wind_directions = ['n', 'e', 's', 'w']
alpha = 0.15
my_gamma = 0.85
epsilon = 0.15
my_num_episodes = 450 # 1000
max_num_steps = 30

def get_name():
  return 'q_loc'

def get_epsilon_q_choice(q_table, pos, epsilon):
  directions = q_table[pos[0], pos[1]]
  direction = int(np.argmax(directions))
  random = np.random.binomial(1, epsilon)
  if random == 1 or np.all((directions == 0)):
    direction = int(np.random.choice([0,1,2,3]))
  return direction

def update_q_table(q_table, old_pos, choice, new_pos, reward, alpha, gamma):
  q_table[old_pos[0], old_pos[1], choice] = q_table[old_pos[0], old_pos[1], choice] * (1 - alpha) + \
    alpha * (reward + gamma * np.max(q_table[new_pos[0], new_pos[1], :]))
  return q_table 

def robot_epoch(actual_robot, gamma = my_gamma, num_episodes = my_num_episodes):
  # Initialize Q table
  q_table =  np.zeros((actual_robot.grid.n_cols, actual_robot.grid.n_rows, 4))

  # Run episodes
  #! On actual board implementation
  for episode in range(num_episodes):
    # Initialize robot at current (real location)
    robot = copy.deepcopy(actual_robot)
    old_dirty_count = np.count_nonzero(robot.grid.cells==1)

    for step in range(max_num_steps):
      #?::::Take action given the epsilon-greedy policy::::
      # Get best choice given agents' current location, epsilon greedy
      # add a decay rate which goes to 0 as the number of steps increases
      decayrate = 1 - step/max_num_steps
      decayed_epsilon = epsilon * decayrate

      choice = get_epsilon_q_choice(q_table, robot.pos, decayed_epsilon)

      old_location = copy.copy(robot.pos)

      # Move agent
      if actual_robot.alive == False:
        break

      while wind_directions[choice] != robot.orientation:
        robot.rotate('r')
      robot.move()
      
      # Calculate the reward for the previous action
      new_goal_count = np.count_nonzero(robot.grid.cells==2)
      new_dirty_count = np.count_nonzero(robot.grid.cells==1)
      reward = float(new_goal_count + old_dirty_count - new_dirty_count - 0.2)
      old_dirty_count = new_dirty_count

      # Update Q-table 
      q_table = update_q_table(q_table, old_location, choice, robot.pos, reward, alpha, gamma)

  choice = get_epsilon_q_choice(q_table, actual_robot.pos, 0.0)
  while wind_directions[choice] != actual_robot.orientation:
    actual_robot.rotate('r')
  actual_robot.move()
  # print(actual_robot.orientation)