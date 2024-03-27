import numpy as np
from collections import defaultdict

class Simulation:

    def __init__(self, batt_cap=1000,
                 eff_round_trip=0.9,
                 c_rate=1,
                 soc_init=0.5,
                 soc_max=1,
                 soc_min=0.2,
                 self_discharge_per_hour=0,
                 p_co2=0.1,
                 start_date="",
                 end_date="",
                 price_data="",
                 emission_data="",
                 textinfo="",
                 save_results=False,
                 folder_name="",
                 degradation_profile=defaultdict(lambda: 0),
                 replacement_cost=0,
                 salvage_value=0,
                 life_cycle_emissions=0,
                 shelf_life_years=15,
                 horizon = 8760):

        self.batt_cap = batt_cap
        self.eff_round_trip = eff_round_trip
        self.c_rate = c_rate
        self.soc_init = soc_init
        self.soc_max = soc_max
        self.soc_min = soc_min
        self.self_discharge_per_hour = self_discharge_per_hour
        self.p_co2 = p_co2
        self.start_date = start_date
        self.end_date = end_date
        self.price_data = price_data
        self.emission_data = emission_data
        self.textinfo = textinfo
        self.save_results = save_results
        self.folder_name = folder_name
        self.degradation_profile = degradation_profile
        self.replacement_cost = replacement_cost
        self.salvage_value = salvage_value
        self.life_cycle_emissions = life_cycle_emissions
        self.shelf_life_years = shelf_life_years
        self.horizon = horizon