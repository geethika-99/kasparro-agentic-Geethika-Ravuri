import re

class ParserAgent:
    def run(self, raw):
        product = dict(raw)

        name = product.get("name", "")
        product["id"] = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

        price_raw = product.get("price", "")
        digits = re.findall(r"\d+", price_raw)
        product["price_amount"] = int("".join(digits)) if digits else 0

        for k in ["ingredients", "benefits", "skin_type"]:
            if k in product and not isinstance(product[k], list):
                product[k] = [product[k]]

        return product