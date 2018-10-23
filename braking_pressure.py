# Pressão freio de um carro (%), em relação à distância do obstáculo (0 a 100m) e à velocidade do carro (0 a 100km/h).


import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
# functions
distance = ctrl.Antecedent(np.arange(0, 101, 1), 'distance')
velocity = ctrl.Antecedent(np.arange(0, 101, 1), 'velocity')
pressure = ctrl.Consequent(np.arange(0, 101, 1), 'pressure')

# Auto-membership function population is possible with .automf(3, 5, or 7)
distance.automf(3)
velocity.automf(3)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
pressure['low'] = fuzz.trimf(pressure.universe, [0, 0, 30])
pressure['medium'] = fuzz.trimf(pressure.universe, [20, 50, 75])
pressure['high'] = fuzz.trimf(pressure.universe, [65, 100, 100])

# You can see how these look with .view()
# quality['average'].view()

# service.view()

# tip.view()

rules = []

rules.append( ctrl.Rule(distance['good'], pressure['low']) )
rules.append( ctrl.Rule(distance['average'], pressure['medium']) )
rules.append( ctrl.Rule(distance['poor'], pressure['high']) )

rules.append( ctrl.Rule(velocity['good'], pressure['high']) )
rules.append( ctrl.Rule(velocity['average'], pressure['medium']) )
rules.append( ctrl.Rule(velocity['poor'], pressure['low']) )


# rule1.view()

braking_ctrl = ctrl.ControlSystem(rules)

braking = ctrl.ControlSystemSimulation(braking_ctrl)

# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
braking.input['distance'] = 80
braking.input['velocity'] = 60

# Crunch the numbers
braking.compute()

print(braking.output['pressure'])
pressure.view(sim=braking)

input('ENTER TO EXIT')