import numpy as np
import Environment as ev


class Robot(object):
    # 角度采用角度制而不是弧度制，原因是整数更便于储存
    def __init__(self, w=80, h=40, l1=70, l2=30, theta1=0, theta2=0):
        # 关键属性
        self.w = w
        self.h = h
        self.l1 = l1
        self.l2 = l2
        self.theta1 = theta1
        self.theta2 = theta2
        self.currentPosX = 50
        # 导出属性,注意这里的坐标都是自建参考系的相对坐标
        self.posA = 0, 0
        self.posB = w, 0
        self.posC = w, h
        self.posD = 0, h
        self.posE = w + np.sin(np.deg2rad(theta1)) * l1, h + np.cos(np.deg2rad(theta1)) * l1
        self.posP = self.calculate_pos_p()

    # 计算P点在相对坐标的位置
    def calculate_pos_p(self):
        x = self.w + np.sin(np.deg2rad(self.theta1)) * self.l1 + np.sin(np.deg2rad(self.theta1 + self.theta2)) * self.l2
        y = self.h + np.cos(np.deg2rad(self.theta1)) * self.l1 + np.cos(np.deg2rad(self.theta1 + self.theta2)) * self.l2
        return x, y

    # 计算旋转矩阵
    def calculate_rotation_matrix(self):
        if self.posP[1] >= 0:
            return np.matrix([[1, 0], [0, 1]])  # 返回单位阵表示无旋转
        d = (self.posP[0] ** 2 + self.posP[1] ** 2) ** 0.5
        cos_phi = self.posP[0] / d
        sin_phi = -self.posP[1] / d
        return np.matrix([[cos_phi, -sin_phi], [sin_phi, cos_phi]])

    def update_all_pos(self):
        self.posE = self.w + np.sin(np.deg2rad(self.theta1)) * self.l1, \
                    self.h + np.cos(np.deg2rad(self.theta1)) * self.l1
        self.posP = self.calculate_pos_p()

    def get_all_positions(self) -> np.array:
        return np.array([self.posA, self.posB, self.posC, self.posD, self.posE, self.posP])

    def get_current_pos_x(self):
        return self.currentPosX

    def get_all_positions_in_world_frame(self):
        X = self.get_all_positions().T
        return np.array((np.dot(self.calculate_rotation_matrix(), X) + np.array([[self.currentPosX], [0]])).T)
