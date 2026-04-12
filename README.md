# US & Canada Federal AI Use Case Comparison

**Live Dashboard:** [https://nsanders.me/us-canada-ai-use-case-comparison/](https://nsanders.me/us-canada-ai-use-case-comparison/)

This project provides an interactive, data-driven dashboard comparing the declared adoption of Artificial Intelligence across the federal governments of the United States and Canada. Built using Vanilla HTML/JS and Chart.js, the dashboard analyzes over 2,500 distinct federal AI use cases spanning multiple administration frameworks.

## 📊 Data Sources & Policy Context

The data pipeline aggregates and unifies disparate public compliance registries:

1. **United States (2024 Inventory)**: 
   - **Source**: Office of Management and Budget (OMB) / Federal CIO Council.
   - **Context**: Reflects the exhaustive tracking mandate established via [Executive Order 13960](https://www.federalregister.gov/documents/2020/12/08/2020-27063/promoting-the-use-of-trustworthy-artificial-intelligence-in-the-federal-government) and the Biden administration's [OMB Memo M-24-10](https://www.whitehouse.gov/wp-content/uploads/2024/03/M-24-10-Advancing-Governance-Innovation-and-Risk-Management-for-Agency-Use-of-Artificial-Intelligence.pdf), focusing primarily on assessing systems that are "Rights-Impacting" or "Safety-Impacting".
2. **United States (2025 Transition Status)**:
   - **Context**: In April 2025, the Trump administration issued [OMB M-25-21](https://www.whitehouse.gov/wp-content/uploads/2025/02/M-25-21-Accelerating-Federal-Use-of-AI-through-Innovation-Governance-and-Public-Trust.pdf), drastically streamlining disclosure requirements to focus solely on highly consequential "High-Impact" systems to reduce bureaucratic friction. *As of early 2026, a public consolidated 2025 dataset reflecting these new rules remains unpublished.*
3. **Canada (2025 Register)**:
   - **Source**: Treasury Board of Canada Secretariat (Open Canada Portal).
   - **Context**: Launched in late 2025 under Prime Minister Mark Carney, this represents [Canada’s inaugural "MVP" AI Register](https://www.canada.ca/en/treasury-board-secretariat/news/2025/11/canada-launches-first-register-of-ai-uses-in-federal-government.html) aimed at tracking institutional experiments and scaled production tools systematically.

## ⚙️ Repository Structure

* `index.html`: The interactive single-page dashboard featuring infinite-scroll analytics, case filtering, and responsive visualizations via Chart.js.
* `process_data.py`: A Python automation script that parses raw government CSVs, applies a Natural Language Processing (NLP) taxonomy to identify common application capabilities (e.g., Computer Vision, Generative AI), and structures the data for the web UI.
* `ai_data.json`: The compiled frontend JSON payload built by the data processor.
* `us_inventory_published_2024_retrieved_2026-04-12.csv`: The raw source data for U.S. departments.
* `ca_inventory_published_2025_retrieved_2026-04-12.csv`: The raw source data for Canadian institutions.

## 🚀 How to Run Locally

You do not need a server to run this. Simply open `index.html` in your web browser. 

If you wish to re-run the text categorization or build a new `.json` bundle with fresh CSV data, run:
```bash
python3 process_data.py
```
