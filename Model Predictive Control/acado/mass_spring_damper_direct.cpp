/* ----------------------------------------------------------------------------

mass_spring_damper_direct.cpp

Acado toolkit MPC setup for a simple mass-spring-damper system. This 
version solves and simulations the problem directly using the acado toolkit.

Nominal model is:
         +---> x              +---> y
         |                    |
     +--------+     k     +--------+
     |        |---/\/\/---|        |
u -->|   m1   |           |   m2   |
     |        |-----]-----|        |
     +--------+     c     +--------+


Created: 08/27/19
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

---------------------------------------------------------------------------- */


#include <acado_toolkit.hpp>
#include <acado_gnuplot.hpp>
// #include <acado_code_generation.hpp>

using namespace std;

USING_NAMESPACE_ACADO

int main( ) {
    // Define the system parameters
    const double m1 = 1.0;                          // mass 1 (kg)
    const double m2 = 1.0;                          // mass 1 (kg)
    const double k = 2.0 * pow((2.0 * M_PI), 2);    // spring constant (N/m) 
    const double c = 1.0;                           // damping coefficient (N/m/s)
    const double MAX_FORCE = 50.0;                  // maximum force from actuator (N)
    const double MIN_FORCE = -50.0;                 // minimum force from actuator (N)

    // Define the MPC solution time-related parameters    
    const int N  = 20;          // Number of timesteps to solve over
    const int Ni = 4;           // Number of integration steps per time step
    const double Ts = 0.05;     // Sampling time (s) for the MPC solution
    
    // Define the state variables
    DifferentialState x;
    DifferentialState x_dot; 
    DifferentialState y;    
    DifferentialState y_dot;        

    // Define the controller input
    Control u;

    // Define the differential equations
    DifferentialEquation f;
    
    // System differential equations
    f << dot(x) == x_dot;
    f << dot(x_dot) == k/m1 * (y - x) + c/m1 * (y_dot - x_dot) + u/m1;
    f << dot(y) == y_dot;
    f << dot(y_dot) == -k/m2 * (y - x) - c/m2 * (y_dot - x_dot);    
    
    // Define the weighting matrices and reference functions
    // Function describing the desired state trajectory
    Function desired_states;            
    
    // Function defining the desired final states
    Function desired_states_final;

    // Include all the states in those functions
    desired_states << x << x_dot << y << y_dot << u;
    desired_states_final << x << x_dot << y << y_dot;


    // Define the components of the cost function
    Function h;

    h << x;
    h << x_dot;
    h << y;
    h << y_dot;
    h << u;

    // Provide defined weighting matrices
    DMatrix Q(5, 5);
    Q.setIdentity();
	Q(0,0) = 1.0e6;
	Q(1,1) = 10.0;
    Q(2,2) = 1.0e6;
    Q(3,3) = 10.0;
    Q(4,4) = 1.0e-6;

    // Define the state reference vector
    DVector r(4);
    r.setAll(0.0);

    // Define the Optimal Control Problem (OCP)
    // We're solving at N steps between time 0 and N*Ts
    OCP ocp(0.0, N * Ts, N);

    // subject to the system ODEs
    ocp.subjectTo(f);
    
    // control constraints
    ocp.subjectTo(MIN_FORCE <= u <= MAX_FORCE);

    // Add the objective function for the state trajectory
    ocp.minimizeLSQ(Q, h, r);
    
    // We also must explicitly include a minimization for the final state
    //ocp.minimizeLSQEndTerm(Q_final, desired_states_final);

    // Set up the simulation
	OutputFcn identity;
	DynamicSystem dynamicSystem(f, identity);

	Process process(dynamicSystem, INT_RK45);

    // Set up the MPC algorithm as a real time controller
	RealTimeAlgorithm alg(ocp, 0.05);
	alg.set(MAX_NUM_ITERATIONS, 2);
	
	StaticReferenceTrajectory zeroReference;

	Controller controller(alg, zeroReference);


    // Set up the simulation environment and run it.
	SimulationEnvironment sim(0.0, 3.0, process, controller);

    // Define the initial conditions
	DVector x0(4);
	x0(0) = 1.0;    // x position (m)
	x0(1) = 0.0;    // x velocity (m/s)
    x0(2) = 1.0;    // y position (m)
	x0(3) = 0.0;    // y velocity (m/s)

	if (sim.init( x0 ) != SUCCESSFUL_RETURN) {
		exit( EXIT_FAILURE );
    }
	
    if (sim.run( ) != SUCCESSFUL_RETURN) {
		exit( EXIT_FAILURE );
    }

    // Now, plot the results
	VariablesGrid sampledProcessOutput;
	sim.getSampledProcessOutput(sampledProcessOutput);

	VariablesGrid feedbackControl;
	sim.getFeedbackControl(feedbackControl);

	GnuplotWindow window;
	window.addSubplot(sampledProcessOutput(0), "m1 (m)" );
    window.addSubplot(sampledProcessOutput(2), "m2 (m)" );
	window.addSubplot(feedbackControl(0),      "Force (N)" );
	window.plot();

    return EXIT_SUCCESS;
}