from Robot import *
import random


class QLearningRobot(Robot):
    def __init__(self, alpha, discount, epsilon, w=60, h=40, l1=70, l2=45, theta1=60, theta2=0):
        super().__init__(w, h, l1, l2, theta1, theta2)
        self.alpha = alpha
        self.discount = discount
        self.epsilon = epsilon
        self.q_value_table = {}

    def run_one_step(self):
        delta_1 = random.randint(-1, 1)
        delta_2 = random.randint(-1, 1)
        # 以epsilon的概率随机行动
        if np.random.rand() < self.epsilon:
            pass
        else:
            # calc the argMax Q-value of the current state
            maxQ = 0
            argMaxQ = 1, 1
            if (self.theta1, self.theta2) in self.q_value_table:
                q_values_of_actions = self.q_value_table[(self.theta1, self.theta2)]
                for action in q_values_of_actions:
                    if q_values_of_actions[action] > maxQ:
                        maxQ = q_values_of_actions[action]
                        argMaxQ = action
            delta_1, delta_2 = argMaxQ
        # print(delta_1)
        # next-state
        new_theta1, new_theta2, new_x = ev.get_next_state(self, delta_1, delta_2)
        # calc reward of this action
        reward = new_x - self.currentPosX
        # calc the max Q-value of the next state
        maxQ = 0
        if (new_theta1, new_theta2) in self.q_value_table:
            q_values_of_actions = self.q_value_table[(new_theta1, new_theta2)]
            for action in q_values_of_actions:
                if q_values_of_actions[action] > maxQ:
                    maxQ = q_values_of_actions[action]
        sample = self.discount * maxQ + reward
        # update current q-state
        if (self.theta1, self.theta2) not in self.q_value_table:
            self.q_value_table[(self.theta1, self.theta2)] = {}
        q_values_of_actions = self.q_value_table[(self.theta1, self.theta2)]
        if (delta_1, delta_2) not in q_values_of_actions:
            q_values_of_actions[(delta_1, delta_2)] = 0
        # 算法核心，更新 Q-value
        current_q = q_values_of_actions[(delta_1, delta_2)]
        q_values_of_actions[(delta_1, delta_2)] = (1 - self.alpha) * current_q + self.alpha * sample

        # 更新物理属性
        self.currentPosX = new_x
        self.theta1, self.theta2 = new_theta1, new_theta2
        self.update_all_pos()

    def go_home(self,alpha,discount,epsilon):
        self.__init__(alpha, discount, epsilon)