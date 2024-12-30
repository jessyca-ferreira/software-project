import numpy as np
from gymnasium.spaces import Box
from rsoccer_gym.Entities import Ball, Frame, Robot
from rsoccer_gym.ssl.ssl_gym_base import SSLBaseEnv
from utils.Point import Point
import random
import pygame


class SSLExampleEnv(SSLBaseEnv):
    def __init__(self, render_mode=None):
        field = 2 # SSL Division A Field
        super().__init__(field_type=field, n_robots_blue=1,
                         n_robots_yellow=0, time_step=0.025)
        n_obs = 4 # Ball x,y and Robot x, y
        self.action_space = Box(low=-1, high=1, shape=(2, ))
        self.observation_space = Box(low=-self.field.length/2,\
            high=self.field.length/2,shape=(n_obs, ))
        
        self.target = Point(0,0)

    def _frame_to_observations(self):
        ball, robot = self.frame.ball, self.frame.robots_blue[0]
        return np.array([ball.x, ball.y, robot.x, robot.y])

    def _get_commands(self, actions):
        robot_pos = Point(x=self.frame.robots_blue[0].x,
                          y=self.frame.robots_blue[0].y)

        if robot_pos.dist_to(self.target) < 0.2:
            self.target = Point(x=self.x(), y=self.y())

        robot_to_target = (self.target - robot_pos).normalize()
            
        return [Robot(yellow=False, id=0,
                      v_x=robot_to_target.x, v_y=robot_to_target.y)]

    def _calculate_reward_and_done(self):
        if self.frame.ball.x > self.field.length / 2 \
            and abs(self.frame.ball.y) < self.field.goal_width / 2:
            reward, done = 1, True
        else:
            reward, done = 0, False
        return reward, done
    
    def x(self):
        return random.uniform(-self.field.length/2 + 0.2, self.field.length/2 - 0.2)

    def y(self):
        return random.uniform(-self.field.width/2 + 0.2, self.field.width/2 - 0.2)
    
    def _get_initial_positions_frame(self):

        pos_frame: Frame = Frame()

        pos_frame.ball = Ball(x=self.x(), y=self.y())

        pos_frame.robots_blue[0] = Robot(x=self.x(), y=self.y(), theta=0.0)

        self.target = Point(x=self.x(), y=self.y())

        return pos_frame
    
    def step(self, action):
        super().render()
        next_state, reward, terminated, _ = super().step(action)
        return next_state, reward, terminated, False, {}
 
    def render(self, mode='human'):
        # def pos_transform(pos_x, pos_y):
        #     return (
        #         int(pos_x * self.field_renderer.scale + self.field_renderer.center_x),
        #         int(pos_y * self.field_renderer.scale + self.field_renderer.center_y),
        #     )

        super().render()
        self.draw_target(
            self.view,
            # pos_transform,
            self.target,
            (255, 0, 0),
        )

    def draw_target(self, screen, point, color):
        pygame.draw.circle(screen, color, point, 100, 5)