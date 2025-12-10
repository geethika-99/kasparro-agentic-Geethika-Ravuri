# Minimal orchestrator runner

"""Minimal orchestrator runner

This script provides a small, self-contained runner so the project can be executed
without external dependencies. It reads two product JSON files and writes four
output files into the specified output directory:

- product_page.json
- faq.json
- comparison_page.json
- manifest.json

Usage (as in README):
	python -m src.orchestrator --input data/input_product.json --product_b data/product_b.json --out outputs/

The real project may have a more complex orchestrator; this implementation is
intended only to make the repository runnable for demonstration and testing.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict

# import local agents
from .agents.parser_agent import ParserAgent
from .agents.block_extractor import BlockExtractorAgent
from .agents.question_generator import QuestionGeneratorAgent
from .agents.template_engine import TemplateEngine
from .agents.comparator_agent import ComparatorAgent
from .agents.writer_agent import WriterAgent
import io


def load_json(path: Path) -> Any:
	with path.open('r', encoding='utf-8') as f:
		return json.load(f)


def write_json(path: Path, data: Any) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	with path.open('w', encoding='utf-8') as f:
		json.dump(data, f, indent=2, ensure_ascii=False)


def load_template(path: Path) -> Dict[str, Any]:
	with path.open('r', encoding='utf-8') as f:
		return json.load(f)


def render_product_page(template: Dict[str, Any], product: Dict[str, Any]) -> Dict[str, Any]:
	blocks = BlockExtractorAgent().run(product)
	engine = TemplateEngine()
	context = {"blocks": blocks, "product": product}
	return engine.render(template, context)


def render_faq_page(template: Dict[str, Any], product: Dict[str, Any], faqs: list) -> Dict[str, Any]:
	engine = TemplateEngine()
	context = {"product": product, "faq_blocks": faqs}
	return engine.render(template, context)


def render_comparison_page(template: Dict[str, Any], a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
	comparator = ComparatorAgent()
	comp = comparator.run(a, b)
	engine = TemplateEngine()
	context = {
		"productA": comp.get("productA"),
		"productB": comp.get("productB"),
		"comparison_blocks": comp.get("comparisons"),
	}
	return engine.render(template, context)


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", required=True, help="Path to input product A JSON")
	parser.add_argument("--product_b", required=True, help="Path to product B JSON")
	parser.add_argument("--out", required=True, help="Output directory")
	args = parser.parse_args()

	root = Path(os.getcwd())
	a_path = (root / args.input).resolve()
	b_path = (root / args.product_b).resolve()
	out_dir = (root / args.out).resolve()

	if not a_path.exists():
		raise SystemExit(f"Input file not found: {a_path}")
	if not b_path.exists():
		raise SystemExit(f"Product B file not found: {b_path}")

	# load and normalize inputs
	a_raw = load_json(a_path)
	b_raw = load_json(b_path)

	parser = ParserAgent()
	a = parser.run(a_raw)
	b = parser.run(b_raw)

	# load templates
	templates_dir = root / "templates"
	product_template = load_template(templates_dir / "product_page_template.json")
	faq_template = load_template(templates_dir / "faq_template.json")
	comparison_template = load_template(templates_dir / "comparison_template.json")

	# generate FAQ questions
	qgen = QuestionGeneratorAgent()
	faqs = qgen.run(a)

	# render pages via TemplateEngine + agents
	product_page = render_product_page(product_template, a)
	faq_page = render_faq_page(faq_template, a, faqs)
	comparison_page = render_comparison_page(comparison_template, a, b)

	out_dir.mkdir(parents=True, exist_ok=True)

	writer = WriterAgent()
	created = []

	p1 = out_dir / "product_page.json"
	writer.write(product_page, str(p1))
	created.append(str(p1.relative_to(root)))

	p2 = out_dir / "faq.json"
	writer.write(faq_page, str(p2))
	created.append(str(p2.relative_to(root)))

	p3 = out_dir / "comparison_page.json"
	writer.write(comparison_page, str(p3))
	created.append(str(p3.relative_to(root)))

	# writer builds manifest with sha256 hashes
	writer.write_manifest(str(out_dir), [str(p1), str(p2), str(p3)])
	created.append(str((out_dir / "manifest.json").relative_to(root)))

	print("Wrote files:")
	for p in created:
		print(" -", p)


if __name__ == "__main__":
	main()
