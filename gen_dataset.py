import numpy as np
import pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(42)

N = 5000

# Segments roughly mirroring the 3 personas
segments = rng.choice(
    ["Final-year student", "Fresh graduate", "Working professional"],
    size=N, p=[0.45, 0.35, 0.20]
)

target_roles = rng.choice(
    ["Product Manager", "Software Engineer", "Data Analyst", "Marketing"],
    size=N, p=[0.55, 0.20, 0.15, 0.10]
)

# Signup dates over a 6-month acquisition window
start = datetime(2026, 1, 1)
signup_offsets = rng.integers(0, 180, size=N)
signup_dates = [start + timedelta(days=int(d)) for d in signup_offsets]

# Segment-driven base propensities (this is the strategic hypothesis we're testing:
# earlier-stage students engage more consistently than time-starved working professionals)
base_rates = {
    "Final-year student":     dict(resume=0.86, assess=0.78, roadmap=0.72, first_task=0.60, d7=0.42, d30=0.24),
    "Fresh graduate":         dict(resume=0.90, assess=0.83, roadmap=0.77, first_task=0.55, d7=0.34, d30=0.16),
    "Working professional":   dict(resume=0.80, assess=0.70, roadmap=0.62, first_task=0.42, d7=0.22, d30=0.09),
}

def sim_funnel(seg):
    r = base_rates[seg]
    resume = rng.random() < r["resume"]
    assess = resume and (rng.random() < r["assess"])
    roadmap = assess and (rng.random() < r["roadmap"])
    first_task = roadmap and (rng.random() < r["first_task"])
    d7 = first_task and (rng.random() < r["d7"])
    d30 = d7 and (rng.random() < r["d30"])
    return resume, assess, roadmap, first_task, d7, d30

rows = []
for i in range(N):
    seg = segments[i]
    resume, assess, roadmap, first_task, d7, d30 = sim_funnel(seg)
    rows.append({
        "user_id": f"U{i+1:05d}",
        "signup_date": signup_dates[i].strftime("%Y-%m-%d"),
        "segment": seg,
        "target_role": target_roles[i],
        "resume_uploaded": int(resume),
        "assessment_completed": int(assess),
        "roadmap_generated": int(roadmap),
        "first_task_completed": int(first_task),
        "d7_active": int(d7),
        "d30_active": int(d30),
    })

df = pd.DataFrame(rows)
df.to_csv("/home/synthetic_users.csv", index=False)
print(df.shape)
print(df.groupby("segment")[["resume_uploaded","assessment_completed","roadmap_generated","first_task_completed","d7_active","d30_active"]].mean().round(3))
