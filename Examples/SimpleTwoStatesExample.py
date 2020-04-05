# This example is written for the new interface
import StateModeling as stm

M = stm.Model()  # creates a new Model instance
M.newState(name='S0', axesInit=0.0)  # ground state
S1 = M.newVariables({'S1': 1.0})  # transition rate
M.newState(name='S1', axesInit=S1)  # excited state. Systems starts in the excited state
true_I0 = 1200; true_k = 0.135
M.newVariables({'k': true_k})  # transition rate
I0 = M.newVariables({'I0': true_I0})  # transition rate
M.addRate('S1', 'S0', 'k')  # S1 --> S0  first order decay leading to a single exponential decay
M.addResult('detected', lambda State: I0 * State['S1'])  # ('I', 'S')
M.toFit(['k', 'S1'])   # fitting S1 works, but not fitting I0 !
# M.toFit(['k'])

# simulate data

Tmax = 80
measured = M.simulate('measured', {'detected': 0}, Tmax=Tmax, applyPoisson=True)

# Fit with distorted starting values
M.relDistort({'k':0.8, 'I0':1.2})
distorted = M.simulate('distorted', {'detected': 0}, Tmax=Tmax)

if True:
    otype = "L-BFGS"
    lossScale = 1e5
else:
    lossScale = None
    otype = "adagrad" # "adadelta" "SGD" "nesterov"  "adam"
fittedVars, fittedRes = M.fit({'detected': measured}, Tmax, otype=otype, NIter=150, verbose=True,  lossScale=lossScale)

M.showResults(ylabel='Intensity')
M.showStates()