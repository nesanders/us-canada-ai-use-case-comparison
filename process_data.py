import csv
import json
import os

def clean_agency(agency):
    if not agency: return "Unknown"
    mapping = {
        "Department of Health and Human Services": "HHS",
        "Department of Veterans Affairs": "VA",
        "Department of Energy": "DOE",
        "Department of Justice": "DOJ",
        "Department of the Interior": "DOI",
        "Department of Homeland Security": "DHS",
        "Department of Commerce": "DOC",
        "Department of Agriculture": "USDA",
        "Department of the Treasury": "TREAS",
        "Department of Transportation": "DOT",
        "Department of State": "STATE",
        "Department of Education": "ED",
        "Department of Labor": "DOL",
        "Department of Housing and Urban Development": "HUD",
        "General Services Administration": "GSA",
        "Social Security Administration": "SSA",
        "National Aeronautics and Space Administration": "NASA",
        "Environmental Protection Agency": "EPA",
        "Securities and Exchange Commission": "SEC",
        "Federal Deposit Insurance Corporation": "FDIC",
        "Tennessee Valley Authority": "TVA",
        "Board of Governors of the Federal Reserve System": "FRB",
        "Federal Reserve Board": "FRB",
        "United States Agency for International Development": "USAID",
        "Small Business Administration": "SBA",
        "Commodity Futures Trading Commission": "CFTC",
        "Federal Trade Commission": "FTC",
        "Nuclear Regulatory Commission": "NRC",
        "National Science Foundation": "NSF",
        "Federal Communications Commission": "FCC",
        "Federal Energy Regulatory Commission": "FERC",
        "Federal Housing Finance Agency": "FHFA",
        "Election Assistance Commission": "EAC",
        "Farm Credit Administration": "FCA",
        "National Archives and Records Administration": "NARA",
        "National Credit Union Administration": "NCUA",
        "National Endowment for the Arts": "NEA",
        "National Indian Gaming Commission": "NIGC",
        "National Transportation Safety Board": "NTSB",
        "Office of Special Counsel": "OSC",
        "Occupational Safety and Health Review Commission": "OSHRC",
        "Pension Benefit Guaranty Corporation": "PBGC",
        "Surface Transportation Board": "STB",
        "Canada / Service canadien d'appui aux tribunaux administratifs": "ATSSC",
        "Fisheries and Oceans Canada": "DFO",
        "Agriculture and Agri-Food Canada": "AAFC",
        "Employment and Social Development Canada": "ESDC",
        "Royal Canadian Mounted Police": "RCMP",
        "Canada Border Services Agency": "CBSA"
    }
    for full, short in mapping.items():
        if full in agency:
            return short
    return agency.split(" / ")[0]

def parse_year(date_str):
    """Extract 4-digit year from mixed date formats."""
    if not date_str:
        return "Unknown"
    s = date_str.strip()
    # ISO: '2025-09-08 00:00:00' or '2025-09-08'
    if len(s) >= 4 and s[:4].isdigit() and (len(s) == 4 or s[4] in ('-', '/')):
        return s[:4]
    # MM/DD/YYYY or M/D/YYYY
    parts = s.split('/')
    if len(parts) == 3 and parts[2][:4].isdigit():
        return parts[2][:4]
    # 'Jan-2024', 'Sep-2023'
    if '-' in s:
        tail = s.rsplit('-', 1)[-1]
        if tail[:4].isdigit():
            return tail[:4]
    return "Unknown"


