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
        
         # Utiliza metade da definicao de min_dist do sslenv.py para definir o raio
        radius = 0.09
        s = 0.5
        
        target_velocity = Point(0, 0)
        target_angle_velocity = 0
        
        distance = self.pos.dist_to(self.targets[0])
        theta = np.arctan2(self.targets[0].y - self.pos.y, self.targets[0].x - self.pos.x)
        for opponent in self.opponents.values():
            distance_opponent = self.pos.dist_to(Point(opponent.x, opponent.y))
            theta_opponent = np.arctan2(opponent.y - self.pos.y, opponent.x - self.pos.x)
            
            if distance_opponent < radius:
                target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(-np.sign(np.cos(theta_opponent))*2, -np.sign(np.cos(theta_opponent))*2))
            elif distance_opponent > s+radius:
                t_velocity, t_angle_velocity = Navigation.goToPoint(self.robot, Point(7*s*np.cos(theta_opponent), 7*s*np.sin(theta_opponent)))
                target_velocity += t_velocity
                target_angle_velocity += t_angle_velocity
            elif distance_opponent < s+radius:
                t_velocity, t_angle_velocity = Navigation.goToPoint(self.robot, Point(-30*(s+radius-distance_opponent)*np.cos(theta_opponent), -30*(s+radius-distance_opponent)*np.sin(theta_opponent)))
                target_velocity += t_velocity
                target_angle_velocity += t_angle_velocity
            
            if distance <= radius:
                self.targets.pop(0)
                return

            if distance > s+radius:
                if (target_angle_velocity == 0):
                    target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(7*s*np.cos(theta), 7*s*np.sin(theta)))
                else:
                    t_velocity, t_angle_velocity = Navigation.goToPoint(self.robot, Point(7*s*np.cos(theta), 7*s*np.sin(theta)))
                    target_velocity += t_velocity
                    target_angle_velocity += t_angle_velocity
            else:
                if (target_angle_velocity == 0):
                    target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(7 * (distance-radius) * np.cos(theta), 7 * (distance-radius) * np.sin(theta)))
                else:
                    t_velocity, t_angle_velocity = Navigation.goToPoint(self.robot, Point(7 * (distance-radius) * np.cos(theta), 7 * (distance-radius) * np.sin(theta)))
                    target_velocity += t_velocity
                    target_angle_velocity += t_angle_velocity
                
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass
