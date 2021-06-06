#! /usr/bin/env python

###############################################################################
# sympy_inverseKinematics_example.py
#
# An example of using SymPy to solve the inverse kinematics via the Jacobian. 
# In this simple example, we only specify the position of the endpoint, not
# its orientation. We're also doing it completely in SymPy, so the solution 
# will be fairly slow. If we needed to do this quickly, we should move to NumPy
# after we've calculated the Jacobian (preferably in a different script).
#
# This version also uses a weighted-Jacobian approach, which we can use to 
# push the solution toward a desired configuration, such as preferring 
# motion in one joint over another.
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 06/06/21
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - @doc_vaughan
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 04/22/20 - JEV - If all initial angles are *exactly* zero *and* any one 
#                      of the a desired positions is *exactly* zero, then the 
#                      solution will not converge.
###############################################################################


# import all the necessary packages
import sympy
import numpy as np

from sympy.physics.mechanics import dynamicsymbols
from sympy.physics.mechanics import Point, ReferenceFrame
from sympy.physics.mechanics import mechanics_printing

# Use basic, non-pretty printing 
mechanics_printing(pretty_print=False)

# Define generalized coordinates
theta0, theta1, theta2, theta3 = dynamicsymbols('theta_0 theta_1 theta_2 theta_3')

# Define first derivatives of generalized coordinates
theta0dot, theta1dot, theta2dot, theta3dot = dynamicsymbols('theta_0 theta_1 theta_2 theta_3', 1)

# Define symbols for other parameters
# Link lengths
l0, l1, l2, l3, l4 = sympy.symbols('l_0 l_1 l_2 l_3 l_4', real=True, nonzero=True)

# Time and gravity
t, g = sympy.symbols('t g', real=True, nonzero=True)

# -----  Define reference frames -----
N = ReferenceFrame('N')

# Define body fixed frame that rotates with Theta 0
XYZ1 = N.orientnew('XYZ1', 'Axis', [theta0, N.z])

# Define new frame to align new z-axis along the link l1
XYZ2 = XYZ1.orientnew('XYZ2', 'Axis', [-theta1, XYZ1.x])

# Define new frame to align new z-axis along the link l2
XYZ3 = XYZ2.orientnew('XYZ3', 'Axis', [-theta2, XYZ2.x])

# Define new frame to align new z-axis along the link l3
XYZ4 = XYZ3.orientnew('XYZ4', 'Axis', [-theta3, XYZ3.x])


# ----- Define points of interest and their velocities -----
# Define Origin and its velocity
O = Point('O')
O.set_vel(N, 0 * N.x)

# Define point P0 and its velocity relative to Origin (Located at servo that controls theta0)
P0 = O.locatenew('P0', l0 * N.z)
P0.set_vel(N, 0 * N.x)

# Define point P1 and its velocity (Located at servo that controls theta1)
P1 = P0.locatenew('P1', l1 * XYZ1.z)
P1.set_vel(N, 0 * N.x)

# Define CoM of first link (Just halfway up first servo)
G1 = P1.locatenew('G1', (l1 / 2) * N.z)
G1.set_vel(N, 0 * N.x)

# Define point point P2 and its velocity (Located at servo that controls theta2)
P2 = P1.locatenew('P2', l2 * XYZ2.z)
P2.v2pt_theory(P1, N, XYZ2)

# Define CoM of 2nd link
G2 = P1.locatenew('G2', (l2 / 2) * XYZ2.z)
G2.v2pt_theory(P1, N, XYZ2)

# Define point P3 and its velocity (Located at servo that controls theta3)
P3 = P2.locatenew('P3', l3 * XYZ3.z)
P3.v2pt_theory(P2, N, XYZ3)

# Define CoM of 3rd link
G3 = P2.locatenew('G3', (l3 / 2) * XYZ3.z)
G3.v2pt_theory(P2, N, XYZ3)

# Define point P4 and its velocity (Located at EE)
P4 = P3.locatenew('P4', l4 * XYZ4.z)
P4.v2pt_theory(P3, N, XYZ4)

# Define CoM of the 4th link
G4 = P3.locatenew('G4', (l4 / 2) * XYZ4.z)
G4.v2pt_theory(P3, N, XYZ4)