def categorize_use_case(text, description):
    if description.strip() == "No description provided." and len(text.split()) < 4:
        return "Missing Disclosure Details"
    
    text = (text + " " + description).lower()
    if any(kw in text for kw in ["vision", "image", "facial recognition", "object detection", "camera", "photo", "satellite", "biometric"]):
        return "Computer Vision"
    elif any(kw in text for kw in ["generative", "llm", "large language model", "chatbot", "chatgpt", "content generation", "summarization", "generate", "copilot", "assistant"]):
        return "Generative AI"
    elif any(kw in text for kw in ["nlp", "natural language", "translation", "transcription", "speech", "text mining", "text analysis", "sentiment"]):
        return "Language Processing"
    elif any(kw in text for kw in ["predict", "forecast", "risk", "anomaly", "fraud", "analytics", "classification", "optimization", "regression", "machine learning", "analysis", "detection", "modeling", "cybersecurity", "security"]):
        return "Analytics & Security"
    elif any(kw in text for kw in ["robotics", "autonomous", "drone", "uav"]):
        return "Autonomous & Robotics"
    elif any(kw in text for kw in ["search", "extraction", "retrieval", "document", "knowledge management"]):
        return "Search & Information Retrieval"
    elif any(kw in text for kw in ["automated", "automation", "processing", "workflow"]):
        return "Process Automation"
    
    return "Other / General"

def process_us_2024(filepath):
    results = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append({
                "id": f"US24-{len(results)}",
                "name": row.get("Use Case Name", "Unnamed System"),
                "agency": clean_agency(row.get("Agency", "Unknown")),
                "full_agency": row.get("Agency", "Unknown"),
                "description": row.get("What is the intended purpose and expected benefits of the AI?", "No description provided."),
                "status": row.get("Stage of Development", "Unknown"),
                "impact": row.get("Is the AI use case rights-impacting, safety-impacting, both, or neither?", "Not Disclosed"),
                "country": "USA",
                "year": "2024",
                "initiation_year": parse_year(row.get("Date Initiated", "")),
                "policy": "M-24-10 / EO 13960",
                "category": categorize_use_case(row.get("Use Case Name", ""), row.get("Description", "No description provided."))
            })
    return results

