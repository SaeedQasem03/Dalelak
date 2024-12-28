import jsonlines
import stanza
import requests

stanza.download('ar')
nlp = stanza.Pipeline(lang='ar', processors='tokenize,ner')

def get_wikidata_links(entity):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "language": "ar",  
        "format": "json",
        "search": entity,
        "limit": 1 
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("search", [])
        if results:
            return {
                "label": results[0].get("label"),
                "description": results[0].get("description"),
                "wikidata_id": results[0].get("id")
            }
    return None

l = []
with jsonlines.open("extracted_text.jsonl") as reader:
    for obj in reader:
        if "contract" in obj:
            l.append(obj)

with open("output.txt", "w", encoding="utf-8") as output_file:
    for idx, i in enumerate(l, start=1):
        doc = nlp(i["contract"])
        
        output_file.write(f"Contract {idx} Named Entities:\n")
        for ent in doc.ents:
            output_file.write(f"{ent.text} [{ent.type}]\n")
            
            link = get_wikidata_links(ent.text)
            if link:
                output_file.write(f"  - Wikidata ID: {link['wikidata_id']}, Label: {link['label']}, Description: {link['description']}\n")
        
        output_file.write("\n")  

