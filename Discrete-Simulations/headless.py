# Import our robot algorithm to use in this simulation:
# from robot_configs.q_o_learning_bot import robot_epoch
from operator import index
import pickle
from environment import Robot
import matplotlib.pyplot as plt
import time

import robot_configs.q_o_learning_bot as q_o
import robot_configs.q_learning_bot as q

# q_o.robot_epoch

agents = [q_o, q]
t0 = time.time()


# grid_file = 'example-random-level.grid'
# grid_file = 'example-random-house-0.grid'
# grid_file = 'death.grid'
grid_files = ['example-random-house-0.grid', 'example-random-level.grid']
gammas = [0.3, 0.5, 0.7, 0.9]
episodes_list = [250,500,750,1000,1500]
# Cleaned tile percentage at which the room is considered 'clean':
stopping_criteria = 100 # 100
index_i = 0
while True:
    index_i = index_i + 1
    print(f'full run {index_i}')
    for agent in agents:
        for grid_file in grid_files:
            for gamma in gammas:
                for num_episodes in episodes_list:
                    # Keep track of some statistics:
                    robot_epoch = agent.robot_epoch
                    efficiencies = []
                    n_moves = []
                    deaths = 0
                    cleaned = []

                    # Run 5 times:
                    for i in range(1):
                        # Open the grid file.
                        # (You can create one yourself using the provided editor).
                        with open(f'grid_configs/{grid_file}', 'rb') as f:
                            grid = pickle.load(f)
                        # Calculate the total visitable tiles:
                        n_total_tiles = (grid.cells >= 0).sum()
                        # Spawn the robot at (1,1) facing north with battery drainage enabled:
                        # robot = Robot(grid, (1, 1), orientation='n', battery_drain_p=1, battery_drain_lam=0)
                        robot = Robot(grid, (1, 1), orientation='n', battery_drain_p=0.5, battery_drain_lam=2)
                        # efficiency = None 

                        # Keep track of the number of robot decision epochs:
                        n_epochs = 0
                        while True:
                            n_epochs += 1
                            # Do a robot epoch (basically call the robot algorithm once):
                            robot_epoch(robot, gamma = gamma, num_episodes = num_episodes)
                            # Stop this simulation instance if robot died :( :
                            if not robot.alive:
                                deaths += 1
                                break
                            # Calculate some statistics:
                            clean = (grid.cells == 0).sum()
                            dirty = (grid.cells >= 1).sum()
                            goal = (grid.cells == 2).sum()
                            # Calculate the cleaned percentage:
                            clean_percent = (clean / (dirty + clean)) * 100
                            # See if the room can be considered clean, if so, stop the simulaiton instance:
                            if clean_percent >= stopping_criteria and goal == 0:
                                break
                            # Calculate the effiency score:
                            moves = [(x, y) for (x, y) in zip(robot.history[0], robot.history[1])]
                            u_moves = set(moves)
                            n_revisted_tiles = len(moves) - len(u_moves)
                            efficiency = (100 * n_total_tiles) / (n_total_tiles + n_revisted_tiles)
                            # Keep track of the last statistics for each simulation instance:
                        efficiencies.append(float(efficiency))
                        n_moves.append(len(robot.history[0]))
                        cleaned.append(clean_percent)
                        # print("done")
                    
                    for (eff, cle) in zip(efficiencies, cleaned):
                        lines = [agent.get_name(), grid_file, str(gamma),str(num_episodes),str(eff), str(cle), '\n']
                        with open('results.txt', 'a') as f:
                            # f.writelines('\n'.join(['']))
                            # f.writelines(' '.join(lines))
                            f.write(' '.join(lines), )

# Make some plots:
# plt.hist(cleaned)
# plt.title('Percentage of tiles cleaned.')
# plt.xlabel('% cleaned')
# plt.ylabel('count')
# plt.show()

# plt.hist(efficiencies)
# print(efficiencies)
# plt.title('Efficiency of robot.')
# plt.xlabel('Efficiency %')
# plt.ylabel('count')
# plt.show()

# lines = ['Readmenew', ,'How to write text files in Python']
# with open('readme.txt', 'a') as f:
#     f.writelines('\n'.join(lines))

# t1 = time.time()
# total = t1-t0
# print(total)