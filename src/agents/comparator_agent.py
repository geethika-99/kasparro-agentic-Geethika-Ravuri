class ComparatorAgent:
    def run(self, A, B):
        return {
            "productA": {
                "id": A["id"],
                "name": A["name"],
                "ingredients": A["ingredients"],
                "benefits": A["benefits"],
                "price": A["price_amount"]
            },
            "productB": {
                "id": B["id"],
                "name": B["name"],
                "ingredients": B["ingredients"],
                "benefits": B["benefits"],
                "price": B["price_amount"]
            },
            "comparisons": [
                {
                    "metric": "concentration",
                    "productA": A.get("concentration"),
                    "productB": B.get("concentration"),
                    "notes": "Higher concentration may be stronger."
                },
                {
                    "metric": "ingredients",
                    "productA": A["ingredients"],
                    "productB": B["ingredients"],
                    "notes": "Overlap indicates similar active profile."
                },
                {
                    "metric": "benefits",
                    "productA": A["benefits"],
                    "productB": B["benefits"],
                    "notes": "Choose based on your need."
                },
                {
                    "metric": "price",
                    "productA": A["price_amount"],
                    "productB": B["price_amount"],
                    "notes": f"Difference: {B['price_amount'] - A['price_amount']}"
                }
            ]
        }