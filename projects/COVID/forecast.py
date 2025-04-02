import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
from sklearn import metrics

#The SIR model as a series of transition states.
def sir_ode(y, t, N, beta, γ):
    S, I, R = y
    dSdt = -beta * I * S / N
    dIdt = beta * S * I / N - γ * I
    dRdt = γ * I
    return dSdt, dIdt, dRdt

def sir_model(β, γ, N, I0, R0, n = 30):
    t =  np.linspace(0, n, n, endpoint = False)
    S0 = N - I0 - R0
    y0 = S0, I0, R0

    ret = odeint(sir_ode, y0, t, args=(N, β, γ))
    S, I, R = ret.T
    return S, I, R

class SIR:
    def __init__(self, β, γ, N):
        self.β = β
        self.γ = γ
        self.N = N

    def predict(self, infected_init, recovered_init, forecast_horizon):
        return sir_model(self.β,self.γ, self.N, I0 = infected_init, R0 = recovered_init, n = forecast_horizon)


def loss(β, N, γ, I0, R0, y_true, n, metric = metrics.mean_squared_error, weights = False):
    #Model scenario
    β = float(β)
    S, I, R = sir_model(β, γ, N, I0, R0, n)
    assert len(I) == len(y_true)
    if weights:
        # model values closer to present higher
        return metric(y_true, I, sample_weight = [i+1 for i in range(I)])
    else:
        return metric(y_true, I)

def optimize_fit(β0, N, γ, I0, R0, y_true, n, metric = metrics.mean_squared_error, weights = False):
    return minimize(loss, [β0], args=(N, γ, I0, R0, y_true, n, metric, weights)).x[0]

def pre_process(history, γ_inverse, FIPS = None):
    columns = history.columns
    assert 'cases' in columns
    assert 'countyFIPS' in columns
    assert 'population' in columns

    if FIPS is not None:
        location_history = history[history['countyFIPS'] == FIPS]
    
    location_history['recovered cases'] = location_history.shift(periods = γ_inverse)['cases']
    location_history['active cases'] = location_history['cases'] - location_history['recovered cases']
    y0 = dict(location_history.iloc[-1])
    
    return y0['population'], y0['active cases'], y0['recovered cases']