# Now that we've defined all the points, we can get the XYZ components of the 
# endpoint position relative to the origin, written in the fixed frame
x_component = P4.pos_from(O).express(N).dot(N.x)
y_component = P4.pos_from(O).express(N).dot(N.y)
z_component = P4.pos_from(O).express(N).dot(N.z)

# We then pack these into a sympy Matrix, so that we can use the .jacobian()
# method, rather than having to take all the partial derivatives manually
F = sympy.Matrix([x_component, y_component, z_component])

# Now, compute the Jacobian with respect to each angle
jacobian = F.jacobian([theta0, theta1, theta2, theta3])

# Prescribe the link lengths
jacobian = jacobian.subs([(l0, 0.102), 
                          (l1, 0.041), 
                          (l2, 0.107), 
                          (l3, 0.107), 
                          (l4, 0.090)])

# We'll substitute the lengths into the endpoint position vector outside
# the loop below, so that fewer parameters needs to be updated via the .subs()
# command during each time through the loop. This should speed up the loop.
endpoint_position_vector = P4.pos_from(O).express(N).subs([(l0, 0.102), 
                                                           (l1, 0.041), 
                                                           (l2, 0.107), 
                                                           (l3, 0.107), 
                                                           (l4, 0.090)])


# Define the current joint angles. Note that the Jacobian approximation will
# only be much good near these points. So, if this method is being used over a
# trajectory, then these values need to be updated and the transpose 
# re-calculated in each loop of the control loop. We do this in the loop below.
# TODO: 04/22/20 - JEV - All of these being *exactly* zero *and* a desired 
#                        being *exactly* zero will result in the solution not 
#                        converging.
current_theta0 = 1e-3
current_theta1 = np.pi/4
current_theta2 = np.pi/4
current_theta3 = np.pi/4

# Find the current endpoint position given the prescribed current joint angles
current_position = endpoint_position_vector.subs([(theta0, current_theta0), 
                                                  (theta1, current_theta1), 
                                                  (theta2, current_theta2), 
                                                  (theta3, current_theta3)])

# Define the desired position. 
# NOTE: We are not doing any checks that this is actually a point the system
# can reach. In general, we should.
# (0, 0.25, 0.155) is approx tbe position with (0, 45deg, 45deg, 45deg)
desired_x = 0.0
desired_y = 0.25
desired_z = 0.1

# Alternately, define the displacement from the current configuration
# NOTE: We are not doing any checks that this is actually a point the system
# can reach. In general, we should.
# desired_x = current_position.dot(N.x) + 0.1
# desired_y = current_position.dot(N.y) + 0.2
# desired_z = current_position.dot(N.z) - 0.2

# Create a vector from those desired locations
desired_position = desired_x * N.x + desired_y * N.y + desired_z * N.z

# And calculate the error
error_vector = desired_position - current_position
position_error = sympy.sqrt(error_vector.dot(error_vector))

# Now, specify the weighting matrix
# Higher values of qN penalize changes in that angle more
q0 = 1.0  # weight on theta0 changes
q1 = 1.0  # weight on theta1 changes
q2 = 1e3  # weight on theta2 changes
q3 = 1.0  # weight on theta3 changes
weighting = sympy.Matrix([[q0, 0, 0, 0],
                          [0, q1, 0, 0],
                          [0, 0, q2, 0],
                          [0, 0, 0, q3]])


# To calculate the necessary angles, we loop until our endpoint position is 
# within a small error bound around the desired position. In practice, this 
# error bound would need to be tuned, and you should add a timeout or counter
# on the calculation to ensure that we don't get stuck in this loop.

