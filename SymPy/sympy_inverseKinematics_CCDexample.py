#! /usr/bin/env python

###############################################################################
# sympy_inverseKinematics_CCDexample.py
#
# An example of using SymPy to solve the inverse kinematics via the Jacobian. 
# In this simple example, we only specify the position of the endpoint, not
# its orientation. We're also doing it completely in SymPy, so the solution 
# will be fairly slow. We're using the Cyclic Coordinate Decent method.
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
#   * 
#
# TODO:
#   * 
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


# We'll substitute the lengths into the endpoint position vector outside
# the loop below, so that fewer parameters needs to be updated via the .subs()
# command during each time through the loop. This should speed up the loop.
P0_vector = P0.pos_from(O).express(N).subs([(l0, 0.102), 
                                              (l1, 0.041), 
                                              (l2, 0.107), 
                                              (l3, 0.107), 
                                              (l4, 0.090)])

P1_vector = P1.pos_from(O).express(N).subs([(l0, 0.102), 
                                              (l1, 0.041), 
                                              (l2, 0.107), 
                                              (l3, 0.107), 
                                              (l4, 0.090)])

P2_vector = P2.pos_from(O).express(N).subs([(l0, 0.102), 
                                              (l1, 0.041), 
                                              (l2, 0.107), 
                                              (l3, 0.107), 
                                              (l4, 0.090)])

P3_vector = P3.pos_from(O).express(N).subs([(l0, 0.102), 
                                              (l1, 0.041), 
                                              (l2, 0.107), 
                                              (l3, 0.107), 
                                              (l4, 0.090)])

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
current_theta1 = 1e-3
current_theta2 = 1e-3
current_theta3 = 1e-3

# Find the current joint and endpoint positions given the prescribed 
# current joint angles
P0_position = P0_vector.subs([(theta0, current_theta0), 
                                (theta1, current_theta1), 
                                (theta2, current_theta2), 
                                (theta3, current_theta3)])
                       
P1_position = P1_vector.subs([(theta0, current_theta0), 
                                (theta1, current_theta1), 
                                (theta2, current_theta2), 
                                (theta3, current_theta3)])
                                
P2_position = P2_vector.subs([(theta0, current_theta0), 
                                (theta1, current_theta1), 
                                (theta2, current_theta2), 
                                (theta3, current_theta3)])
                       
P3_position = P3_vector.subs([(theta0, current_theta0), 
                                (theta1, current_theta1), 
                                (theta2, current_theta2), 
                                (theta3, current_theta3)])
                       
endpoint_position = endpoint_position_vector.subs([(theta0, current_theta0), 
                                                   (theta1, current_theta1), 
                                                   (theta2, current_theta2), 
                                                   (theta3, current_theta3)])


# Define the desired position. 
# NOTE: We are not doing any checks that this is actually a point the system
# can reach. In general, we should.
desired_x = 0.1
desired_y = 0.1
desired_z = 0.2

# Alternately, define the displacement from the current configuration
# NOTE: We are not doing any checks that this is actually a point the system
# can reach. In general, we should.
# desired_x = current_position.dot(N.x) + 0.1
# desired_y = current_position.dot(N.y) + 0.2
# desired_z = current_position.dot(N.z) - 0.2

# Create a vector from those desired locations
desired_position = desired_x * N.x + desired_y * N.y + desired_z * N.z

# And calculate the error
error_vector = desired_position - endpoint_position
position_error = sympy.sqrt(error_vector.dot(error_vector))


