# Sistema que calcula a pressão a ser colocada em um freio de carro de acordo 
# com a velocity do carro e distância do obstáculo.

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def braking_pressure():
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

    # Rules

    rules = []

    rules.append( ctrl.Rule(distance['good'], pressure['low']) )
    rules.append( ctrl.Rule(distance['average'], pressure['medium']) )
    rules.append( ctrl.Rule(distance['poor'], pressure['high']) )

    rules.append( ctrl.Rule(velocity['good'], pressure['high']) )
    rules.append( ctrl.Rule(velocity['average'], pressure['medium']) )
    rules.append( ctrl.Rule(velocity['poor'], pressure['low']) )

    rules.append( ctrl.Rule(velocity['good'] & distance['poor'], pressure['high']) )
    rules.append( ctrl.Rule(velocity['poor'] & distance['poor'], pressure['medium']) )
    rules.append( ctrl.Rule(velocity['poor'] & distance['good'], pressure['low']) )

    return ctrl.ControlSystem(rules), pressure


if __name__ == '__main__':
    
    braking_ctrl, pressure = braking_pressure()
    i = 1

    while True:
        try:
            print('--------  {}  --------'.format(i))

            braking = ctrl.ControlSystemSimulation(braking_ctrl)

            braking.input['distance'] = float(input('DISTANCE: '))
            braking.input['velocity'] = float(input('VELOCITY: '))

            braking.compute()

            print('PRESSURE:', braking.output['pressure'])
            print()
            pressure.view(sim=braking)
        except KeyboardInterrupt as e:
            break