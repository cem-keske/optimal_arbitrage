import pandas as pd
import numpy as np
from datetime import datetime
import os
from utilities import count_cycles


def save_results(simulation, schedule, costs):
    filename = "[PCO2_" + str(simulation.p_co2) + "]_" + simulation.textinfo \
               + "_" + datetime.now().strftime("_%m_%d_%H_%M_%S") + '.xlsx'
    folder_name = os.path.join("05_Results", simulation.folder_name)
    working_dir = os.path.dirname(os.getcwd())
    save_folder = os.path.join(working_dir, folder_name)

    if not os.path.exists(save_folder):
        # Create a new directory because it does not exist
        os.makedirs(save_folder)
        print(F"The new save directory is created:\n\t{save_folder}")

    excel_file = os.path.join(working_dir, folder_name, filename)

    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    # compute metrics to save
    cycles = count_cycles(schedule.pcc_purchase_schedule,
                          charging_eff=np.sqrt(simulation.eff_round_trip),
                          batt_cap=simulation.batt_cap,
                          delta_T_hours=simulation.delta_T_hours)
    setattr(simulation, 'cycles', cycles)

    # Write each dataframe to a different worksheet.
    degradation = pd.DataFrame(simulation.degradation_profile.items(), columns=['soc', 'degradation'])
    simulation_df = pd.DataFrame(simulation.__dict__, index=[0])

    simulation_df.to_excel(writer, sheet_name='params & results')
    degradation.to_excel(writer, sheet_name='degradation_profile')
    schedule.to_excel(writer, sheet_name='schedule')
    costs.to_excel(writer, sheet_name='costs')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


def read_day_ahead_prices(str_date_start, str_date_end):
    filename = "02_PriceData/Day_Ahead/auction_spot_prices_germany_luxembourg_2020.csv"
    cols = list(pd.read_csv(filename, nrows=1))
    cols_to_read = [col for col in cols if ((col.find("Hour") == 0) or col == "Delivery day")]

    prices = pd.read_csv(filename, usecols=cols_to_read, parse_dates=["Delivery day"], dayfirst=True)
    year_begin = pd.to_datetime("00:00 01.10.2018 GMT-2", dayfirst=True).tz_convert("GMT").tz_localize(None)
    year_end = pd.to_datetime("23:00 31.12.2020 GMT-1", dayfirst=True).tz_convert("GMT").tz_localize(None)
    full_year_dates = pd.date_range(start=year_begin, end=year_end, freq="1H", inclusive='both')

    hour_cols = [col for col in cols_to_read if col != "Delivery day"]
    flatlist = np.flip(np.array(prices[hour_cols].to_numpy()), 0).flatten()

    flatlist = flatlist[~np.isnan(flatlist)]
    df = pd.DataFrame({'ts': full_year_dates, 'prices': flatlist})

    startdate = pd.to_datetime(str_date_start, dayfirst=True)
    enddate = pd.to_datetime(str_date_end, dayfirst=True)

    date_filter = [(startdate <= val < enddate) for val in df['ts']]
    filtered_prices = df[date_filter]

    return pd.DataFrame({'ts': [v for v in filtered_prices.ts], 'prices': [v for v in filtered_prices.prices]})


def read_ef(mef_filename, str_date_start, str_date_end):
    ''' Reads MEF values from a given file name (absolute).

    inputs:

        mef_filename: input file name
        str_date_start: string for the starting date in GMT
        str_date_end: string for the ending name in GMT

    returns:

        dataframe:  [ts, mef]

    '''

    startdate = pd.to_datetime(str_date_start, dayfirst=True)
    enddate = pd.to_datetime(str_date_end, dayfirst=True)

    marginal_emission_factors = pd.read_csv(mef_filename, parse_dates=['datetime'])

    date_filter = [(val >= startdate) & (val < enddate) for val in
                   marginal_emission_factors['datetime'].dt.tz_convert('GMT').dt.tz_localize(
                       None)]
    dates = [val for val in marginal_emission_factors['datetime'].dt.tz_convert('GMT').dt.tz_localize(None)
             if (val >= startdate) & (val < enddate)]

    filtered_mef = marginal_emission_factors[date_filter].copy().rename(columns={"datetime": "ts",
                                                                                 "carbon_intensity_avg": "mef"},
                                                                        errors="raise")

    filtered_mef.ts = filtered_mef.ts.dt.tz_convert('GMT').dt.tz_localize(None)

    return pd.DataFrame({'ts': dates, 'mef': [val for val in filtered_mef.mef]})


def read_aef(aef_filename, str_date_start, str_date_end):
    ''' Reads AEF values from a given file name (absolute). However, outputs them as MEF for compatibility.

    inputs:

        mef_filename: input file name
        str_date_start: string for the starting date in GMT
        str_date_end: string for the ending name in GMT

    returns:

        dataframe:  [ts, mef]

    '''

    startdate = pd.to_datetime(str_date_start, dayfirst=True)
    enddate = pd.to_datetime(str_date_end, dayfirst=True)

    marginal_emission_factors = pd.read_csv(aef_filename, parse_dates=['datetime'])

    date_filter = [(val >= startdate) & (val < enddate) for val in
                   marginal_emission_factors['datetime'].dt.tz_convert('GMT').dt.tz_localize(
                       None)]
    dates = [val for val in marginal_emission_factors['datetime'].dt.tz_convert('GMT').dt.tz_localize(None)
             if (val >= startdate) & (val < enddate)]

    filtered_mef = marginal_emission_factors[date_filter].copy().rename(columns={"datetime": "ts",
                                                                                 "carbon_intensity_avg": "mef"},
                                                                        errors="raise")

    filtered_mef.ts = filtered_mef.ts.dt.tz_convert('GMT').dt.tz_localize(None)

    return pd.DataFrame({'ts': dates, 'mef': [val for val in filtered_mef.mef]})
