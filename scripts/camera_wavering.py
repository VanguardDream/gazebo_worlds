from math import degrees, radians
import rospy
import math
import numpy as np

from scipy.spatial.transform import Rotation as Rot
from gazebo_msgs.msg import *
from gazebo_msgs.srv import SetModelState

def set_camera_state(x, y, z, theta, phi, psi):
    #default x : 0
    #default y : 0
    #default z : 7
    #default theta  (r) : 0
    #default phi    (p) : 90
    #default psi    (y) : 0

    state = ModelState()
    state.model_name = 'camera'
    state.pose.position.x = x
    state.pose.position.y = y
    state.pose.position.z = z

    _eul = np.array([theta, phi, psi])
    _rot = Rot.from_euler('xyz', _eul, degrees=True)

    quat = _rot.as_quat()

    state.pose.orientation.x = quat[0]
    state.pose.orientation.y = quat[1]
    state.pose.orientation.z = quat[2]
    state.pose.orientation.w = quat[3]

    # rospy.wait_for_service('/gazebo/set_model_state')

    # try:
    #     rospy.ServiceProxy('/gazebo/set_model_state',SetModelState)
    #     resp = set_state(state)
    # except rospy.ServiceException as e:
    #     print(f"service call failed! : {e}")

    pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=1)
    pub.publish(state)


if __name__ == "__main__":
    rospy.init_node("wavering_camera_node")
    rate = rospy.Rate(75)

    # State Variables
    x = 0
    y = 0
    z = 7
    theta = 0
    phi = 90
    psi = 0

    # Wavering Variables
    t = 0


    while not rospy.is_shutdown():
        d = radians(t)
        set_camera_state(x - 0.01 * np.sin(d), \
                            y - 0.01 * np.sin(d), \
                                z - 0.02 * np.sin(d), \
                                    theta - 6 * np.sin(d), \
                                        phi - 6 * np.sin(d), \
                                            psi - 6 * np.sin(d)
                                            )
        t = t + 5
        rate.sleep()