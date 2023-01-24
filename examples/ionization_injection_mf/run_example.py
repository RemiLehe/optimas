"""
This example optimizes an LPA based on ionization injection using FBPIC
simulations with varying fidelity (resolution).

The FBPIC simulations are performed using the template defined in the
`template_simulation_script.py` file.

In addition to the objective `f`, three additional parameters
are analyzed for each simulation and including in the optimization
history. The calculation of `f` and the additional parameters is performed
in the `analyze_simulation` function, which for convenience is here defined in
the `analysis_script.py` file.
"""
from libe_opt.core import Parameter, VaryingParameter, Objective
from libe_opt.generators import AxMultiFidelityGenerator
from libe_opt.evaluators import TemplateEvaluator
from libe_opt.explorations import Exploration

from analysis_script import analyze_simulation


# Create varying parameters and objectives.
var_1 = VaryingParameter('laser_scale', 0.7, 1.05)
var_2 = VaryingParameter('z_foc', 3., 7.5)
var_3 = VaryingParameter('mult', 0.1, 1.5)
var_4 = VaryingParameter('plasma_scale', 0.6, 0.8)
res = VaryingParameter('resolution', 2., 4., is_fidelity=True,
                       fidelity_target_value=4.)
obj = Objective('f', minimize=True)


# Define additional parameters to analyze.
energy_med = Parameter('energy_med')
energy_mad = Parameter('energy_mad')
charge = Parameter('charge')


# Create generator.
gen = AxMultiFidelityGenerator(
    varying_parameters=[var_1, var_2, var_3, var_4, res],
    objectives=[obj],
    analyzed_parameters=[energy_med, energy_mad, charge],
    n_init=4
)


# Create evaluator.
ev = TemplateEvaluator(
    sim_template='template_simulation_script.py',
    analysis_func=analyze_simulation,
    n_gpus=1  # Use 1 GPU per simulation.
)


# Create exploration.
exp = Exploration(
    generator=gen,
    evaluator=ev,
    max_evals=100,
    sim_workers=4,
    run_async=True
)


# To safely perform exploration, run it in the block below (this is needed
# for some flavours of multiprocessing, namely spawn and forkserver)
if __name__ == '__main__':
    exp.run()