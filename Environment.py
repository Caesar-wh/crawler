import Robot
import numpy as np


def get_next_state(robot: Robot, delta_1, delta_2):
    # 先定每次操作角度
    def regular(x):
        if x > 0:
            return 2
        elif x < 0:
            return -2
        else:
            return 0

    # 用于限定范围
    def limit(x, low, up):
        if x < low:
            return low
        if x > up:
            return up
        return x

    # 限定范围
    delta_1 = regular(delta_1)
    delta_2 = regular(delta_2)
    # 注意 theta1+ theta2不能大于270度，否则该物理模型失效
    theta1 = limit(robot.theta1 + delta_1, 0, 100)
    theta2 = limit(robot.theta2 + delta_2, 0, 130)
    xp = robot.w + np.sin(np.deg2rad(theta1)) * robot.l1 + np.sin(np.deg2rad(theta1 + theta2)) * robot.l2
    yp = robot.h + np.cos(np.deg2rad(theta1)) * robot.l1 + np.cos(np.deg2rad(theta1 + theta2)) * robot.l2
    delta_x = 0
    if robot.posP[1] <= 0 and yp <= 0:
        delta_x = (robot.posP[0] ** 2 + robot.posP[1] ** 2) ** 0.5 - (xp ** 2 + yp ** 2) ** 0.5
    return theta1, theta2, robot.currentPosX + delta_x
