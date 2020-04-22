#! /usr/bin/env python

###############################################################################
# inverse_kinematics_example.py
#
# This script uses a Jacobian generated in SymPy (sympy_inverseKinematics_example.py)
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 04/22/20
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - @doc_vaughan
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#    *  
#
# TODO:
#    * 04/22/20 - JEV - Using arrays for links and angles is probably better
###############################################################################

import numpy as np
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt

def jacobian_num(l_0, l_1, l_2, l_3, l_4, theta_0, theta_1, theta_2, theta_3):
    return np.array([[-l_2 * np.sin(theta_1) * np.cos(theta_0) - l_3 * (np.sin(theta_1) * np.cos(theta_2) + np.sin(theta_2) * np.cos(theta_1)) * np.cos(theta_0) - l_4 * ((-np.sin(theta_2) * np.sin(theta_3) + np.cos(theta_2) * np.cos(theta_3)) * np.sin(theta_1) + (np.sin(theta_2) * np.cos(theta_3) + np.sin(theta_3) * np.cos(theta_2)) * np.cos(theta_1)) * np.cos(theta_0), -l_2 * np.sin(theta_0) * np.cos(theta_1) - l_3 * (-np.sin(theta_1) * np.sin(theta_2) + np.cos(theta_1) * np.cos(theta_2)) * np.sin(theta_0) - l_4 * ((-np.sin(theta_2) * np.sin(theta_3) + np.cos(theta_2) * np.cos(theta_3)) * np.cos(theta_1) - (np.sin(theta_2) * np.cos(theta_3) + np.sin(theta_3) * np.cos(theta_2)) * np.sin(theta_1)) * np.sin(theta_0), -l_3 * (-np.sin(theta_1) * np.sin(theta_2) + np.cos(theta_1) * np.cos(theta_2)) * np.sin(theta_0) - l_4 * ((-np.sin(theta_2) * np.sin(theta_3) + np.cos(theta_2) * np.cos(theta_3)) * np.cos(theta_1) + (-np.sin(theta_2) * np.cos(theta_3) - np.sin(theta_3) * np.cos(theta_2)) * np.sin(theta_1)) * np.sin(theta_0), -l_4 * ((-np.sin(theta_2) * np.sin(theta_3) + np.cos(theta_2) * np.cos(theta_3)) * np.cos(theta_1) + (-np.sin(theta_2) * np.cos(theta_3) - np.sin(theta_3) * np.cos(theta_2)) * np.sin(theta_1)) * np.sin(theta_0)],
                     [-l_2 * np.sin(theta_0) * np.sin(theta_1) - l_3 * (np.sin(theta_1) * np.cos(theta_2) + np.sin(theta_2) * np.cos(theta_1)) * np.sin(theta_0) - l_4 * ((-np.sin(theta_2) * np.sin(theta_3) + np.cos(theta_2) * np.cos(theta_3)) * np.sin(theta_1) + (np.sin(theta_2) * np.cos(theta_3) + np.sin(theta_3) * np.cos(theta_2)) * np.cos(theta_1)) * np.sin(theta_0),  l_2 * np.cos(theta_0) * np.cos(theta_1) + l_3 * (-np.sin(theta_1) * np.sin(theta_2) + np.cos(theta_1) * np.cos(theta_2)) * np.cos(theta_0) + l_4 * ((-np.sin(theta_2) * np.sin(theta_3) + np.cos(theta_2) * np.cos(theta_3)) * np.cos(theta_1) - (np.sin(theta_2) * np.cos(theta_3) + np.sin(theta_3) * np.cos(theta_2)) * np.sin(theta_1)) * np.cos(theta_0),  l_3 * (-np.sin(theta_1) * np.sin(theta_2) + np.cos(theta_1) * np.cos(theta_2)) * np.cos(theta_0) + l_4 * ((-np.sin(theta_2) * np.sin(theta_3) + np.cos(theta_2) * np.cos(theta_3)) * np.cos(theta_1) + (-np.sin(theta_2) * np.cos(theta_3) - np.sin(theta_3) * np.cos(theta_2)) * np.sin(theta_1)) * np.cos(theta_0),  l_4 * ((-np.sin(theta_2) * np.sin(theta_3) + np.cos(theta_2) * np.cos(theta_3)) * np.cos(theta_1) + (-np.sin(theta_2) * np.cos(theta_3) - np.sin(theta_3) * np.cos(theta_2)) * np.sin(theta_1)) * np.cos(theta_0)],
                     [                                                                                                                                                                                                                                                                          0,                                      -l_2 * np.sin(theta_1) + l_3 * (-np.sin(theta_1) * np.cos(theta_2) - np.sin(theta_2) * np.cos(theta_1)) + l_4 * (-(-np.sin(theta_2) * np.sin(theta_3) + np.cos(theta_2) * np.cos(theta_3)) * np.sin(theta_1) + (-np.sin(theta_2) * np.cos(theta_3) - np.sin(theta_3) * np.cos(theta_2)) * np.cos(theta_1)),                             l_3 * (-np.sin(theta_1) * np.cos(theta_2) - np.sin(theta_2) * np.cos(theta_1)) + l_4 * ((np.sin(theta_2) * np.sin(theta_3) - np.cos(theta_2) * np.cos(theta_3)) * np.sin(theta_1) + (-np.sin(theta_2) * np.cos(theta_3) - np.sin(theta_3) * np.cos(theta_2)) * np.cos(theta_1)),                l_4 * ((np.sin(theta_2) * np.sin(theta_3) - np.cos(theta_2) * np.cos(theta_3)) * np.sin(theta_1) + (-np.sin(theta_2) * np.cos(theta_3) - np.sin(theta_3) * np.cos(theta_2)) * np.cos(theta_1))]])

