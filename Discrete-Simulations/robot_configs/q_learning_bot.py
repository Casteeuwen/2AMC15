import copy 
import numpy as np

simple_reward_map = {-6:-2,-5:-2,-4:-2 ,-3:-2,-2: -9, -1: -9, 0: -2 , 1: 2, 2: 4, 3: -1}
materials = {0: 'cell_clean', -1: 'cell_wall', -2: 'cell_obstacle', -3: 'cell_robot_n', -4: 'cell_robot_e',
              -5: 'cell_robot_s', -6: 'cell_robot_w', 1: 'cell_dirty', 2: 'cell_goal', 3: 'cell_death'}
wind_directions = ['n', 'e', 's', 'w']
alpha = 0.1
gamma = 0.85
epsilon = 0.15
num_episodes = 3000
max_num_steps = 30

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

def robot_epoch(actual_robot):
  # Initialize Q table
  q_table =  np.zeros((actual_robot.grid.n_cols, actual_robot.grid.n_rows, 4))

  # Run episodes
  #! On actual board implementation
  for episode in range(num_episodes):
    # Initialize robot at current (real location)
    robot = copy.deepcopy(actual_robot)
    # old_empty_count = 0
    old_dirty_count = np.count_nonzero(robot.grid.cells==1)
    for step in range(max_num_steps):
      #?::::Take action given the epsilon-greedy policy::::
      # Get best choice given agents' current location, epsilon greedy
      choice = get_epsilon_q_choice(q_table, robot.pos, epsilon)

      old_location = copy.copy(robot.pos)
      # old_vibe = robot.grid.cells[old_location]
      # print(f'old: {old_location} vibe: {materials[old_vibe]}')

      # Move agent
      # TODO build check to see if it has died, exit this episode in that case
      while wind_directions[choice] != robot.orientation:
        robot.rotate('r')
      robot.move()
      
      
      # Calculate the reward for the previous action
      # TODO expand this past simply counting clean cells
      # new_empty_count =  np.count_nonzero(robot.grid.cells==0)
      # reward = float(new_empty_count - old_empty_count) - 2.0
      # old_empty_count = new_empty_count
      new_dirty_count = np.count_nonzero(robot.grid.cells==1)
      reward = float(old_dirty_count - new_dirty_count - 0.3)
      old_dirty_count = new_dirty_count

      # print(f'new: {robot.pos} vibe {materials[robot.grid.cells[robot.pos]]}')
      # Update Q-table 
      q_table = update_q_table(q_table, old_location, choice, robot.pos, reward, alpha, gamma)
      # print(robot.grid.cells)
      # print(reward)
    # print("_______________________________________________________")
    # print(q_table) 
  
  directions = q_table[actual_robot.pos[0], actual_robot.pos[1]]
  print(directions)
  choice = int(np.argmax(directions))
  print(wind_directions[choice])
  while wind_directions[choice] != actual_robot.orientation:
    actual_robot.rotate('r')
  # while 's' != actual_robot.orientation:
  #   actual_robot.rotate('r')
  actual_robot.move()
    
      
    















  # # Run episodes 
  # #! Custom implementation (not used)
  # for episode in range(num_episodes):
  #   # Initialize robot at current (real location)
  #   location = robot.pos
  #   for step in range(max_num_steps):
  #     #?::::Take action given the epsilon-greedy policy::::
  #     # Get best choice given agents' current location, epsilon greedy
  #     choice = get_epsilon_q_choice(q_table, location, epsilon)

  #     # Compute actual movement based on randomness parameter of the model
  #     if np.random.binomial(1, robot.p_move) == 1:
  #       choice = int(np.random.choice([0,1,2,3]))

  #     # Move agent
      

  #     # Update Q-table 

  #     # 
  #     pass

