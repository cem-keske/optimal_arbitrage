import gurobipy
import numpy as np
import pandas as pd


def count_cycles(purchase_schedule, delta_T_hours, charging_eff, batt_cap):
    return np.sum(purchase_schedule*delta_T_hours*charging_eff)/batt_cap


def combined_objective_cost(prices, emissions, w_emissions, w_prices=1):
    """

    :param prices:
    :param emissions:
    :param w_emissions:
    :param w_prices:
    :return:
    """
    if np.any(prices.ts != emissions.ts):
        raise Exception("prices.ts != mef.ts")
    combined_cost = w_prices * prices.prices + w_emissions * emissions.mef
    # combined_cost /= np.max(np.abs(combined_cost), axis=0)
    df = pd.DataFrame({"ts": prices.ts, "combined_cost": combined_cost, "prices": prices.prices, "emissions": emissions.mef})
    return df


def compute_real_degr(A,B,soc_schedule,shelf_degr):
    degr = []
    for i in range(len(soc_schedule)-1):
        phi1 = A*(1-soc_schedule[i])**B
        phi2 = A*(1-soc_schedule[i+1])**B
        d = np.maximum(np.abs(phi1-phi2)/2, shelf_degr)

        degr.append(d)

    return np.cumsum(degr)