# AI Career Copilot

A personalized skill-gap-to-roadmap product for engineering students and fresh graduates figuring out what to learn next — built end-to-end as a Consumer PM + AI PM portfolio project (strategy → PRD → prioritization → data analysis →  AI prototype → UX prototype).

---

## The problem

Engineering students and fresh graduates have unlimited access to career content — YouTube, Coursera, LinkedIn, ChatGPT — but no reliable way to prioritize it against their specific target role and current skill level. The result is decision paralysis, not a content shortage.

## The product

Upload a resume and pick a target role. AI Career Copilot parses the resume, classifies skills against that role's taxonomy (Have / Partial / Missing), and generates a personalized 12-week roadmap of weekly tasks — with progress tracking and an AI assistant grounded in that roadmap.

## Key decisions & results

- **Market gap:** every competitor gives more content (LinkedIn, Coursera, roadmap sites) or a human (career coaches) — nothing combines personalized AI gap analysis with a scalable action plan.
- **Simulated funnel (n=5,000):** 87% resume upload → 68% assessment → 47% roadmap → 26% first task → 9% D7 → 2% D30. Biggest drop-off is D7→D30, not signup.
- **Segment analysis:** final-year students retain ~10x better at D30 than working professionals despite converting slightly slower at the top of the funnel → reprioritized the initial target segment to 3rd/4th-year students.
- **A/B test (simulated, n=1,200/group):** cutting weekly tasks from 10 to 3 lifted first-task completion **+28.5%** and D7 retention **+52.2%** (both p<0.001) — shipped as the default.
- **Feature backlog** prioritized with RICE (not MoSCoW alone) because effort and confidence varied too much across features for a flat bucket ranking to be useful.

## What's in this repo

| Folder | Contents |
|---|---|
| `01-strategy/` | Problem statement, 3 user personas, Jobs-to-be-Done (`strategy_foundations.docx`) |
| `02-prd/` | Full PRD — vision, user stories, requirements, MVP scope, metrics, risks, launch plan (`prd.docx`) |
| `03-competitive-analysis/` | Competitive analysis + RICE/MoSCoW feature backlog, one workbook, two tabs (`competitive_analysis_backlog.xlsx`) |
| `04-analytics/` | Synthetic 5,000-user dataset (`synthetic_users.csv`), Excel funnel + segment analysis with live formulas (`user_analytics.xlsx`), Python retention charts, A/B test results |
| `05-ai-prototype/` | AI feature — real resume parsing, skill-gap classification, and roadmap generation via the Claude API (`copilot_prototype.html`) |
| `06-ux-prototype/` | 10-screen click-through UX prototype, landing page through upgrade flow (`screens_prototype.html`) |
| `figma/` | Figma design file link + screenshots (see below) |
| `portfolio_summary.docx` | One-page project summary |

## Data & analysis

- `synthetic_users.csv` — 5,000 simulated users with a realistic, segment-driven funnel (resume upload → assessment → roadmap → first task → D7 → D30), generated to demonstrate analysis methodology. **This is simulated data, not real users** — built to show the analysis approach ahead of having a live product.
- `user_analytics.xlsx` — funnel conversion and segment performance, computed with live Excel formulas (SUMIFS/COUNTIFS) so it recalculates if the raw data changes.
- Python/Pandas retention analysis — funnel drop-off, retention-by-segment, and "stickiness" (of users retained at D7, how many last to D30) charts.
- A/B test simulation — two-proportion z-test comparing a 10-task vs. 3-task weekly roadmap, with significance testing (scipy).

## Skills demonstrated

Problem framing · User research · PRD writing · Prioritization (RICE/MoSCoW) · Funnel & retention analysis · A/B testing · Excel modeling · Python/Pandas · AI product design · UX prototyping · Roadmapping

## About

Built solo as a portfolio project to demonstrate Consumer PM + AI PM range: from problem framing to a working AI feature.
