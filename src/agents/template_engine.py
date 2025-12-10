class TemplateEngine:

    def render(self, template, context):
        out = {}
        for field, rule in template["fields"].items():
            if "source" in rule:
                src = rule["source"]
                if src == "title-block":
                    out[field] = context["blocks"]["title-block"]["content"]
                else:
                    parts = src.split(".")
                    value = context
                    for p in parts:
                        value = value.get(p, {})
                    out[field] = value

            elif "depends_on" in rule:
                combined = []
                for dep in rule["depends_on"]:
                    content = context["blocks"][dep]["content"]
                    if isinstance(content, list):
                        combined += content
                    else:
                        combined.append(content)

                text = " ".join(combined)

                for r in rule.get("rules", []):
                    if r.startswith("limit_chars"):
                        n = int(r.split(":")[1])
                        if len(text) > n:
                            text = text[:n] + "..."
                out[field] = text

            elif "blocks" in rule:
                out[field] = [context["blocks"][b] for b in rule["blocks"]]

        return out