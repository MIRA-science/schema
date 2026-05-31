
yaml_deps = src/dc/dc.yaml src/discoursegraphs/discoursegraphs_base.yaml src/prov/prov.yaml src/schemaorg/schemaorg.yaml src/sioc/sioc.yaml
dg_yaml = src/discoursegraphs/discoursegraphs.yaml
dg_ctxj = src/discoursegraphs/discoursegraphs.context.jsonld
mira_yaml = src/mira/mira.yaml
mira_ctxj = src/mira/mira.context.jsonld
svgfiles = discoursegraphs.svg mira.svg
linkml_ttl_files = linkml_mira.ttl linkml_discoursegraphs.ttl

all: site/index.html $(svgfiles) $(linkml_ttl_files)

validate:
	linkml validate $(mira_yaml)

clean:
	rm -rf $(svgfiles) $(linkml_ttl_files) *.puml src/*/*.jsonld docs site

docs/index.md: $(mira_yaml) $(dg_yaml) $(yaml_deps)
	gen-doc -d docs --no-hierarchical-class-view --no-render-imports  --no-use-class-uris --no-use-slot-uris --diagram-type er_diagram src/mira/mira.yaml --include-top-level-diagram

site/index.html: docs/index.md
	mkdocs build -f mkdocs_mira.yaml

$(svgfiles):%.svg: %.puml
	plantuml -f svg $<

%.context.jsonld: %.yaml
	gen-jsonld-context $< > $@

discoursegraphs.puml: $(dg_yaml) $(yaml_deps)
	gen-plantuml $(dg_yaml) --no-mergeimports > $@

mira.puml: $(mira_yaml) $(dg_yaml) $(yaml_deps)
	gen-plantuml $(mira_yaml) --no-mergeimports > $@

linkml_discoursegraphs.ttl: $(dg_ctxj)
	gen-rdf -f ttl --context $(dg_ctxj) $(dg_yaml) > $@

linkml_mira.ttl: $(mira_ctxj)
	gen-rdf -f ttl --context $(mira_ctxj) $(mira_yaml) > $@

$(mira_ctxj): $(dg_ctxj)
$(dg_ctxj): src/discoursegraphs/discoursegraphs_base.context.jsonld src/prov/prov.context.jsonld src/schemaorg/schemaorg.context.jsonld
src/discoursegraphs/discoursegraphs_base.context.jsonld: src/sioc/sioc.context.jsonld
src/sioc/sioc.context.jsonld: src/dc/dc.context.jsonld
