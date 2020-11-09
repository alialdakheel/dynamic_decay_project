"""
Plot results of experiment
"""

import matplotlib as matplt
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def level_vs_time_subplots(dfs, conf):
    cols = 1
    fig, ax_arr = plt.subplots(len(dfs)//cols, cols, sharex=True)

    for i, (ax, df) in enumerate(zip(ax_arr.flatten(), dfs)):
        g = sns.pointplot(
                x='time',
                y='level',
                data=df,
                linestyles='',
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

def level_vs_time(df, conf):
    markers = ['x', 'o', '^', 'v']
    # for c, marker in zip(conf, markers):
        # df_conf = df[df.config == c]
        # g = sns.pointplot(
                # y='level', x='time', hue='cnf', data=df_conf,
                # ci='sd',
                # scale=0.6,
                # markers=marker,
                # palette='Set2',
                # dodge=True
        # )
        # g.set_xticklabels(g.get_xticklabels(),
                # fontsize=6, rotation=43, ha="right")
        # g.set_xlabel("Time (s)")
        # g.set_ylabel("Level")
    df['config_sat'] = df.config.str.cat(df.sat_state, sep=', ').astype(str)
    g = sns.lineplot(
            x='level', y='time', hue='cnf', data=df[:100000],
            ci='sd',
            markers=True,
            dashes=False,
            err_style='bars',
            # scale=0.8,
            # errwidth=0.6,
            # markers='*',
            style='config',
            # style='config_sat',
            # style='sat_state',
            # palette='Set2',
            palette='Dark2',
            # dodge=True
    )
    # g.set_xticklabels(g.get_xticklabels(),
            # fontsize=6, rotation=43,
            # # ha="right"
            # )
    g.set_xlabel("Time (s)")
    g.set_ylabel("Level")
    g.legend('')
    plt.show()

def level_vs_time_sp2(df, conf):
    cols = 1
    fig, ax_arr = plt.subplots(len(conf)//cols, cols)
    ax_arr.flatten()
    for i, (c, marker) in enumerate(zip(conf, markers)):
        df_conf = df[df.config == c]
        g = sns.pointplot(
                y='level', x='time', hue='sat_state', data=df_conf,
                # order=df_conf.sort_values('av_level').time,
                ci='sd',
                scale=0.6,
                errwidth=0.5,
                # markers=marker,
                # palette=sns.color_palette('Spectral'),
                palette='tab20',
                ax=ax_arr[i]
        )
        g.legend('')
        ax = ax_arr[i]
        ax.set_xticklabels(ax.get_xticklabels(),
                fontsize=6, rotation=43, ha="right")
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_title(conf[i].split('___')[-1])
    fig.text(0.5, 0.04, "Time (s)", va='center', ha='center',)
    fig.text(0.04, 0.5, "Level (mean, std)", va='center', ha='center', rotation='vertical')
    fig.subplots_adjust(left=0.08, right=0.94, bottom=0.1, top=0.94, hspace=0.2)
    plt.show()

def level_vs_time_sp3(df, conf, savefig=False):
    cols = 2
    fig, ax_arr = plt.subplots(2*len(conf)//cols, cols)
    # ax_arr.flatten()
    for i, c in enumerate(conf):
        df_conf = df[df.config == c].sort_values('av_level')
        for i2, s in enumerate(df.sat_state.unique()):
            ax = ax_arr[i, i2]
            ax.plot(
                    df_conf[df_conf.sat_state == s].av_level.to_numpy(),
                    marker='o',
                    linestyle='',
                    color='r' if s == 'UNSATISFIABLE' else 'b',
                    label=s
                    )
            ax.set_xticklabels(df_conf[df_conf.sat_state == s].time.to_numpy())
            # ax.set_xticklabels(ax.get_xticklabels(),
                    # fontsize=6, rotation=43, ha="right")
            # ax.set_xlabel("")
            # ax.set_ylabel("")
            ax.set_title(conf[i].split('___')[-1]+ ', ' + s)
    fig.text(0.5, 0.04, "Time (s)", va='center', ha='center',)
    fig.text(0.04, 0.5, "Level (mean, std)", va='center', ha='center', rotation='vertical')
    fig.subplots_adjust(left=0.08, right=0.94, bottom=0.1, top=0.94, hspace=0.4)
    if savefig:
        fig.savefig('level_vs_time_sp3.png')
    plt.show()

def level_vs_time_diff(df, conf):
    # markers = ['x', 'o', '^', 'v']
    markers = [i for i in range(12)]
    # cm = sns.color_palette('tab20')
    cm = sns.color_palette('twilight', len(df.cnf.unique()))
    # num_plot = np.math.factorial(len(conf)) // (2 * np.math.factorial(len(conf)-2))
    num_plot = 4*4
    cols = 4
    cnfs = df.cnf.unique()

    fig, ax_arr = plt.subplots(num_plot//cols, cols, sharex=True)
    # ax_arr.flatten()
    for i, c in enumerate(conf):
        df_conf = df[df.config == c].reset_index()
        for i2, c2 in enumerate(conf):
            ax = ax_arr[i, i2]
            df_conf2 = df[df.config == c2].reset_index()
            df_conf[f"diff{i2}"] = df_conf2.time - df_conf.time
            g = sns.boxplot(x='sat_state', y=f"diff{i2}",
                    data=df_conf,
                    showmeans=True,
                    ax=ax
            )
            conf2 = c2.rstrip(')').rstrip('\'').split('___')[-1]
            conf1 = c.rstrip(')').rstrip('\'').split('___')[-1]
            ax.set_title(f"{conf2} - {conf1}")
            ax.set_xlabel("")
            ax.set_ylabel("")
            ax.set_xticklabels(ax.get_xticklabels(),
                    fontsize=9, rotation=20, ha="right")

    fig.subplots_adjust(left=0.08, right=0.94, bottom=0.1, top=0.94, hspace=0.2)
    plt.show()

def level_vs_time_boxplots(df, conf):
    cols = 2
    num_plot = 4
    fig, ax_arr = plt.subplots(num_plot//cols, cols, sharex=True)
    for i, c in enumerate(['time', 'av_level']):
        for i2, ss in enumerate(df.sat_state.unique()):
            ax = ax_arr[i2, i]
            df_conf = df[df.sat_state == ss].sort_values('config')
            g = sns.boxplot(x='config', y=c, data=df_conf,
                    showmeans=True,
                    ax=ax
            )

            ax.set_xticklabels(
                    [str(b).rstrip(')').rstrip('\'').split('___')[-1]
                        for b in ax.get_xticklabels()],
                    fontsize=15, rotation=20, ha="right")
            ax.set_xlabel("")
            ax.set_title(f"{c}, {ss}")
    fig.subplots_adjust(left=0.08, right=0.94, bottom=0.1, top=0.94, hspace=0.2)
    plt.show()

def level_vs_level(df, conf, logscale=False):
    markers = [i for i in range(12)]
    # cm = sns.color_palette('tab20')
    cm = sns.color_palette('twilight', len(df.cnf.unique()))
    # num_plot = np.math.factorial(len(conf)) // (2 * np.math.factorial(len(conf)-2))
    num_plot = 4*4
    cols = 4
    cnfs = df.cnf.unique()

    fig, ax_arr = plt.subplots(num_plot//cols, cols)
    ax_arr.flatten()
    for i, c in enumerate(conf):
        df_conf = df[df.config == c].reset_index()
        for i2, c2 in enumerate(conf):
            ax = ax_arr[i, i2]
            # ax = ax_arr[i*len(conf[i:])+i2)
            # print("next plot", i*len(conf[i:])+i2)

            df_conf2 = df[df.config == c2].reset_index()
            df_conf[f"diff{i2}"] = df_conf2.time - df_conf.time

            g = sns.scatterplot(x=df_conf.av_level, y=df_conf2.av_level,
                    hue=df_conf[f"diff{i2}"],
                    ax=ax
            )
            if logscale:
                g.set(xscale='log')
                g.set(yscale='log')
            conf2 = c2.rstrip(')').rstrip('\'').split('___')[-1]
            conf1 = c.rstrip(')').rstrip('\'').split('___')[-1]
            ax.set_title(f"{conf2} - {conf1}")
            ax.set_xlabel(conf1)
            ax.set_ylabel(conf2)
            # ax.set_xticklabels(ax.get_xticklabels(),
                    # fontsize=9, rotation=20, ha="right")

    fig.subplots_adjust(left=0.05, right=0.96, bottom=0.05, top=0.96,
            hspace=0.5, wspace=0.2)
    plt.show()

if __name__ == "__main__":
    # from parse_output import parse_exp_output, dict_to_dfs
    from parse_output2 import parse_exp_output, dict_to_df
    exp_outputs_dir = "exp_output"
    config_list = [
            "cadical-1.3.1-c9b8d0b67a123___sat_500",
            "cadical-1.3.1-c9b8d0b67a123___sat_950",
            "cadical-1.3.1-c9b8d0b67a123___unsat_500",
            "cadical-1.3.1-c9b8d0b67a123___unsat_950"
            ]
    res_dict = parse_exp_output(exp_outputs_dir, config_list)
    # dfs = dict_to_dfs(res_dict)
    # df = dict_to_df(res_dict)
    df = dict_to_df(res_dict, explode_level=False)

    # filter_outliers
    # outlier_threshold = 1000 #(level)
    # for i, df in enumerate(dfs):
        # df.level = df.level.astype(int)
        # dfs[i] = df.groupby('path').filter(lambda x: x['level'].mean() < outlier_threshold)

    # level_vs_time_subplots(dfs, config_list)

    # level_vs_time(df, config_list)
    # level_vs_time_sp2(df, config_list)
    # level_vs_time_diff(df, config_list)
    # level_vs_time_boxplots(df, config_list)


