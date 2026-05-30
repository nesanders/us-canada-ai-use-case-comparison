# US & Canada Federal AI Use Case Comparison

**Live Dashboard:** [https://nsanders.me/us-canada-ai-use-case-comparison/](https://nsanders.me/us-canada-ai-use-case-comparison/)  
**2025 Inventory Analysis:** [https://nsanders.me/us-canada-ai-use-case-comparison/analysis.html](https://nsanders.me/us-canada-ai-use-case-comparison/analysis.html)

This project provides an interactive, data-driven dashboard comparing the declared adoption of Artificial Intelligence across the federal governments of the United States and Canada. Built using vanilla HTML/JS and Chart.js, the dashboard covers 6,153 distinct federal AI use cases across three disclosure datasets and two administration frameworks.

## 📊 Data Sources & Policy Context

The data pipeline aggregates and unifies disparate public compliance registries:

1. **United States (2024 Inventory)**: 
   - **Source**: Office of Management and Budget (OMB) / Federal CIO Council.
   - **Context**: Reflects the exhaustive tracking mandate established via [Executive Order 13960](https://www.federalregister.gov/documents/2020/12/08/2020-27063/promoting-the-use-of-trustworthy-artificial-intelligence-in-the-federal-government) and the Biden administration's [OMB Memo M-24-10](https://www.whitehouse.gov/wp-content/uploads/2024/03/M-24-10-Advancing-Governance-Innovation-and-Risk-Management-for-Agency-Use-of-Artificial-Intelligence.pdf), focusing primarily on assessing systems that are "Rights-Impacting" or "Safety-Impacting".
2. **United States (2025 Inventory)**:
   - **Source**: OMB / Federal CIO Council via [GitHub](https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory).
   - **Context**: In April 2025, the Trump administration issued [OMB M-25-21](https://www.whitehouse.gov/wp-content/uploads/2025/02/M-25-21-Accelerating-Federal-Use-of-AI-through-Innovation-Governance-and-Public-Trust.pdf), drastically streamlining disclosure requirements to focus solely on highly consequential "High-Impact" systems to reduce bureaucratic friction. The consolidated 2025 inventory was published in April 2026, documenting **3,611 use cases across 56 agencies** — a nearly 70% increase in raw count over 2024, though direct comparison is complicated by the narrower risk focus and reduced reporting burden.
3. **Canada (2025 Register)**:
   - **Source**: Treasury Board of Canada Secretariat (Open Canada Portal).
   - **Context**: Launched in late 2025 under Prime Minister Mark Carney, this represents [Canada’s inaugural "MVP" AI Register](https://www.canada.ca/en/treasury-board-secretariat/news/2025/11/canada-launches-first-register-of-ai-uses-in-federal-government.html) aimed at tracking institutional experiments and scaled production tools systematically. While this Register acts as a broad catalogue, Canada manages high-risk deployments through a separate [Algorithmic Impact Assessment (AIA)](https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai/algorithmic-impact-assessment.html) process. The AIA mandates formal, public risk-scoring specifically for automated systems that make administrative decisions about citizens. The AI Register data is included here, not the AIA data.

## 🔍 2025 Inventory Analysis

The companion [`analysis.html`](https://nsanders.me/us-canada-ai-use-case-comparison/analysis.html) page presents a record-by-record review of all 3,611 disclosures in the 2025 U.S. inventory. Key findings include:

- **The High-Impact designation is being applied inconsistently.** DOT filed zero High-Impact records across 70 aviation and transportation safety systems. NASA filed one — a physical security camera — while classifying autonomous air traffic separation, Mars rover targeting AI, and a rocket facility gas system controller as Not High-Impact.
- **71.5% of correctly-classified High-Impact records are missing all required safeguard fields** (testing, impact assessment, independent review, monitoring, failsafe, and appeal process).
- **HHS deployed AI on Palantir infrastructure to scan position descriptions and grant applications for compliance with EOs 14151 and 14168.** Both systems are classified Not High-Impact. A companion HRSA system will evaluate funding opportunities against "dynamically-changing Executive Orders."
- **DOE's ACORN system autonomously executes control actions in a nuclear reactor context** and is classified Not High-Impact.
- **The State Department retired three geopolitical forecasting systems** — a global civilian-killing forecaster, a protest/riot predictor, and a political-influence network mapper — with blank descriptions and no retirement rationale.
- **704 records (19%) were filed without unique IDs**, preventing direct citation; this project assigns synthetic row-position IDs (US25-*n*) to make them addressable.

All record links in the analysis open in-page detail cards and include direct links to the exact source CSV row on GitHub.

## ⚙️ Repository Structure

* `index.html`: The interactive single-page dashboard featuring case filtering, grouped agency charts, and responsive visualizations via Chart.js.
* `analysis.html`: A record-by-record analysis of the 2025 U.S. inventory — findings on High-Impact classification failures, missing safeguard documentation, and notable individual disclosures.
* `process_data.py`: A Python script that parses raw government CSVs, normalizes agency names to consistent abbreviations across years, applies an NLP taxonomy to categorize use cases, and builds `ai_data.json`.
* `ai_data.json`: The compiled frontend JSON payload built by the data processor.
* `us_inventory_published_2024_retrieved_2026-04-12.csv`: Raw U.S. AI inventory under Biden/M-24-10 rules.
* `us_inventory_published_2025_retrieved_2026-05-30.csv`: Raw U.S. AI inventory under Trump/M-25-21 rules (3,611 records across 56 agencies).
* `ca_inventory_published_2025_retrieved_2026-04-12.csv`: Raw Canadian AI register data.

## 🚀 How to Run Locally

You do not need a server to run this. Simply open `index.html` in your web browser. 

If you wish to re-run the text categorization or build a new `.json` bundle with fresh CSV data, run:
```bash
python3 process_data.py
```

## Disclosure

This project was built with AI assistance from Google's Gemini and Anthropic's Claude Code.