from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point
import numpy as np
import matplotlib.pyplot as plt

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)

    def decision(self):
        if len(self.targets) == 0:
            return
        
        num_targets = len(self.targets)
                
        goals = [[0 for i in range(num_targets)] for j in range(len(self.teammates))]
        bids = [[-np.inf for i in range(num_targets)] for j in range(len(self.teammates))]
        costs = [[-Point(j.x, j.y).dist_to(self.targets[i]) for i in range(num_targets)] for j in self.teammates.values()]
        
        agent_index = 0
        
        for (i, agent) in enumerate(self.teammates.values()):        
            if (agent.id == self.id):
                agent_index = i
                
            agent_goals = goals[i]
            agent_bids = bids[i]
            agent_costs = costs[i]

            for j in range(num_targets):
                if (agent_costs[j] > agent_bids[j]):
                    agent_goals[j] = 1
                    agent_bids[j] = agent_costs[j]

            bids[i] = agent_bids
            goals[i] = agent_goals
            costs[i] = agent_costs

        target_index = 0
        final_bids = [0 for i in range(num_targets)]
        for i in range(len(bids)):
            for j in range(num_targets):
                if (bids[agent_index][j] > bids[i][j] and goals[i][j] == 1):
                    final_bids[j] = bids[agent_index][j]
                    
        target_index = final_bids.index(max(final_bids))
                
         # Utiliza metade da definicao de min_dist do sslenv.py para definir o raio
        radius = 0.18
        s = 1.2
                
        target_velocity = Point(0, 0)
        target_angle_velocity = 0
        
        distance = self.pos.dist_to(self.targets[target_index])
        theta = np.arctan2(self.targets[target_index].y - self.pos.y, self.targets[target_index].x - self.pos.x)
        for opponent in self.opponents.values():
            distance_opponent = self.pos.dist_to(Point(opponent.x, opponent.y))
            theta_opponent = np.arctan2(opponent.y - self.pos.y, opponent.x - self.pos.x)
            
            if distance_opponent < radius:
                target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(-np.sign(np.cos(theta_opponent))*1.5, -np.sign(np.cos(theta_opponent))*1.5))
            elif distance_opponent > s+radius:
                t_velocity, t_angle_velocity = Navigation.goToPoint(self.robot, Point(80*s*np.cos(theta_opponent), 80*s*np.sin(theta_opponent)))
                target_velocity += t_velocity
                target_angle_velocity += t_angle_velocity
            elif distance_opponent < s+radius:
                t_velocity, t_angle_velocity = Navigation.goToPoint(self.robot, Point(-50*(s+radius-distance_opponent)*np.cos(theta_opponent), -50*(s+radius-distance_opponent)*np.sin(theta_opponent)))
                target_velocity += t_velocity
                target_angle_velocity += t_angle_velocity

            if distance > s+radius:
                if (target_angle_velocity == 0):
                    target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(100*s*np.cos(theta), 100*s*np.sin(theta)))
                else:
                    t_velocity, t_angle_velocity = Navigation.goToPoint(self.robot, Point(100*s*np.cos(theta), 100*s*np.sin(theta)))
                    target_velocity += t_velocity
                    target_angle_velocity += t_angle_velocity
            else:
                if (target_angle_velocity == 0):
                    target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(150 * (distance-radius) * np.cos(theta), 150 * (distance-radius) * np.sin(theta)))
                else:
                    t_velocity, t_angle_velocity = Navigation.goToPoint(self.robot, Point(150 * (distance-radius) * np.cos(theta), 150 * (distance-radius) * np.sin(theta)))
                    target_velocity += t_velocity
                    target_angle_velocity += t_angle_velocity
                
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass
