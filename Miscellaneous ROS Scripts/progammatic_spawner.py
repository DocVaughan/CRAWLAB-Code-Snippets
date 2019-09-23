###############################################################################
# progammatic_spawner.py
#
# Script exploring programmatically spawning objects in Gazebo. 
# 
# If these are spawned with the Gazebo physics running, we should drop them from
# the same height, but at different xy locations. This will let them fall into 
# a pile.
#
# If we spawn with physics pauses, we need to be more careful about the initial
# location to prevent "explosions" from the overlap of the objects.
#
# Note: A Gazebo environment should already be open adn running when this script
#       run.
#  
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 09/23/19
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu or vaughanje@ornl.gov
#   - @doc_vaughan
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 
###############################################################################

import rospy
import tf
# import actionlib
import numpy as np

from std_msgs.msg import String
# from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
# from actionlib_msgs.msg import *

from gazebo_msgs.srv import DeleteModel, SpawnModel, GetModelState 
from geometry_msgs.msg import *

if __name__ == '__main__':
    print("Waiting for gazebo services...")
    rospy.init_node("progammatic_spawner")
    rospy.wait_for_service("gazebo/delete_model")
    rospy.wait_for_service("gazebo/spawn_sdf_model")
    print("Got it.")
    
    delete_model = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)
    spawn_model = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)
    get_model_state = rospy.ServiceProxy("/gazebo/get_model_state", GetModelState)

    # TODO: Update to point to environmental variable for gazebo models
    with open("/home/josh/.gazebo/models/wood_cube_10cm/model.sdf", "r") as f:
        wood_cube_10cm_xml = f.read()

    
    # TODO: Update to point to environmental variable for gazebo models
    with open("/home/josh/.gazebo/models/wood_cube_5cm/model.sdf", "r") as f:
        wood_cube_5cm_xml = f.read()

    
    # TODO: Update to point to environmental variable for gazebo models
    with open("/home/josh/.gazebo/models/wood_cube_2_5cm/model.sdf", "r") as f:
        wood_cube_2p5cm_xml = f.read()

    # Define the number of each size cube to spawn
    NUM_10CM = 10
    NUM_5CM = 50
    NUM_2p5CM = 0
    NUM_CUBES_TOTAL = NUM_10CM + NUM_5CM + NUM_2p5CM
    random_item_extensions = 1000 * np.random.sample(1000)
    base_item_names = []
    item_names = []

    # Generate a list of item names to allow manipulation, property checking,
    # and deletion later. The name is needed
    for index in range(NUM_CUBES_TOTAL):
        base_item_names.append('cube_{:04d}'.format(int(random_item_extensions[index])))


    for index, item_name in enumerate(base_item_names):
        print(index)

        if index < NUM_10CM:
            x_position = 2 + np.random.random() - 0.5 # Random position
            y_position = 2 + np.random.random() - 0.5 # Random position
            z_position = 1.0                          # Random position

            orientation = Quaternion(0,0,0,1) #tf.transformations.quaternion_from_euler(0, 0, 0))

            current_item_name = "{}_10p0cm".format(item_name)

            print("Spawning model: {}".format(current_item_name))

            item_pose = Pose(Point(x=x_position, y=y_position, z=z_position), orientation)
            spawn_model(current_item_name, wood_cube_10cm_xml, "", item_pose, "world")
        
        elif index < NUM_10CM + NUM_5CM:
            x_position = 1.5 + 0.2 * np.random.random() - 0.1 # Random position
            y_position = 1.5 + 0.2 * np.random.random() - 0.1 # Random position
            z_position = 1.0                                  # Random position

            orientation = Quaternion(0,0,0,1) #tf.transformations.quaternion_from_euler(0, 0, 0))

            current_item_name = "{}_05p0cm".format(item_name)

            print("Spawning model: {}".format(current_item_name))

            item_pose = Pose(Point(x=x_position, y=y_position, z=z_position), orientation)
            spawn_model(current_item_name, wood_cube_5cm_xml, "", item_pose, "world")
        
        else:
            x_position = 1.0 + 0.2 * np.random.random() - 0.1 # Random position
            y_position = 1.0 + 0.2 * np.random.random() - 0.1 # Random position
            z_position = 1.0                                  # Random position

            orientation = Quaternion(0,0,0,1) #tf.transformations.quaternion_from_euler(0, 0, 0))

            current_item_name = "{}_02p5cm".format(item_name)

            print("Spawning model: {}".format(current_item_name))

            item_pose = Pose(Point(x=x_position, y=y_position, z=z_position), orientation)
            spawn_model(current_item_name, wood_cube_2p5cm_xml, "", item_pose, "world")

        # Append the current item name to the full list of names. This is crude
        # and could be done more efficient, but should work for this exploratory
        # script.
        item_names.append(current_item_name)

    rospy.sleep(5)

    # We can get the state of those objects
    item_names.sort()
    example_model_name = item_names[25]
    get_model_state(example_model_name, "ground_plane")


    # We can also delete all those objects, using their item name
    for item in item_names:
        print("Deleting model: {}", item)
        delete_model(item)

    # # Spawn 10 10cm cubes
    # for num in range(NUM_10CM):
    #     x_position = 2 + 0.2 * np.random.random() - 0.1 # Random position
    #     y_position = 2 + 0.2 * np.random.random() - 0.1 # Random position
    #     z_position = 1.0 * np.random.random()           # Random position

    #     orientation = Quaternion(0,0,0,1) #tf.transformations.quaternion_from_euler(0, 0, 0))

    #     item_names = "cube_{0}_10cm_{1}".format(num, int(100 *  np.random.random()))

    #     print("Spawning model: {}".format(item_name))

    #     item_pose = Pose(Point(x=x_position, y=y_position, z=z_position), orientation)
    #     spawn_model(item_name, wood_cube_10cm_xml, "", item_pose, "world")

    # # Spawn 25 5cm cubes
    # for num in range(NUM_5CM):
    #     x_position = 1 + 0.2 * np.random.random() - 0.1 # Random position
    #     y_position = 1 + 0.2 * np.random.random() - 0.1 # Random position
    #     z_position = 1.0 * np.random.random()           # Random position

    #     orientation = Quaternion(0,0,0,1) #tf.transformations.quaternion_from_euler(0, 0, 0))

    #     item_name = "cube_{0}_5cm_{1}".format(num, int(100 *  np.random.random()))

    #     print("Spawning model: {}".format(item_name))

    #     item_pose = Pose(Point(x=x_position, y=y_position, z=z_position), orientation)
    #     spawn_model(item_name, wood_cube_5cm_xml, "", item_pose, "world")

    # # Spawn 100 2.5cm cubes
    # for num in xrange(NUM_2p5CM):
    #     x_position = 0.5 + 0.2 * np.random.random() - 0.1 # Random position
    #     y_position = 0.5 + 0.2 * np.random.random() - 0.1 # Random position
    #     z_position = 1.0 * np.random.random()           # Random position

    #     orientation = Quaternion(0,0,0,1) #tf.transformations.quaternion_from_euler(0, 0, 0))

    #     item_name = "cube_{0}_2p5cm_{1}".format(num, int(100 *  np.random.random()))

    #     print("Spawning model: {}".format(item_name))

    #     item_pose = Pose(Point(x=x_position, y=y_position, z=z_position), orientation)
    #     spawn_model(item_name, wood_cube_2p5cm_xml, "", item_pose, "world")