# To calculate the necessary angles, we loop until our endpoint position is 
# within a small error bound around the desired position. In practice, this 
# error bound would need to be tuned, and you should add a timeout or counter
# on the calculation to ensure that we don't get stuck in this loop.
while position_error > 1e-3:
    # Uncomment to track the convergence to the final position
    print('Position Error: {:8.4f}'.format(position_error))

    # Start with the last joint
    joint_to_desired_term = (desired_position - P3_position) / (desired_position - P3_position).magnitude()
    joint_to_endpoint_term = (endpoint_position - P3_position) / (endpoint_position - P3_position).magnitude()
    
    delta_theta3 = sympy.acos(joint_to_endpoint_term.dot(joint_to_desired_term))
    direction = joint_to_endpoint_term.cross(joint_to_desired_term)
    
    if direction.dot(N.z) < 0:
        delta_theta3 = -delta_theta3
        
    current_theta3 = current_theta3 + delta_theta3
        
    # Now, "rotate" that link, updating the joint and endpoint positions
    P0_position = P0_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                       
    P1_position = P1_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                                
    P2_position = P2_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                       
    P3_position = P3_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                       
    endpoint_position = endpoint_position_vector.subs([(theta0, current_theta0), 
                                                       (theta1, current_theta1), 
                                                       (theta2, current_theta2), 
                                                       (theta3, current_theta3)])
    
    
    # Now, we move to the next joint - P2 and theta2
    joint_to_desired_term = (desired_position - P2_position) / (desired_position - P2_position).magnitude()
    joint_to_endpoint_term = (endpoint_position - P2_position) / (endpoint_position - P2_position).magnitude()
    
    delta_theta2 = sympy.acos(joint_to_endpoint_term.dot(joint_to_desired_term))
    direction = joint_to_endpoint_term.cross(joint_to_desired_term)
    
    if direction.dot(N.z) < 0:
        delta_theta2 = -delta_theta2
        
    current_theta2 = current_theta2 + delta_theta2
        
    # Now, "rotate" that link, updating the joint and endpoint positions
    P0_position = P0_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                       
    P1_position = P1_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                                
    P2_position = P2_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                       
    P3_position = P3_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                       
    endpoint_position = endpoint_position_vector.subs([(theta0, current_theta0), 
                                                       (theta1, current_theta1), 
                                                       (theta2, current_theta2), 
                                                       (theta3, current_theta3)])
    
    # Now, we move to the next joint - P1 and theta1
    joint_to_desired_term = (desired_position - P1_position) / (desired_position - P1_position).magnitude()
    joint_to_endpoint_term = (endpoint_position - P1_position) / (endpoint_position - P1_position).magnitude()
    
    delta_theta1 = sympy.acos(joint_to_endpoint_term.dot(joint_to_desired_term))
    direction = joint_to_endpoint_term.cross(joint_to_desired_term)
    
    if direction.dot(N.z) < 0:
        delta_theta1 = -delta_theta1
        
    current_theta1 = current_theta1 + delta_theta1
        
    # Now, "rotate" that link, updating the joint and endpoint positions
    P0_position = P0_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                       
    P1_position = P1_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                                
    P2_position = P2_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                       
    P3_position = P3_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                       
    endpoint_position = endpoint_position_vector.subs([(theta0, current_theta0), 
                                                       (theta1, current_theta1), 
                                                       (theta2, current_theta2), 
                                                       (theta3, current_theta3)])

    # Now, we move to the next joint - P0 and theta0
    joint_to_desired_term = (desired_position - P0_position) / (desired_position - P0_position).magnitude()
    joint_to_endpoint_term = (endpoint_position - P0_position) / (endpoint_position - P0_position).magnitude()
    
    delta_theta0 = sympy.acos(joint_to_endpoint_term.dot(joint_to_desired_term))
    direction = joint_to_endpoint_term.cross(joint_to_desired_term)
    
    if direction.dot(N.z) < 0:
        delta_theta0 = -delta_theta0
        
    current_theta0 = current_theta0 + delta_theta0
        
    # Now, "rotate" that link, updating the joint and endpoint positions
    P0_position = P0_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                       
    P1_position = P1_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                                
    P2_position = P2_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                       
    P3_position = P3_vector.subs([(theta0, current_theta0), 
                                    (theta1, current_theta1), 
                                    (theta2, current_theta2), 
                                    (theta3, current_theta3)])
                       
    endpoint_position = endpoint_position_vector.subs([(theta0, current_theta0), 
                                                       (theta1, current_theta1), 
                                                       (theta2, current_theta2), 
                                                       (theta3, current_theta3)])
    
    
    # And calculate the resulting error.
    current_position = endpoint_position
    error_vector = desired_position - current_position
    position_error = sympy.sqrt(error_vector.dot(error_vector))


# Wrap in float() to avoid the sympy Zero type
x_pos = float(endpoint_position.dot(N.x).evalf())
y_pos = float(endpoint_position.dot(N.y).evalf())
z_pos = float(endpoint_position.dot(N.z).evalf())
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

# And recalculate the position to be sure the angle limited version still 
# reached the same position. Truly accounting for joint limits is beyond the
# scope of this basic example.
calculated_position = endpoint_position_vector.subs([(theta0, current_theta0), 
                                                     (theta1, current_theta1), 
                                                     (theta2, current_theta2), 
                                                     (theta3, current_theta3)])

x_pos = float(calculated_position.dot(N.x).evalf())
y_pos = float(calculated_position.dot(N.y).evalf())
z_pos = float(calculated_position.dot(N.z).evalf())

print('\nLimited joint angles:     ({:+7.4f}, {:+7.4f}, {:+7.4f}, {:+7.4f}) deg'.format(np.rad2deg(current_theta0),
                                                                                        np.rad2deg(current_theta1),
                                                                                        np.rad2deg(current_theta2),
                                                                                        np.rad2deg(current_theta3)))

print('Revised position:         ({:+7.4f}, {:+7.4f}, {:+7.4f}) m\n'.format(x_pos, y_pos, z_pos))