import csv
import json
import os

def clean_agency(agency):
    if not agency: return "Unknown"
    # Simplify common agency names for charting
    mapping = {
        "Department of Homeland Security": "DHS",
        "Department of Justice": "DOJ",
        "Department of State": "State",
        "Department of Veterans Affairs": "VA",
        "Department of Commerce": "Commerce",
        "Department of Education": "Education",
        "Department of Energy": "Energy",
        "Department of Health and Human Services": "HHS",
        "Department of the Treasury": "Treasury",
        "General Services Administration": "GSA",
        "National Aeronautics and Space Administration": "NASA",
        "Environmental Protection Agency": "EPA",
        "Social Security Administration": "SSA",
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
    return agency.split(" / ")[0] # For Canadian bilingual names

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
                "description": row.get("Description", "No description provided."),
                "status": row.get("Stage of Development", "Unknown"),
                "impact": row.get("Is the AI use case rights-impacting, safety-impacting, both, or neither?", "Not Disclosed"),
                "country": "USA",
                "year": "2024",
                "initiation_year": row.get("Date Initiated", "").split("/")[-1] if "/" in row.get("Date Initiated", "") else row.get("Date Initiated", "Unknown"),
                "policy": "M-24-10 / EO 13960",
                "category": categorize_use_case(row.get("Use Case Name", ""), row.get("Description", "No description provided."))
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
    ca_data = process_ca_2025("ca_inventory_published_2025_retrieved_2026-04-12.csv")
    
    combined = us_data + ca_data
    
    # Generate stats for charts
    stats = {
        "usa_count": len(us_data),
        "ca_count": len(ca_data),
        "usa_agencies": {},
        "ca_agencies": {},
        "timeline_usa": {},
        "timeline_ca": {},
        "categories_usa": {},
        "categories_ca": {}
    }
    
    for item in us_data:
        stats["usa_agencies"][item["agency"]] = stats["usa_agencies"].get(item["agency"], 0) + 1
        stats["categories_usa"][item["category"]] = stats["categories_usa"].get(item["category"], 0) + 1
        yr = item["initiation_year"][:4] if item["initiation_year"] else "Unknown"
        if yr.isdigit() and 2000 <= int(yr) <= 2025:
            stats["timeline_usa"][yr] = stats["timeline_usa"].get(yr, 0) + 1

    for item in ca_data:
        stats["ca_agencies"][item["agency"]] = stats["ca_agencies"].get(item["agency"], 0) + 1
        stats["categories_ca"][item["category"]] = stats["categories_ca"].get(item["category"], 0) + 1
        yr = item["initiation_year"][:4] if item["initiation_year"] else "Unknown"
        if yr.isdigit() and 2000 <= int(yr) <= 2025:
            stats["timeline_ca"][yr] = stats["timeline_ca"].get(yr, 0) + 1

    # Sort agencies
    stats["usa_agencies"] = dict(sorted(stats["usa_agencies"].items(), key=lambda x: x[1], reverse=True))
    stats["ca_agencies"] = dict(sorted(stats["ca_agencies"].items(), key=lambda x: x[1], reverse=True))
    
    # Sort timelines
    stats["timeline_usa"] = dict(sorted(stats["timeline_usa"].items()))
    stats["timeline_ca"] = dict(sorted(stats["timeline_ca"].items()))

    # Sort categories
    stats["categories_usa"] = dict(sorted(stats["categories_usa"].items(), key=lambda x: x[1], reverse=True))
    stats["categories_ca"] = dict(sorted(stats["categories_ca"].items(), key=lambda x: x[1], reverse=True))

    output = {
        "stats": stats,
        "items": combined
    }
    
    with open("ai_data.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Processed {len(combined)} total use cases.")

if __name__ == "__main__":
    main()