def process_us_2025(filepath):
    results = []
    with open(filepath, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            agency_abbr = row.get("agency", "").strip()
            agency_full = row.get("agency_name", agency_abbr).strip()
            agency_normalized = clean_agency(agency_full) if agency_full else agency_abbr
            description = row.get("problem_solved", "").strip()
            if not description:
                description = row.get("benefits", "").strip()
            if not description:
                description = "No description provided."
            is_hi_raw = row.get("is_high_impact", "").strip()
            is_hi_lower = is_hi_raw.lower()
            if "presumed" in is_hi_lower:
                impact = "Presumed High-Impact"
            elif "not high" in is_hi_lower:
                impact = "Not High-Impact"
            elif "high" in is_hi_lower:
                impact = "High-Impact"
            else:
                impact = "Not Disclosed"
            results.append({
                "id": row.get("id", f"US25-{len(results)}").strip(),
                "name": row.get("use_case_name", "Unnamed System").strip(),
                "agency": agency_normalized,
                "full_agency": agency_full,
                "description": description,
                "status": row.get("development_stage", "Unknown").strip(),
                "impact": impact,
                "country": "USA",
                "year": "2025",
                "initiation_year": parse_year(row.get("operational_date", "")),
                "policy": "M-25-21",
                "category": categorize_use_case(row.get("use_case_name", ""), description)
            })
    return results

def process_ca_2025(filepath):
    results = []
    with open(filepath, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append({
                "id": row.get("ai_register_id", f"CA25-{len(results)}"),
                "name": row.get("name_ai_system_en", "Unnamed System"),
                "agency": clean_agency(row.get("government_organization", "Unknown")),
                "full_agency": row.get("government_organization", "Unknown"),
                "description": row.get("description_ai_system_en", "No description provided."),
                "status": row.get("ai_system_status_en", "Unknown"),
                "impact": "Not Categorized by Risk" if row.get("involves_personal_information") != "Y" else "Involves Personal Info",
                "country": "Canada",
                "year": "2025",
                "initiation_year": row.get("status_date", "Unknown"),
                "policy": "Treasury Board AI Register MVP",
                "category": categorize_use_case(row.get("name_ai_system_en", ""), row.get("description_ai_system_en", "") + " " + row.get("ai_system_capabilities_en", ""))
            })
    return results

def main():
    us_data = process_us_2024("us_inventory_published_2024_retrieved_2026-04-12.csv")
    us25_data = process_us_2025("us_inventory_published_2025_retrieved_2026-05-30.csv")
    ca_data = process_ca_2025("ca_inventory_published_2025_retrieved_2026-04-12.csv")

    combined = us_data + us25_data + ca_data

    # Generate stats for charts
    stats = {
        "usa_count": len(us_data),
        "us25_count": len(us25_data),
        "ca_count": len(ca_data),
        "usa_agencies": {},
        "us25_agencies": {},
        "ca_agencies": {},
        "timeline_usa": {},
        "timeline_us25": {},
        "timeline_ca": {},
        "categories_usa": {},
        "categories_us25": {},
        "categories_ca": {}
    }

    for item in us_data:
        stats["usa_agencies"][item["agency"]] = stats["usa_agencies"].get(item["agency"], 0) + 1
        stats["categories_usa"][item["category"]] = stats["categories_usa"].get(item["category"], 0) + 1
        yr = item["initiation_year"][:4] if item["initiation_year"] else "Unknown"
        if yr.isdigit() and 2000 <= int(yr) <= 2026:
            stats["timeline_usa"][yr] = stats["timeline_usa"].get(yr, 0) + 1

    for item in us25_data:
        stats["us25_agencies"][item["agency"]] = stats["us25_agencies"].get(item["agency"], 0) + 1
        stats["categories_us25"][item["category"]] = stats["categories_us25"].get(item["category"], 0) + 1
        yr = item["initiation_year"][:4] if item["initiation_year"] else "Unknown"
        if yr.isdigit() and 2000 <= int(yr) <= 2026:
            stats["timeline_us25"][yr] = stats["timeline_us25"].get(yr, 0) + 1

    for item in ca_data:
        stats["ca_agencies"][item["agency"]] = stats["ca_agencies"].get(item["agency"], 0) + 1
        stats["categories_ca"][item["category"]] = stats["categories_ca"].get(item["category"], 0) + 1
        yr = item["initiation_year"][:4] if item["initiation_year"] else "Unknown"
        if yr.isdigit() and 2000 <= int(yr) <= 2026:
            stats["timeline_ca"][yr] = stats["timeline_ca"].get(yr, 0) + 1

    # Sort agencies
    stats["usa_agencies"] = dict(sorted(stats["usa_agencies"].items(), key=lambda x: x[1], reverse=True))
    stats["us25_agencies"] = dict(sorted(stats["us25_agencies"].items(), key=lambda x: x[1], reverse=True))
    stats["ca_agencies"] = dict(sorted(stats["ca_agencies"].items(), key=lambda x: x[1], reverse=True))

    # Sort timelines
    stats["timeline_usa"] = dict(sorted(stats["timeline_usa"].items()))
    stats["timeline_us25"] = dict(sorted(stats["timeline_us25"].items()))
    stats["timeline_ca"] = dict(sorted(stats["timeline_ca"].items()))

    # Sort categories
    stats["categories_usa"] = dict(sorted(stats["categories_usa"].items(), key=lambda x: x[1], reverse=True))
    stats["categories_us25"] = dict(sorted(stats["categories_us25"].items(), key=lambda x: x[1], reverse=True))
    stats["categories_ca"] = dict(sorted(stats["categories_ca"].items(), key=lambda x: x[1], reverse=True))

    output = {
        "stats": stats,
        "items": combined
    }
    
    with open("ai_data.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Processed {len(combined)} total use cases ({len(us_data)} US 2024, {len(us25_data)} US 2025, {len(ca_data)} Canada).")

if __name__ == "__main__":
    main()
