import json
import os
import hashlib

class WriterAgent:

    def write(self, obj, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)

    def write_manifest(self, outdir, files):
        manifest = []
        for f in files:
            content = open(f, "rb").read()
            manifest.append({
                "file": os.path.basename(f),
                "sha256": hashlib.sha256(content).hexdigest()
            })

        self.write({"manifest": manifest}, os.path.join(outdir, "manifest.json"))