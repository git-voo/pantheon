#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt

schemes = ['cubic', 'vegas', 'bbr']
colors  = {'cubic':'C0','vegas':'C1','bbr':'C2'}
markers = {'A':'o','B':'^'}

# load both profiles
with open('data_profileA/pantheon_perf.json') as f:
    perfA = json.load(f)
with open('data_profileB/pantheon_perf.json') as f:
    perfB = json.load(f)

fig, ax = plt.subplots()

for prof, perf in [('A', perfA), ('B', perfB)]:
    for scheme in schemes:
        stats = perf[scheme]['1']['all']
        rtt  = stats['delay']
        tput = stats['tput']
        # plot
        sc = ax.scatter(rtt, tput,
                        color=colors[scheme],
                        marker=markers[prof],
                        s=100,
                        label=f"{scheme.capitalize()} (Profile {prof})")
        # annotate directly next to the point
        ax.annotate(f"{scheme.capitalize()} P{prof}",
                    (rtt, tput),
                    textcoords="offset points",
                    xytext=(5,5),
                    fontsize=9)

ax.set_xlabel('95th‑percentile RTT (ms)')
ax.set_ylabel('Average Throughput (Mbit/s)')
ax.invert_xaxis()
ax.set_title('Throughput vs. RTT Across Profiles A & B')

# remove duplicate legend entries
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(
    list(by_label.values()),
    list(by_label.keys()),
    loc='lower left',
    bbox_to_anchor=(1, 0)
)


fig.tight_layout()
plt.savefig('throughput_vs_rtt_profiles_annotated.png')
