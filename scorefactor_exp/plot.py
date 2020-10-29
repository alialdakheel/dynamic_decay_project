"""
Plot results of experiment
"""

import matplotlib.pyplot as plt
import seaborn as sns

def level_vs_time_subplots(dfs):
    cols = 1
    fig, ax_arr = plt.subplots(len(dfs)//cols, cols, sharex=True)

    for ax, df in zip(ax_arr.flatten(), dfs):
        g = sns.pointplot(
                x='time',
                y='level',
                data=df,
                scale=0.4,
                errwidth=0.3,
                ci='sd',
                ax=ax
                )
        ax.set_xticklabels(ax.get_xticklabels(),
                fontsize=6, rotation=43, ha="right")
    # plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    from parse_output import parse_exp_output, dict_to_dfs
    exp_outputs_dir = "exp_output"
    config_list = [
            "cadical-1.3.1-c9b8d0b67a123___sat_500",
            "cadical-1.3.1-c9b8d0b67a123___sat_950",
            "cadical-1.3.1-c9b8d0b67a123___unsat_500",
            "cadical-1.3.1-c9b8d0b67a123___unsat_950"
            ]
    res_dict = parse_exp_output(exp_outputs_dir, config_list)
    dfs = dict_to_dfs(res_dict)
    level_vs_time_subplots(dfs)


