import numpy as np
import collections


class SIR_model():
    SIR = collections.namedtuple(
        typename='SIRComponents',
        field_names=[
            'S',
            'I',
            'R',
            'i'])

    ModelParams = collections.namedtuple(
        typename='ModelParams',
        field_names=[
            'beta',
            't_I'  # t_I = 1/gamma
        ]
    )

    def __init__(self, data):
        """
        data: simulate_data
        """
        self.data = data
        beta = data.construct_beta(data.rt, data.t_I)
        self.x = self.SIR(
            S=data.S0,
            I=data.I0,
            R=0,
            i=0
        )
        self.θ = self.ModelParams(beta, data.t_I)

    def f(self, t, x, θ, N, dt=1, noise_param=1/25):
        """
        State transition function.
            Args:
                t: time
                x: state space
                θ: parameters
                N: population
                dt: time step in days
        """

        # Stochastic transitions
        dSI = np.random.poisson(x.S * x.I / N * θ.beta)  # S to I
        dIR = np.random.poisson(x.I / θ.t_I)  # I to R

        # OEV = np.maximum(1., dSI**2 * noise_param)
        # OEV_sample= np.random.normal(0, 1, size=len(dSI))
        # i_noise = dSI + OEV_sample * np.sqrt(OEV)

        # Updates
        x_new = self.SIR(
            S=np.clip(x.S - dSI, 0, N),
            I=np.clip(x.I + dSI - dIR, 0, N),
            R=np.clip(x.R + dIR, 0, N),
            i=np.clip(dSI, 0, N)
        )

        return x_new

    def h(self, x):
        """
        Observational function.
            Args:
                x: state space
        """
        # y = np.random.binomial(x.i.astype(int), α)
        return x.i

    def f0(self, pop, m=300):
        """
        Initial guess of the state space.
            Args:
                pop: population
                m: number of ensemble members
        """
        #     I0 = pop * inf_init
        #     S0 = pop - I0
        #     R0 = 0
        #     i = 0
        S0 = np.random.uniform(pop*0.8, pop, size=m)
        I0 = pop - S0
        R0 = np.zeros(m)
        i0 = np.zeros(m)

        x0 = self.SIR(
            S=S0,
            I=I0,
            R=R0,
            i=i0
        )
        return x0

    def θ0(self, prior, m=300):
        """
        Initial guess of the parameter space.
            Args:
                prior: prior
                m: number of ensemble members
        """
        beta = prior['beta']['dist'](**prior['beta']['args'], size=m)
        θ0 = self.ModelParams(beta=beta, t_I=np.ones(m) * self.data.t_I)
        return θ0