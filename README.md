# Reconocimiento_voz_objetos_ROS
hola

```python
class Teleop:
    def __init__(self):
        self.velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
        self.pose_lite_publisher = rospy.Publisher('body_pose/raw', PoseLite, queue_size = 1)
        self.pose_publisher = rospy.Publisher('body_pose', Pose, queue_size = 1)
        self.joy_subscriber = rospy.Subscriber('joy', Joy, self.joy_callback)
        self.swing_height = rospy.get_param("gait/swing_height", 0)
        self.nominal_height = rospy.get_param("gait/nominal_height", 0)

        self.speed = rospy.get_param("~speed", 0.5)
        self.turn = rospy.get_param("~turn", 1.0)

```