def endpoint_position(l_0, l_1, l_2, l_3, l_4, theta_0, theta_1, theta_2, theta_3):
    return np.array([-l_2 * np.sin(theta_0) * np.sin(theta_1) - l_3 * (np.sin(theta_1) * np.cos(theta_2) + np.sin(theta_2) * np.cos(theta_1)) * np.sin(theta_0) - l_4 * ((-np.sin(theta_2) * np.sin(theta_3) + np.cos(theta_2) * np.cos(theta_3)) * np.sin(theta_1) + (np.sin(theta_2) * np.cos(theta_3) + np.sin(theta_3) * np.cos(theta_2)) * np.cos(theta_1)) * np.sin(theta_0),
                    l_2 * np.sin(theta_1) * np.cos(theta_0) + l_3 * (np.sin(theta_1) * np.cos(theta_2) + np.sin(theta_2) * np.cos(theta_1)) * np.cos(theta_0) + l_4 * ((-np.sin(theta_2) * np.sin(theta_3) + np.cos(theta_2) * np.cos(theta_3)) * np.sin(theta_1) + (np.sin(theta_2) * np.cos(theta_3) + np.sin(theta_3) * np.cos(theta_2)) * np.cos(theta_1)) * np.cos(theta_0),
                    l_0 + l_1 + l_2 * np.cos(theta_1) + l_3 * (-np.sin(theta_1) * np.sin(theta_2) + np.cos(theta_1) * np.cos(theta_2)) + l_4 * ((-np.sin(theta_2) * np.sin(theta_3) + np.cos(theta_2) * np.cos(theta_3)) * np.cos(theta_1) - (np.sin(theta_2) * np.cos(theta_3) + np.sin(theta_3) * np.cos(theta_2)) * np.sin(theta_1))])

# Define the link lengths - all in meters
link_0 = 0.102
link_1 = 0.041
link_2 = 0.107
link_3 = 0.107
link_4 = 0.090

# Define the current joint angles. Note that the Jacobian approximation will
# only be much good near these points. So, if this method is being used over a
# trajectory, then these values need to be updated and the transpose 
# re-calculated in each loop of the control loop. We do this in the loop below.
initial_theta_0 = 1e-3
initial_theta_1 = 1e-3
initial_theta_2 = 1e-3
initial_theta_3 = 1e-3

# The current angles match the initial ones here
current_theta_0 = initial_theta_0 
current_theta_1 = initial_theta_1 
current_theta_2 = initial_theta_2 
current_theta_3 = initial_theta_3 

# Find the current endpoint position given the initial joint angles
initial_position = endpoint_position(link_0, link_1, link_2, link_3, link_4,
                                     initial_theta_0, initial_theta_1,
                                     initial_theta_2, initial_theta_3)


# Define the desired position. 
# NOTE: We are not doing any checks that this is actually a point the system
# can reach. In general, we should.
x_desired = 0.0
y_desired = 0.1
z_desired = 0.2
desired_position = np.array([x_desired, y_desired, z_desired])

# And calculate the error
error_vector = desired_position - initial_position
position_error = euclidean(desired_position, initial_position)

