from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point
import numpy as np

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)

    def decision(self):
        if len(self.targets) == 0:
            return
        
        radius = 0.1
        s = 10
        
        target_velocity = Point(0, 0)
        target_angle_velocity = 0
        
        distance = self.pos.dist_to(self.targets[0])
        distance_opponent = 1000
        closest_oponent = None
        for opponent in self.opponents.values():
            if (min(distance_opponent, self.pos.dist_to(Point(opponent.x, opponent.y))) == self.pos.dist_to(Point(opponent.x, opponent.y))):
                closest_oponent = opponent
    
            distance_opponent = min(distance_opponent, self.pos.dist_to(Point(opponent.x, opponent.y)))
            
        theta = np.arctan2(self.targets[0].y - self.pos.y, self.targets[0].x - self.pos.x)
        theta_opponent = np.arctan2(closest_oponent.y - self.pos.y, closest_oponent.x - self.pos.x)
        
        print(self.targets[0], self.pos, distance)
        
        if distance_opponent < radius:
            target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(np.sign(np.cos(theta_opponent)), np.sign(np.cos(theta_opponent))))
        elif distance_opponent > s+radius:
            target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(50*s*np.cos(theta_opponent), 50*s*np.sin(theta_opponent)))
        elif distance_opponent < s+radius:
            target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(-70*(s+radius-distance_opponent)*np.cos(theta_opponent), -70*(s+radius-distance_opponent)*np.sin(theta_opponent)))
        
        if distance < radius:
            self.targets.pop(0)
            return

        if distance > s+radius:
            if (target_angle_velocity == 0):
                target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(50*s*np.cos(theta)+distance, 50*s*np.sin(theta)+distance))
            else:
                t_velocity, t_angle_velocity = Navigation.goToPoint(self.robot, Point(50*s*np.cos(theta)+distance, 50*s*np.sin(theta)+distance))
                target_velocity += t_velocity
                target_angle_velocity += t_angle_velocity
        else:
            if (target_angle_velocity == 0):
                target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(50 * (distance-radius) * np.cos(theta) + distance, 50 * (distance-radius) * np.sin(theta) + distance))
            else:
                t_velocity, t_angle_velocity = Navigation.goToPoint(self.robot, Point(50 * (distance-radius) * np.cos(theta) + distance, 50 * (distance-radius) * np.sin(theta) + distance))
                target_velocity += t_velocity
                target_angle_velocity += t_angle_velocity
        
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass
