"""
    Script to filter CaDiCal results.csv from SAT race 2019
"""

import pandas as pd

def load_dfs(file_name):
    results_df = pd.read_csv(file_name)

    cadical_df = results_df[results_df.solver==' CaDiCaL']

    cadical_sat_df = cadical_df[cadical_df.configuration == " sat"]
    cadical_unsat_df = cadical_df[cadical_df.configuration == " unsat"]

    return cadical_sat_df, cadical_unsat_df

def filter_complete(cadical_sat_df, cadical_unsat_df):
    """
    Given two dataframes filter out CNFs that are solved by both

    """
    cadical_unsat_df = cadical_unsat_df[cadical_unsat_df.status == " complete"]
    cadical_sat_df = cadical_sat_df[cadical_sat_df.status == " complete"]

    unsat_benchmark_list = [cnf for cnf in cadical_unsat_df.benchmark]
    sat_benchmark_list = [cnf for cnf in cadical_sat_df.benchmark]

    ind_sat_unsat = [cnf in unsat_benchmark_list for cnf in sat_benchmark_list]
    ind_unsat_sat = [cnf in sat_benchmark_list for cnf in unsat_benchmark_list]

    ind_cadical_sat = cadical_sat_df.benchmark[ind_sat_unsat].index
    cadical_sat_df = cadical_sat_df.loc[ind_cadical_sat]
    ind_cadical_unsat = cadical_unsat_df.benchmark[ind_unsat_sat].index
    cadical_unsat_df = cadical_unsat_df.loc[ind_cadical_unsat]

    cadical_sat_df.reset_index(drop=True, inplace=True)
    cadical_unsat_df.reset_index(drop=True, inplace=True)

    return cadical_sat_df, cadical_unsat_df

def filter_time(cadical_sat_df, cadical_unsat_df, factor=2):
    """
    Given two dataframes filter out CNFs that take less than a factor of 2 time
    to be solved by one of the modes.

    """
    benchmark_list = list(cadical_sat_df.benchmark)

    filtered_cnf_list = list()
    for cnf in benchmark_list:
        sat_time = cadical_sat_df[cadical_sat_df.benchmark == cnf]["solver time"]
        unsat_time = cadical_unsat_df[cadical_unsat_df.benchmark == cnf]["solver time"]
        ratio = float(sat_time) / float(unsat_time)
        if ratio >= factor or ratio <= 1/factor:
            filtered_cnf_list.append(cnf)

    return filtered_cnf_list


if __name__ == "__main__":
    benchmarks_filename = "results.csv"
    sat_df, unsat_df = load_dfs(benchmarks_filename)
    sat_df, unsat_df = filter_complete(sat_df, unsat_df)
    filtered_cnf_list = filter_time(sat_df, unsat_df, factor=1)

    # save_filename = "filtered_cnf_list"
    save_filename = "unfiltered_cnf_list"
    with open(save_filename, "w") as fp:
        fp.writelines([
            ".".join(cnf[4:].split(".")[:-1]) + "\n" for cnf in filtered_cnf_list
            ])

