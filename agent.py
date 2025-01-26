from utils.ssl.base_agent import BaseAgent
from utils.TaskAttribution import TaskAttribution
from utils.PathPlanning import PathPlanning

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)

    def decision(self):
        if len(self.targets) == 0:
            return
        
        # Utiliza definicao de min_dist do sslenv.py para definir o raio
        radius = 0.18
        step = 1.2
        
        target_index = TaskAttribution.attribute_task(self.id, self.targets, self.teammates, self.opponents)
        target_velocity, target_angle_velocity = PathPlanning.get_directions(self.robot, self.opponents, radius, step, self.pos, self.targets, target_index)
                    
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass
