import numpy as np
import pandas as pd

from utils.mape import mape
from utils.plotting import plot_results, plot_error_histograms, plot_power_error
from utils.run_opendc import runOpenDC

def evaluate_results(all_cineca_dfs, all_sim_dfs):
    temp_mape_results = []
    power_mape_results = []

    for i, (cineca_df, sim_df) in enumerate(zip(all_cineca_dfs, all_sim_dfs)):
        temp_mape = mape(cineca_df.total_cpu_temp, sim_df.temperature_C)
        power_mape = mape(cineca_df.total_cpu_power, sim_df.power_draw)

        temp_mape_results.append(temp_mape)
        power_mape_results.append(power_mape)

    plot_results(all_cineca_dfs, all_sim_dfs)
    plot_error_histograms(all_cineca_dfs, all_sim_dfs)
    plot_power_error(all_cineca_dfs, all_sim_dfs)

    return temp_mape_results, power_mape_results


def match_dataframe_lengths(df1: pd.DataFrame, df2: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    len1 = len(df1)
    len2 = len(df2)

    if len1 > len2:
        df1 = df1.iloc[:len2]
    elif len2 > len1:
        df2 = df2.iloc[:len1]

    return df1, df2


def read_cineca(node):
    cineca_df = pd.read_parquet(
        f'Input/M100_input/power_temp_node-26{node}')
    cineca_df = cineca_df.sort_values(by='timestamp').reset_index()

    # add p1_power and p0_power to a new column called total_cpu_power
    cineca_df['total_cpu_power'] = cineca_df['p0_power'] + cineca_df['p1_power']

    # add avg_core_temp_0 and avg_core_temp_1 to a new column called total_cpu_temp
    cineca_df['total_cpu_temp'] = cineca_df['avg_core_temp_0'] + cineca_df['avg_core_temp_1']

    return cineca_df


def read_sim(node):
    sim_df = pd.read_parquet(f'Output/cineca/raw-output/{node}/seed=0/host.parquet')
    sim_df = sim_df.sort_values(by='timestamp').reset_index()

    return sim_df


if __name__ == "__main__":
    runOpenDC("Input/scenarios/cineca.json")

    all_cineca_dfs = []
    all_sim_dfs = []

    for i in range(6):
        print(f"Calling for node {i}")

        sim_df, cineca_df = match_dataframe_lengths(read_sim(i), read_cineca(i))
        all_cineca_dfs.append(cineca_df)
        all_sim_dfs.append(sim_df)

    temp_mape_results, power_mape_results = evaluate_results(all_cineca_dfs, all_sim_dfs)

    temp_mape_results.append(np.mean(temp_mape_results))
    power_mape_results.append(np.mean(power_mape_results))

    mape_data = list(zip(temp_mape_results, power_mape_results))

    # Create the DataFrame with the correct columns
    mape_df = pd.DataFrame(mape_data, columns=['temp_mape', 'power_mape'])
    print(mape_df)

    mape_df.to_csv('Output/mape_results.csv', index=True)
