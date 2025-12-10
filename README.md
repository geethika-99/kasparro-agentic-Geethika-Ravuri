# Agents & Their Jobs
ParserAgent — "The Cleaner"
->Takes raw JSON and cleans it so every other agent receives perfect data.

# BlockExtractorAgent — "The Builder"
->Creates small content blocks that templates can reuse anywhere.

QuestionGeneratorAgent — "The Brain"
## Automatically generates 20 questions using rules:

->Benefits → Benefit questions

->Usage → Usage questions

->Price → Purchase questions
->Side effects → Safety questions

->Fillers → Ensure at least 20 Qs


#ComparatorAgent — "The Analyst"

->Compares two products and produces structured comparison notes.

# TemplateEngine — "The Architect"

Uses template JSONs to assemble the:
->product page
->FAQ page
->comparison page

#ValidatorAgent — "The Inspector"
Makes sure everything follows schema rules.

WriterAgent — "The Publisher"
->Saves the output JSON files and builds a manifest.



## Output Files
- outputs/product_page.json  
- outputs/faq.json  
- outputs/comparison_page.json  
- outputs/manifest.json  



## How to Run

pip install -r requirements.txt
python -m src.orchestrator --input data/input_product.json --product_b data/product_b.json --out outputs/