
yaml_deps = dct.yaml discoursegraphs_base.yaml prov.yaml schemaorg.yaml sioc.yaml rdf.yaml
dg_yaml = discoursegraphs.yaml
dg_ctxj = discoursegraphs.context.jsonld
mira_yaml = mira.yaml
mira_shacl = mira.shacl
mira_ctxj = mira.context.jsonld
svgfiles = discoursegraphs.svg mira.svg
linkml_ttl_files = linkml_mira.ttl linkml_discoursegraphs.ttl
generated_typescript = packages/mira-ts/src/index.ts
generated_python = src/mira/_generated.py
# dg_base.ttl is published by the discourse-graph project; fetch it for validation.
# To test an unpublished copy: make refresh_dg_base DG_BASE_URL=file:///path/to/dg_base.ttl
DG_BASE_URL ?= https://discoursegraphs.com/schema/dg_base.ttl
build_dir = .build
dg_base_ttl = $(build_dir)/dg_base.ttl
ontology_ttl = $(build_dir)/ontology.ttl

all: site/index.html $(svgfiles) $(linkml_ttl_files) $(mira_shacl)

generate: $(generated_python) $(generated_typescript)

validate_data: validate sampleData.json $(mira_shacl) $(ontology_ttl)
	uv run pyshacl -s mira.shacl -sf turtle -e $(ontology_ttl) sampleData.json

$(dg_base_ttl):
	mkdir -p $(build_dir)
	curl -sfL -o $@.tmp $(DG_BASE_URL) && mv $@.tmp $@

refresh_dg_base:
	rm -f $(dg_base_ttl)
	$(MAKE) $(dg_base_ttl)

# pyshacl takes a single ontology graph, so merge mira.ttl with dg_base.ttl.
$(ontology_ttl): mira.ttl $(dg_base_ttl)
	uv run python -c "import sys; from rdflib import Graph; g = Graph(); [g.parse(f) for f in sys.argv[2:]]; g.serialize(sys.argv[1], format='turtle')" $@ $^

$(generated_python): $(mira_yaml) $(yaml_deps)
	uv run gen-pydantic $(mira_yaml) > $@

$(generated_typescript): $(mira_yaml) $(yaml_deps)
	uv run gen-typescript --output $@ $(mira_yaml)

validate:
	uv run linkml validate $(mira_yaml)

clean:
	rm -rf $(svgfiles) $(linkml_ttl_files) *.puml *.context.jsonld docs site $(generated_typescript) $(generated_python) $(build_dir)

.PHONY: all generate validate validate_data clean refresh_dg_base

docs/index.md: $(mira_yaml) $(dg_yaml) $(yaml_deps) README.md elements.md
	mkdir -p docs/elements
	cp README.md docs/about.md
	cp elements.md docs/
	uv run gen-doc -d docs --no-hierarchical-class-view --render-imports --no-mergeimports --no-use-class-uris --no-use-slot-uris --diagram-type er_diagram mira.yaml --include-top-level-diagram --template-directory templates

site/index.html: docs/index.md mira.svg
	uv run mkdocs build -f mkdocs_mira.yaml
	cp mira.svg site/elements/
	sed -i~ 's/index.md//g' site/*.html site/*/*.html
	rm site/*~ site/*/*~

$(svgfiles):%.svg: %.puml
	curl -o $@ --data-binary @$< --location https://www.conversence.com/plantuml_deflate/svg

%.context.jsonld: %.yaml
	uv run gen-jsonld-context -o $@ $<

discoursegraphs.puml: $(dg_yaml) $(yaml_deps)
	uv run gen-plantuml $(dg_yaml) --no-mergeimports > $@

mira.puml: $(mira_yaml) $(dg_yaml) $(yaml_deps)
	uv run gen-plantuml $(mira_yaml) --no-mergeimports > $@

mira.shacl: $(mira_yaml) $(dg_yaml) $(yaml_deps)
	uv run gen-shacl $(mira_yaml) > $@

linkml_discoursegraphs.ttl: $(dg_ctxj)
	uv run gen-rdf -o $@ -f ttl --context $(dg_ctxj) $(dg_yaml)

linkml_mira.ttl: $(mira_ctxj)
	uv run gen-rdf -o $@ -f ttl --context $(mira_ctxj) $(mira_yaml)

$(mira_ctxj): $(dg_ctxj)
$(dg_ctxj): discoursegraphs_base.context.jsonld prov.context.jsonld schemaorg.context.jsonld rdf.context.jsonld
discoursegraphs_base.context.jsonld: sioc.context.jsonld
sioc.context.jsonld: dct.context.jsonld