# To calculate the necessary angles, we loop until our endpoint position is 
# within a small error bound around the desired position. In practice, this 
# error bound would need to be tuned, and you should add a timeout or counter
# on the calculation to ensure that we don't get stuck in this loop.
while position_error > 1e-3:
    # Uncomment to track the convergence to the final position
    print('Position Error: {:8.4f}'.format(position_error))

    current_jacobian = jacobian_num(link_0, link_1, link_2, link_3, link_4,
                                    current_theta_0, current_theta_1,
                                    current_theta_2, current_theta_3)
    
    # This, alpha, term acts something like a proportional gain on the solution
    # If it is too large, you will get oscillation or instability. Too small,
    # and the solution might take a long time to converge
    alpha = 1.0
    
    # Get the angles using the transpose of the jacobian_num
    # joint_angle_changes = current_jacobian.transpose().dot(alpha * error_vector)
    
    # Or try the pseudo-inverse instead, which should converge to the solution
    # more quickly
    joint_angle_changes = np.linalg.pinv(current_jacobian).dot(alpha * error_vector)

    # Update the joint angles
    current_theta_0 = current_theta_0 + joint_angle_changes[0]
    current_theta_1 = current_theta_1 + joint_angle_changes[1] 
    current_theta_2 = current_theta_2 + joint_angle_changes[2] 
    current_theta_3 = current_theta_3 + joint_angle_changes[3] 
    
    # Let's check the answer by plugging those angles back into the 
    # forward kinematics. We'll use this calculated position to calculate 
    # the error from our desired location, and will repeat this process 
    # if necessary.
    current_position = endpoint_position(link_0, link_1, link_2, link_3, link_4,
                                         current_theta_0, current_theta_1,
                                         current_theta_2, current_theta_3)
    
    # Update the error
    error_vector = desired_position - current_position
    position_error = euclidean(desired_position, current_position)


# Since we're going to print NumPy arrays, let's set up that formatting
np.set_printoptions(precision=4, sign=' ')
print('\nFinal position:           {} m'.format(current_position))
print('Desired position:         {} m'.format(desired_position))
print('Euclidian distance error: {:7.4f} m'.format(position_error))

print('Required joint angles:    ({:+7.4f}, {:+7.4f}, {:+7.4f}, {:+7.4f}) deg'.format(np.rad2deg(current_theta_0),
                                                                                      np.rad2deg(current_theta_1),
                                                                                      np.rad2deg(current_theta_2),
                                                                                      np.rad2deg(current_theta_3)))


# The solution might return multiple rotations of a joint. 
# Here, we first limit the solution to 0-2*pi rad. (0-360 deg)
current_theta_0 = np.abs(current_theta_0) % (2 * np.pi) * np.sign(current_theta_0)
current_theta_1 = np.abs(current_theta_1) % (2 * np.pi) * np.sign(current_theta_1)
current_theta_2 = np.abs(current_theta_2) % (2 * np.pi) * np.sign(current_theta_2)
current_theta_3 = np.abs(current_theta_3) % (2 * np.pi) * np.sign(current_theta_3)

# Then, we correct for angle 'wrap around' to limit the angle to +/-180deg
# This is a every inelegant way of doing this, but works for this basic demo.
if current_theta_0 > np.pi:
    current_theta_0 -= (2 * np.pi)
elif current_theta_0 < -np.pi:
    current_theta_0 += (2 * np.pi)

if current_theta_1 > np.pi:
    current_theta_1 -= (2 * np.pi)
elif current_theta_1 < -np.pi:
    current_theta_1 += (2 * np.pi)

if current_theta_2 > np.pi:
    current_theta_2 -= (2 * np.pi)
elif current_theta_2 < -np.pi:
    current_theta_2 += (2 * np.pi)

if current_theta_3 > np.pi:
    current_theta_3 -= (2 * np.pi)
elif current_theta_3 < -np.pi:
    current_theta_3 += (2 * np.pi)

# And recalculate the position to be sure the angle limited version still 
# reached the same position. Truly accounting for joint limits is beyond the
# scope of this basic example.
calculated_position = endpoint_position(link_0, link_1, link_2, link_3, link_4,
                                         current_theta_0, current_theta_1,
                                         current_theta_2, current_theta_3)


print('\nLimited joint angles:     ({:+7.4f}, {:+7.4f}, {:+7.4f}, {:+7.4f}) deg'.format(np.rad2deg(current_theta_0),
                                                                                        np.rad2deg(current_theta_1),
                                                                                        np.rad2deg(current_theta_2),
                                                                                        np.rad2deg(current_theta_3)))

print('Revised position:         {} m\n'.format(calculated_position))