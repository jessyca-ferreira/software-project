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
        s = 2
        
        distance = self.pos.dist_to(self.targets[0])
        theta = np.arctan2(self.targets[0].y - self.pos.y, self.targets[0].x - self.pos.x)
        
        print(self.targets[0], self.pos, distance)
        
        if distance < radius:
            self.targets.pop(0)
            return

        if distance > s+radius:
            target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(50*s*np.cos(theta)+distance, 50*s*np.sin(theta)+distance))
        else:
            target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(50 * (distance-radius) * np.cos(theta) + distance, 50 * (distance-radius) * np.sin(theta) + distance))
        
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass
