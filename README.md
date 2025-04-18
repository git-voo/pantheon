# Pantheon Congestion‑Control Evaluation

This repository contains everything needed to reproduce our Programming Assignment 3 experiments on TCP Congestion Control using the Pantheon framework and Mahimahi.

## Repository Structure

```
pantheon/                      ← Pantheon source tree (git submodule)
  data_profileA/               ← Raw logs & analysis for Profile A
  data_profileB/               ← Raw logs & analysis for Profile B
  src/                         ← Pantheon scripts (test.py, analyze.py, wrappers)
  50mbps.trace                 ← 60‑line bandwidth trace (50 Mbps)
  1mbps.trace                  ← 60‑line bandwidth trace (1 Mbps)
  generate_loss_plots.py         ← Custom script to plot per‑second loss rates
  generate_profile_comparison.py ← Script to plot throughput vs. RTT across profiles
  README.md                      ← This file
```

## Dependencies

- Ubuntu 18.04 (or similar Linux)
- Python 2.7 (for Pantheon & wrappers)
- Python 3.6+ (for custom plotting scripts)
- Mahimahi (`sudo apt install mahimahi`)
- Git (with submodule support)
- Python packages:
  ```bash
  sudo apt update
  sudo apt install python3-matplotlib python3-pyyaml
  ```

## Setup Pantheon & Schemes

1. **Clone repo & submodules**  
   ```bash
   git clone https://github.com/StanfordSNR/pantheon.git
   cd pantheon
   git submodule update --init --recursive
   ```

2. **Install global dependencies**  
   ```bash
   sudo ./tools/install_deps.sh
   ```

3. **Install per‑scheme dependencies & build**  
   ```bash
   # Only run once per VM:
   src/experiments/setup.py --setup --schemes "cubic bbr vegas"
   ```

## Emulated Test Profiles

We test **three schemes** (Cubic, BBR, Vegas) under **two profiles**:

| Profile | Bandwidth | One‑way Delay |
|:-------:|:---------:|:-------------:|
| **A**   | 50 Mbps   | 10 ms         |
| **B**   | 1 Mbps    | 200 ms        |

### Create Trace Files

```bash
# Profile A (50 Mbps)
for i in $(seq 1 60); do
  echo 50
done > 50mbps.trace

# Profile B (1 Mbps)
for i in $(seq 1 60); do
  echo 1
done > 1mbps.trace
```

## Running Experiments

From the repository root:

### Profile A

```bash
src/experiments/test.py local   --schemes "cubic bbr vegas"   --runtime 60   --uplink-trace 50mbps.trace   --downlink-trace 50mbps.trace   --prepend-mm-cmds "mm-delay 10"   --data-dir data_profileA
```

### Profile B

```bash
src/experiments/test.py local   --schemes "cubic bbr vegas"   --runtime 60   --uplink-trace 1mbps.trace   --downlink-trace 1mbps.trace   --prepend-mm-cmds "mm-delay 200"   --data-dir data_profileB
```

Each command produces:
- `*_datalink_run1.log`, `*_acklink_run1.log`  
- `*_datalink_throughput_run1.png`  
- `*_datalink_delay_run1.png`  
- `pantheon_perf.json`, `pantheon_metadata.json`  
- `pantheon_report.pdf`

## Analyzing Experiment Logs
from the root directory, ru the following

```bash
src/analysis/analyze.py --data-dir data_profileA
src/analysis/analyze.py --data-dir data_profileB
```

## Generating Loss‑Rate Plots

```bash
python3 generate_loss_plots.py data_profileA
python3 generate_loss_plots.py data_profileB
```

This will produce:
```
data_profileX/{cubic,bbr,vegas}_loss_run1.png
```

## Generating Profile Comparison Scatter

```bash
python3 generate_profile_comparison.py
```

This will output:
```
throughput_vs_rtt_profiles_annotated.png
```

## Final Report

The complete write‑up (with graph discussions and Part C answers) is in:

```
data_profileX/pantheon_report.pdf
```

Open it in any PDF viewer to review the experiment description, results, and analysis.

---