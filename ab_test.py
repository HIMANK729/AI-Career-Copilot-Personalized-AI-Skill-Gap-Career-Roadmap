import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

rng = np.random.default_rng(7)

NAVY = "#1F3864"
ACCENT = "#2E74B5"
ORANGE = "#C55A11"

N_PER_GROUP = 1200

# Hypothesis: showing 3 prioritized tasks instead of 10 raises first-task completion
# (less overwhelm) and that higher completion drags D7 retention up with it.
p_first_task_control = 0.255   # matches overall funnel rate we already simulated
p_first_task_variant = 0.255 * 1.35  # hypothesized +35% relative lift from reduced overwhelm

# D7 retention conditional on completing the first task (variant users who do engage are similarly sticky)
p_d7_given_task_control = 0.35
p_d7_given_task_variant = 0.37  # small additional lift: fewer, clearer next steps also help week-1 return

def simulate_group(n, p_task, p_d7_given_task):
    first_task = rng.random(n) < p_task
    d7 = np.where(first_task, rng.random(n) < p_d7_given_task, False)
    return first_task, d7

control_task, control_d7 = simulate_group(N_PER_GROUP, p_first_task_control, p_d7_given_task_control)
variant_task, variant_d7 = simulate_group(N_PER_GROUP, p_first_task_variant, p_d7_given_task_variant)

def summarize(name, task, d7, n):
    return {
        "Group": name,
        "N": n,
        "First-Task Completions": int(task.sum()),
        "First-Task Completion Rate": task.mean(),
        "D7 Actives": int(d7.sum()),
        "D7 Retention Rate": d7.mean(),
    }

results = pd.DataFrame([
    summarize("Control (10 tasks/week)", control_task, control_d7, N_PER_GROUP),
    summarize("Variant (3 tasks/week)", variant_task, variant_d7, N_PER_GROUP),
])
print(results.to_string(index=False))

# Two-proportion z-test on primary metric: first-task completion
count = np.array([control_task.sum(), variant_task.sum()])
nobs = np.array([N_PER_GROUP, N_PER_GROUP])
p_pool = count.sum() / nobs.sum()
se = np.sqrt(p_pool * (1 - p_pool) * (1/nobs[0] + 1/nobs[1]))
z = (count[1]/nobs[1] - count[0]/nobs[0]) / se
p_value_primary = 2 * (1 - stats.norm.cdf(abs(z)))

# Secondary metric: D7 retention
count_d7 = np.array([control_d7.sum(), variant_d7.sum()])
p_pool_d7 = count_d7.sum() / nobs.sum()
se_d7 = np.sqrt(p_pool_d7 * (1 - p_pool_d7) * (1/nobs[0] + 1/nobs[1]))
z_d7 = (count_d7[1]/nobs[1] - count_d7[0]/nobs[0]) / se_d7
p_value_secondary = 2 * (1 - stats.norm.cdf(abs(z_d7)))

rel_lift_primary = (variant_task.mean() - control_task.mean()) / control_task.mean() * 100
rel_lift_secondary = (variant_d7.mean() - control_d7.mean()) / control_d7.mean() * 100

print(f"\nPrimary metric (first-task completion): z={z:.2f}, p-value={p_value_primary:.4f}, relative lift={rel_lift_primary:.1f}%")
print(f"Secondary metric (D7 retention): z={z_d7:.2f}, p-value={p_value_secondary:.4f}, relative lift={rel_lift_secondary:.1f}%")

# Chart
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
metrics = [("First-Task Completion Rate", control_task.mean(), variant_task.mean(), p_value_primary),
           ("D7 Retention Rate", control_d7.mean(), variant_d7.mean(), p_value_secondary)]
for ax, (title, c_val, v_val, pval) in zip(axes, metrics):
    bars = ax.bar(["Control\n(10 tasks)", "Variant\n(3 tasks)"], [c_val*100, v_val*100], color=[ACCENT, ORANGE])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_title(f"{title}\n(p={pval:.4f})", fontsize=11, color=NAVY, fontweight="bold")
    for b, val in zip(bars, [c_val, v_val]):
        ax.text(b.get_x()+b.get_width()/2, val*100+0.5, f"{val*100:.1f}%", ha="center", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
plt.suptitle("A/B Test: Reducing Weekly Tasks from 10 to 3", fontsize=13, color=NAVY, fontweight="bold")
plt.tight_layout()
plt.savefig("/home/chart_ab_test.png", dpi=150)
plt.close()
