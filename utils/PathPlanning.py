from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point
import numpy as np

class PathPlanning:
    @staticmethod
    def get_directions(robot, opponents, radius, s, pos, targets, target_index):
        target_velocity = Point(0, 0)
        target_angle_velocity = 0
        
        distance = pos.dist_to(targets[target_index])
        theta = np.arctan2(targets[target_index].y - pos.y, targets[target_index].x - pos.x)
        for opponent in opponents.values():
            distance_opponent = pos.dist_to(Point(opponent.x, opponent.y))
            theta_opponent = np.arctan2(opponent.y - pos.y, opponent.x - pos.x)
            
            if distance_opponent < radius:
                target_velocity, target_angle_velocity = Navigation.goToPoint(robot, Point(-np.sign(np.cos(theta_opponent))*1.5, -np.sign(np.cos(theta_opponent))*1.5))
            elif distance_opponent > s+radius:
                t_velocity, t_angle_velocity = Navigation.goToPoint(robot, Point(80*s*np.cos(theta_opponent), 80*s*np.sin(theta_opponent)))
                target_velocity += t_velocity
                target_angle_velocity += t_angle_velocity
            elif distance_opponent < s+radius:
                t_velocity, t_angle_velocity = Navigation.goToPoint(robot, Point(-50*(s+radius-distance_opponent)*np.cos(theta_opponent), -50*(s+radius-distance_opponent)*np.sin(theta_opponent)))
                target_velocity += t_velocity
                target_angle_velocity += t_angle_velocity

            if distance > s+radius:
                if (target_angle_velocity == 0):
                    target_velocity, target_angle_velocity = Navigation.goToPoint(robot, Point(100*s*np.cos(theta), 100*s*np.sin(theta)))
                else:
                    t_velocity, t_angle_velocity = Navigation.goToPoint(robot, Point(100*s*np.cos(theta), 100*s*np.sin(theta)))
                    target_velocity += t_velocity
                    target_angle_velocity += t_angle_velocity
            else:
                if (target_angle_velocity == 0):
                    target_velocity, target_angle_velocity = Navigation.goToPoint(robot, Point(150 * (distance-radius) * np.cos(theta), 150 * (distance-radius) * np.sin(theta)))
                else:
                    t_velocity, t_angle_velocity = Navigation.goToPoint(robot, Point(150 * (distance-radius) * np.cos(theta), 150 * (distance-radius) * np.sin(theta)))
                    target_velocity += t_velocity
                    target_angle_velocity += t_angle_velocity
                    
        return target_velocity, target_angle_velocity