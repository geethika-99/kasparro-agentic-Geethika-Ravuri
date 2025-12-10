class BlockExtractorAgent:
    def run(self, p):
        return {
            "title-block": {
                "content": f"{p['name']} — {p.get('concentration','')}"
            },
            "benefits-block": {
                "content": p.get("benefits", [])
            },
            "ingredients-block": {
                "content": p.get("ingredients", [])
            },
            "usage-block": {
                "content": p.get("usage", "")
            },
            "safety-block": {
                "content": p.get("side_effects", "No side effects listed")
            },
            "price-block": {
                "content": {
                    "amount": p.get("price_amount", 0),
                    "currency": "INR",
                    "display": p.get("price", "")
                }
            }
        }