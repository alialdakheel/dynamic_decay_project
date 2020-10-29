"""
Plot results of experiment
"""

import matplotlib.pyplot as plt
import seaborn as sns

def level_vs_time_subplots(dfs, conf):
    cols = 1
    fig, ax_arr = plt.subplots(len(dfs)//cols, cols, sharex=True)

    for i, (ax, df) in enumerate(zip(ax_arr.flatten(), dfs)):
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
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_title(conf[i].split('___')[-1])
    fig.text(0.5, 0.04, "Time (s)", va='center', ha='center',)
    fig.text(0.04, 0.5, "Level (mean, std)", va='center', ha='center', rotation='vertical')
    fig.subplots_adjust(left=0.08, right=0.94, bottom=0.1, top=0.94, hspace=0.2)
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
    level_vs_time_subplots(dfs, config_list)


