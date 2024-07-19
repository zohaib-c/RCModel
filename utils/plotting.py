import matplotlib.pyplot as plt

def plot_results(all_cineca_dfs, all_sim_dfs):
    plt.rcParams.update({'font.size': 36})

    fig, axs = plt.subplots(6, 1, figsize=(20, 26), sharex=True)
    fig.subplots_adjust(hspace=0.5)

    for i, (cineca_df, sim_df) in enumerate(zip(all_cineca_dfs, all_sim_dfs)):
        ax = axs[i]
        ax.set_ylim([30, 140])

        sim_df['elapsed_days'] = sim_df['timestamp'] / 1000 / 60 / 60 / 24

        ax.set_ylabel('Temp (°C)')
        ax.plot(sim_df['elapsed_days'], cineca_df.total_cpu_temp.rolling(50).mean(), color='tab:blue', label='Cineca')
        ax.plot(sim_df['elapsed_days'], sim_df.temperature_C.rolling(50).mean(), color='tab:red', label='RC Model')

        ax.text(0.95, 0.16, f'Node {i}', transform=ax.transAxes, fontsize=30,
                verticalalignment='top', horizontalalignment='center', bbox=dict(facecolor='white', alpha=0.5))

        ax.grid(True)

    axs[-1].set_xlabel('Elapsed Time (days)')

    handles = [axs[0].lines[0], axs[1].lines[1]]
    labels = ["Cineca", "RC Model"]

    fig.legend(handles, labels, loc='upper center', ncol=2)
    plt.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))

    plt.savefig('Output/Simulation vs Cineca.png')

    plt.show()


def plot_power_error(all_cineca_dfs, all_sim_dfs):
    plt.rcParams.update({'font.size': 36})

    fig, axs = plt.subplots(2, 3, figsize=(30, 18))
    fig.subplots_adjust(hspace=0.3, wspace=0.3)

    for i, (cineca_df, sim_df) in enumerate(zip(all_cineca_dfs, all_sim_dfs)):
        ax = axs[i // 3, i % 3]
        ax.set_ylim([0, 7000])
        ax.set_xlim([-100, 100])
        error = cineca_df.total_cpu_power - sim_df.power_draw
        ax.hist(error, bins=100, alpha=0.5, label='Power Error')
        ax.set_xlabel('Power Error (W)')
        ax.set_ylabel('Frequency')
        ax.text(0.88, 0.95, f'Node {i}', transform=ax.transAxes, fontsize=30,
                verticalalignment='top', horizontalalignment='center', bbox=dict(facecolor='white', alpha=0.5))
        ax.yaxis.set_major_locator(plt.MaxNLocator(5))

    plt.tight_layout()

    plt.savefig('Output/Power Difference.png')
    plt.show()


def plot_error_histograms(all_cineca_dfs, all_sim_dfs):
    plt.rcParams.update({'font.size': 36})

    fig, axs = plt.subplots(2, 3, figsize=(30, 18))
    fig.subplots_adjust(hspace=0.3, wspace=0.3)

    for i, (cineca_df, sim_df) in enumerate(zip(all_cineca_dfs, all_sim_dfs)):
        ax = axs[i // 3, i % 3]
        ax.set_ylim([0, 4000])
        error = cineca_df.total_cpu_temp - sim_df.temperature_C
        ax.hist(error, bins=100, alpha=0.5, label='Temperature Error')
        ax.set_xlabel('Temperature Error (°C)')
        ax.set_ylabel('Frequency')
        ax.text(0.88, 0.95, f'Node {i}', transform=ax.transAxes, fontsize=30,
                verticalalignment='top', horizontalalignment='center', bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout()

    plt.savefig('Output/Error Histograms.png')
    plt.show()
