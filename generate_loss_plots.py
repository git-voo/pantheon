#!/usr/bin/env python3
"""
generate_loss_plots.py

Generate per-second loss‑rate plots for each congestion control scheme by
counting data-packet departures against ACK departures.

Usage:
    python3 generate_loss_plots.py <data_profile_dir>
"""

import os
import sys
import matplotlib.pyplot as plt

def plot_loss(profile_dir):
    # find schemes by looking for *_datalink_run1.log
    files = os.listdir(profile_dir)
    schemes = sorted({f.split('_')[0] for f in files if f.endswith('_datalink_run1.log')})

    for scheme in schemes:
        datalink = os.path.join(profile_dir, f'{scheme}_datalink_run1.log')
        acklink  = os.path.join(profile_dir, f'{scheme}_acklink_run1.log')

        if not (os.path.isfile(datalink) and os.path.isfile(acklink)):
            print(f"Skipping {scheme}: missing datalink or acklink logs")
            continue

        sent_counts = {}
        ack_counts = {}

        # Count data-packet departures per second
        with open(datalink) as f:
            for line in f:
                parts = line.strip().split()
                if not parts: continue
                try:
                    t_ms = float(parts[0])
                except ValueError:
                    continue
                t_s = t_ms/1000
                sec = int(t_s)
                sent_counts[sec] = sent_counts.get(sec, 0) + 1

        # Count ACK departures per second
        with open(acklink) as f:
            for line in f:
                parts = line.strip().split()
                if not parts: continue
                try:
                    t_ms = float(parts[0])
                except ValueError:
                    continue
                t_s = t_ms/1000
                sec = int(t_s)
                ack_counts[sec] = ack_counts.get(sec, 0) + 1

        # Build timeline
        times = sorted(set(sent_counts) | set(ack_counts))
        loss_rates = []
        for sec in times:
            sent = sent_counts.get(sec, 0)
            acks = ack_counts.get(sec, 0)
            loss = (sent - acks) / sent * 100 if sent > 0 else 0.0
            loss_rates.append(loss)

        # Plot
        plt.figure()
        plt.plot(times, loss_rates, marker='o', linestyle='-')
        plt.xlabel('Time (s)')
        plt.ylabel('Loss Rate (%)')
        plt.title(f'{scheme.capitalize()} Loss Rate over Time\n({os.path.basename(profile_dir)})')
        plt.grid(True)

        out = os.path.join(profile_dir, f'{scheme}_loss_run1.png')
        plt.savefig(out)
        plt.close()
        print(f"Written {out}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 generate_loss_plots.py <data_profile_dir>")
        sys.exit(1)
    plot_loss(sys.argv[1])
