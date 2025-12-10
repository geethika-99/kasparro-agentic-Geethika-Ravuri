import uuid

class QuestionGeneratorAgent:

    def _id(self):
        return str(uuid.uuid4())

    def run(self, product):
        name = product["name"]
        qs = []
        seen = set()

        def add(cat, q, a):
            """Add a unique question (avoid duplicates)."""
            if q in seen:
                return
            seen.add(q)
            qs.append({
                "id": self._id(),
                "category": cat,
                "question": q,
                "answer": a
            })

        # ============================
        # 1. INFORMATIONAL - PRODUCT BASICS
        # ============================
        add("Informational",
            f"What is {name}?",
            f"{name} is a product with {product.get('concentration', 'active ingredients')}.")

        add("Informational",
            f"What is the concentration of {name}?",
            product.get("concentration", "Not specified"))

        add("Informational",
            f"What skin types is {name} suitable for?",
            ", ".join(product.get("skin_type", [])) or "Multiple skin types")

        # ============================
        # 2. INGREDIENTS & BENEFITS
        # ============================
        add("Informational",
            f"What are the key ingredients in {name}?",
            ", ".join(product.get("ingredients", [])) or "Multiple active ingredients")

        # Benefits → Auto Questions (each benefit gets a question)
        for b in product.get("benefits", []):
            add("Informational",
                f"How does {name} help with {b.lower()}?",
                f"{name} offers {b.lower()} benefits through its active ingredients.")

        # ============================
        # 3. USAGE QUESTIONS
        # ============================
        usage = product.get("usage", "Follow the usage instructions.")

        add("Usage",
            f"How do I use {name}?",
            usage)

        add("Usage",
            f"When should I apply {name}?",
            usage)

        add("Usage",
            f"How often should I use {name}?",
            usage or "As directed on the packaging")

        add("Usage",
            f"Can I use {name} daily?",
            "Yes, follow the recommended usage instructions.")

        # ============================
        # 4. SAFETY & SIDE EFFECTS
        # ============================
        side_effects = product.get("side_effects", "Generally well-tolerated")

        if product.get("side_effects"):
            add("Safety",
                "Are there any side effects?",
                side_effects)

            add("Safety",
                f"Is {name} suitable for sensitive skin?",
                f"Sensitive skin users should be aware: {side_effects}")

        add("Safety",
            f"Is {name} safe for daily use?",
            "Yes, when used as directed.")

        # ============================
        # 5. PURCHASE & PRICING
        # ============================
        add("Purchase",
            f"What is the price of {name}?",
            product.get("price", "Contact for pricing"))

        add("Purchase",
            f"Where can I buy {name}?",
            "Available through official retailers and online channels.")

        # ============================
        # 6. STORAGE & SHELF LIFE
        # ============================
        add("Informational",
            f"How should I store {name}?",
            "Store in a cool, dry place away from direct sunlight.")

        add("Informational",
            f"What is the shelf life of {name}?",
            "Follow the expiration date on the packaging.")

        # ============================
        # 7. COMPARISON & RECOMMENDATIONS
        # ============================
        add("Informational",
            f"Who would benefit most from {name}?",
            f"People with {', '.join(product.get('skin_type', []))} skin types seeking {', '.join(product.get('benefits', []))} benefits.")

        add("Informational",
            f"Can I combine {name} with other skincare products?",
            "Yes, but patch test first and avoid combining with conflicting actives.")

        # ============================
        # 8. ENSURE AT LEAST 20 QUESTIONS
        # ============================
        while len(qs) < 20:
            counter = len(qs)
            add("Informational",
                f"What makes {name} unique?",
                f"{name} combines {', '.join(product.get('ingredients', []))} for optimal results.")

        # Trim to exactly 20
        qs = qs[:20]

        return qs