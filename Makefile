
yaml_deps = dct.yaml discoursegraphs_base.yaml prov.yaml schemaorg.yaml sioc.yaml
dg_yaml = discoursegraphs.yaml
dg_ctxj = discoursegraphs.context.jsonld
mira_yaml = mira.yaml
mira_shacl = mira.yaml
mira_ctxj = mira.context.jsonld
svgfiles = discoursegraphs.svg mira.svg
linkml_ttl_files = linkml_mira.ttl linkml_discoursegraphs.ttl

all: site/index.html $(svgfiles) $(linkml_ttl_files) $(mira_shacl)

generate: generate-python generate-typescript mira.shacl

generate-python:
	uv run gen-pydantic $(mira_yaml) > src/mira/_generated.py

generate-typescript:
	uv run gen-typescript $(mira_yaml) > packages/mira-ts/src/index.ts

validate:
	uv run linkml validate $(mira_yaml)

clean:
	rm -rf $(svgfiles) $(linkml_ttl_files) *.puml *.context.jsonld docs site

docs/index.md: $(mira_yaml) $(dg_yaml) $(yaml_deps) README.md elements.md
	mkdir -p docs/elements
	cp README.md docs/about.md
	cp elements.md docs/
	uv run gen-doc -d docs --no-hierarchical-class-view --no-render-imports  --no-use-class-uris --no-use-slot-uris --diagram-type er_diagram mira.yaml --include-top-level-diagram

site/index.html: docs/index.md mira.svg
	uv run mkdocs build -f mkdocs_mira.yaml
	cp mira.svg site/elements/

$(svgfiles):%.svg: %.puml
	plantuml -f svg $<

%.context.jsonld: %.yaml
	uv run gen-jsonld-context $< > $@

discoursegraphs.puml: $(dg_yaml) $(yaml_deps)
	uv run gen-plantuml $(dg_yaml) --no-mergeimports > $@

mira.puml: $(mira_yaml) $(dg_yaml) $(yaml_deps)
	uv run gen-plantuml $(mira_yaml) --no-mergeimports > $@

mira.shacl: $(mira_yaml) $(dg_yaml) $(yaml_deps)
	uv run gen-shacl $(mira_yaml) > $@

linkml_discoursegraphs.ttl: $(dg_ctxj)
	uv run gen-rdf -f ttl --context $(dg_ctxj) $(dg_yaml) > $@

linkml_mira.ttl: $(mira_ctxj)
	uv run gen-rdf -f ttl --context $(mira_ctxj) $(mira_yaml) > $@

$(mira_ctxj): $(dg_ctxj)
$(dg_ctxj): discoursegraphs_base.context.jsonld prov.context.jsonld schemaorg.context.jsonld
discoursegraphs_base.context.jsonld: sioc.context.jsonld
sioc.context.jsonld: dct.context.jsonld
