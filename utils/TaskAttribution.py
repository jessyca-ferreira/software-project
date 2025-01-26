from utils.Point import Point
import numpy as np

class TaskAttribution:
    @staticmethod
    def attribute_task(id, targets, teammates, opponents):
        num_targets = len(targets)
                
        goals = [[0 for i in range(num_targets)] for j in range(len(teammates))]
        bids = [[-np.inf for i in range(num_targets)] for j in range(len(teammates))]
        costs = [[-Point(j.x, j.y).dist_to(targets[i]) for i in range(num_targets)] for j in teammates.values()]
        
        agent_index = 0
        
        for (i, agent) in enumerate(teammates.values()):        
            if (agent.id == id):
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
        return target_index