loop_count = 0
while position_error > 1e-3 and loop_count < 100:
    # Uncomment to track the convergence to the final position
    print('Position Error: {:8.4f}'.format(position_error))

    current_jacobian = jacobian.subs([(theta0, current_theta0), 
                                      (theta1, current_theta1), 
                                      (theta2, current_theta2), 
                                      (theta3, current_theta3)])

    # This, alpha, term acts something like a proportional gain on the solution
    # If it is too large, you will get oscillation or instability. Too small,
    # and the solution might take a long time to converge
    alpha = 0.5

    # Create the desired change in position based on the error vector and the 
    # alpha parameter scaling
    desired_delta_x = alpha * error_vector.dot(N.x)
    desired_delta_y = alpha * error_vector.dot(N.y)
    desired_delta_z = alpha * error_vector.dot(N.z)
    desired_delta_pos = sympy.Matrix([desired_delta_x, desired_delta_y, desired_delta_z])

    # Now, we form the weighted Jacaobian pseudo-inverse
    weighting_term = weighting.inv() * current_jacobian.transpose()
    weighted_jacobian_pinv = weighting_term * (current_jacobian * weighting_term).inv()
    
    # Or try the pseudo-inverse instead, which should converge to the solution
    # more quickly
    delta_joint_angles = weighted_jacobian_pinv * desired_delta_pos
    
    print(delta_joint_angles)

    # Update the joint angles
    current_theta0 = current_theta0 + delta_joint_angles[0]
    current_theta1 = current_theta1 + delta_joint_angles[1]
    current_theta2 = current_theta2 + delta_joint_angles[2]
    current_theta3 = current_theta3 + delta_joint_angles[3]

    # The solution might return multiple rotations of a joint. 
    # Here, we first limit the solution to 0-2*pi rad. (0-360 deg)
    current_theta0 = np.abs(current_theta0) % (2 * np.pi) * np.sign(current_theta0)
    current_theta1 = np.abs(current_theta1) % (2 * np.pi) * np.sign(current_theta1)
    current_theta2 = np.abs(current_theta2) % (2 * np.pi) * np.sign(current_theta2)
    current_theta3 = np.abs(current_theta3) % (2 * np.pi) * np.sign(current_theta3)

    # Then, we correct for angle 'wrap around' to limit the angle to +/-180deg
    # This is a every inelegant way of doing this, but works for this basic demo.
    if current_theta0 > np.pi:
        current_theta0 -= (2 * np.pi)
    elif current_theta0 < -np.pi:
        current_theta0 += (2 * np.pi)

    if current_theta1 > np.pi:
        current_theta1 -= (2 * np.pi)
    elif current_theta1 < -np.pi:
        current_theta1 += (2 * np.pi)

    if current_theta2 > np.pi:
        current_theta2 -= (2 * np.pi)
    elif current_theta2 < -np.pi:
        current_theta2 += (2 * np.pi)

    if current_theta3 > np.pi:
        current_theta3 -= (2 * np.pi)
    elif current_theta3 < -np.pi:
        current_theta3 += (2 * np.pi)
    
    # Let's check the answer by plugging those angles back into the 
    # forward kinematics. Given we used the transpose approximation, the point 
    # should be closer to, but not exactly match our desired configuration. 
    # Note that in this simple, basic formulation, we are not doing any checks 
    # that the desired point is even reachable by the system. We'll use this 
    # calculated position to calculate the error from our desired location, 
    # and will repeat this process if necessary.
    calculated_position = endpoint_position_vector.subs([(theta0, current_theta0), 
                                                         (theta1, current_theta1), 
                                                         (theta2, current_theta2), 
                                                         (theta3, current_theta3)])
    
    # And calculate the resulting error.
    current_position = calculated_position
    error_vector = desired_position - current_position
    position_error = sympy.sqrt(error_vector.dot(error_vector))
    
    loop_count = loop_count + 1


# Wrap in float() to avoid the sympy Zero type
x_pos = float(calculated_position.dot(N.x).evalf())
y_pos = float(calculated_position.dot(N.y).evalf())
z_pos = float(calculated_position.dot(N.z).evalf())
current_theta0 = float(current_theta0)
current_theta1 = float(current_theta1)
current_theta2 = float(current_theta2)
current_theta3 = float(current_theta3)


print('\nFinal position:           ({:+7.4f}, {:+7.4f}, {:+7.4f}) m'.format(x_pos, y_pos, z_pos))
print('Desired position:         ({:+7.4f}, {:+7.4f}, {:+7.4f}) m'.format(desired_x, desired_y, desired_z))
print('Euclidian distance error:  {:7.4f} m'.format(position_error))

print('Required joint angles:    ({:+7.4f}, {:+7.4f}, {:+7.4f}, {:+7.4f}) deg'.format(np.rad2deg(current_theta0),
                                                                                  np.rad2deg(current_theta1),
                                                                                  np.rad2deg(current_theta2),
                                                                                  np.rad2deg(current_theta3)))