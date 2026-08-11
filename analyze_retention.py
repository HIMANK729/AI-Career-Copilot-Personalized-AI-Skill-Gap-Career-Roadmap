import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.rcParams["font.family"] = "DejaVu Sans"

df = pd.read_csv("/home/claude/synthetic_users.csv")

NAVY = "#1F3864"
ACCENT = "#2E74B5"
PALETTE = ["#2E74B5", "#70AD47", "#C55A11"]

# ---- 1. Retention by segment (D7 vs D30) ----
seg_order = ["Final-year student", "Fresh graduate", "Working professional"]
ret = df.groupby("segment")[["d7_active", "d30_active"]].mean().reindex(seg_order) * 100

fig, ax = plt.subplots(figsize=(8, 5))
x = range(len(seg_order))
width = 0.35
ax.bar([i - width/2 for i in x], ret["d7_active"], width, label="D7 Retention", color=ACCENT)
ax.bar([i + width/2 for i in x], ret["d30_active"], width, label="D30 Retention", color="#C55A11")
ax.set_xticks(list(x))
ax.set_xticklabels(seg_order)
ax.set_ylabel("Retention Rate")
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_title("D7 / D30 Retention by User Segment (simulated)", fontsize=13, color=NAVY, fontweight="bold")
ax.legend()
for i, seg in enumerate(seg_order):
    ax.text(i - width/2, ret["d7_active"][seg] + 0.3, f"{ret['d7_active'][seg]:.1f}%", ha="center", fontsize=9)
    ax.text(i + width/2, ret["d30_active"][seg] + 0.3, f"{ret['d30_active'][seg]:.1f}%", ha="center", fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("/home/claude/chart_retention_by_segment.png", dpi=150)
plt.close()

# ---- 2. D30/D7 "stickiness" ratio by segment (retention of retention) ----
ret["d30_of_d7"] = (ret["d30_active"] / ret["d7_active"]) * 100
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(seg_order, ret["d30_of_d7"], color=PALETTE)
ax.set_ylabel("% of D7-active users still active at D30")
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_title("Stickiness: Of Users Retained at D7, Who Stays to D30?", fontsize=12, color=NAVY, fontweight="bold")
for b, seg in zip(bars, seg_order):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.5, f"{ret['d30_of_d7'][seg]:.1f}%", ha="center", fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("/home/claude/chart_stickiness_by_segment.png", dpi=150)
plt.close()

# ---- 3. Full funnel drop-off ----
stages = ["Signups", "Resume\nUploaded", "Assessment\nCompleted", "Roadmap\nGenerated", "First Task\nCompleted", "D7\nActive", "D30\nActive"]
cols = [None, "resume_uploaded", "assessment_completed", "roadmap_generated", "first_task_completed", "d7_active", "d30_active"]
counts = [len(df)] + [df[c].sum() for c in cols[1:]]
pct = [c / counts[0] * 100 for c in counts]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(stages, pct, color=ACCENT)
ax.set_ylabel("% of Total Signups")
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_title("Overall Funnel Conversion (simulated, N=5,000)", fontsize=13, color=NAVY, fontweight="bold")
for b, p, c in zip(bars, pct, counts):
    ax.text(b.get_x() + b.get_width()/2, p + 1.5, f"{p:.1f}%\n(n={c})", ha="center", fontsize=8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("/home/claude/chart_funnel.png", dpi=150)
plt.close()

print(ret.round(3))
print()
print("Funnel %:", [round(p, 1) for p in pct])
