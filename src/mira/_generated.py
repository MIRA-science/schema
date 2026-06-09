from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.11.0"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'mira',
     'default_range': 'string',
     'id': 'http://purl.org/mira-science/mira#',
     'imports': ['prov', 'schemaorg', 'discoursegraphs_base'],
     'name': 'mira',
     'prefixes': {'mira': {'prefix_prefix': 'mira',
                           'prefix_reference': 'http://purl.org/mira-science/mira#'},
                  'owl': {'prefix_prefix': 'owl',
                          'prefix_reference': 'http://www.w3.org/2002/07/owl#'},
                  'rdf': {'prefix_prefix': 'rdf',
                          'prefix_reference': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'},
                  'rdfs': {'prefix_prefix': 'rdfs',
                           'prefix_reference': 'http://www.w3.org/2000/01/rdf-schema#'}},
     'source_file': 'mira.yaml'} )


class Activity(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity', 'from_schema': 'http://www.w3.org/ns/prov#'})

    pass


class Entity(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity', 'from_schema': 'http://www.w3.org/ns/prov#'})

    pass


class CreativeWork(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:CreativeWork', 'from_schema': 'http://schema.org/'})

    pass


class Container(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'sioc:Container', 'from_schema': 'http://rdfs.org/sioc/ns#'})

    pass


class Item(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'sioc:Item', 'from_schema': 'http://rdfs.org/sioc/ns#'})

    format: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })
    has_container: Optional[Container] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    creator: Optional[list[UserAccount]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })


class FoafAgent(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'foaf:Agent',
         'from_schema': 'http://rdfs.org/sioc/ns#'})

    pass


class UserAccount(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'sioc:UserAccount', 'from_schema': 'http://rdfs.org/sioc/ns#'})

    accountName: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'UserAccount',
         'domain_of': ['UserAccount'],
         'slot_uri': 'foaf:accountName'} })


class NodeSchema(Item):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'dgb:NodeSchema',
         'from_schema': 'https://discoursegraphs.com/schema/dg_base',
         'mixin': True})

    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    description: Optional[Item] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class AbstractRelationDef(NodeSchema):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'dgb:AbstractRelationDef',
         'from_schema': 'https://discoursegraphs.com/schema/dg_base',
         'mixin': True})

    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    description: Optional[Item] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class RelationDef(AbstractRelationDef):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'dgb:RelationDef',
         'from_schema': 'https://discoursegraphs.com/schema/dg_base',
         'mixin': True,
         'mixins': ['AbstractRelationDef']})

    domain: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'RelationDef',
         'domain_of': ['RelationDef'],
         'slot_uri': 'rdfs:domain'} })
    range: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'RelationDef',
         'domain_of': ['RelationDef'],
         'slot_uri': 'rdfs:range'} })
    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    description: Optional[Item] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class Agent(FoafAgent):
    """
    An agent engaging in an activity, and posting MIRA nodes.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'dgb:Agent',
         'from_schema': 'https://discoursegraphs.com/schema/dg_base'})

    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'FoafAgent', 'domain_of': ['Agent'], 'slot_uri': 'foaf:name'} })
    account: Optional[list[UserAccount]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'FoafAgent', 'domain_of': ['Agent'], 'slot_uri': 'foaf:account'} })


class Argument(ConfiguredBaseModel):
    """
    A node that can support or oppose another node
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'mira:Argument',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixin': True})

    supports: Optional[list[Claim]] = Field(default=None, title="Supports", json_schema_extra = { "linkml_meta": {'domain': 'Argument',
         'domain_of': ['Argument'],
         'slot_uri': 'mira:supports',
         'subproperty_of': 'RelationDef'} })
    opposes: Optional[list[Claim]] = Field(default=None, title="Opposes", json_schema_extra = { "linkml_meta": {'domain': 'Argument',
         'domain_of': ['Argument'],
         'slot_uri': 'mira:opposes',
         'subproperty_of': 'RelationDef'} })


class Question(NodeSchema):
    """
    Scientific unknowns that we want to make known, and are addressable by the systematic application of research methods
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'mira:Question',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixins': ['NodeSchema']})

    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    description: Optional[Item] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class Claim(NodeSchema):
    """
    Atomic, generalized assertions about the world that (propose to) answer research questions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'mira:Claim',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixins': ['NodeSchema']})

    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    description: Optional[Item] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class Evidence(NodeSchema):
    """
    A specific empirical observation from a particular application of a research method
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'mira:Evidence',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixins': ['NodeSchema']})

    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    description: Optional[Item] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class Study(NodeSchema, Activity):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'mira:Study',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixins': ['NodeSchema', 'Activity']})

    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    description: Optional[Item] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class Request(NodeSchema):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'mira:Request',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixins': ['NodeSchema']})

    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    description: Optional[Item] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class Protocol(NodeSchema, Activity):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'mira:Protocol',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixins': ['NodeSchema', 'Activity']})

    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    description: Optional[Item] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class SourceDocument(NodeSchema, CreativeWork):
    """
    Some research source document that reports/generates evidence, like a book, conference paper, or journal article
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'dg:SourceDocument',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixins': ['NodeSchema'],
         'title': 'Source document'})

    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    description: Optional[Item] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Activity.model_rebuild()
Entity.model_rebuild()
CreativeWork.model_rebuild()
Container.model_rebuild()
Item.model_rebuild()
FoafAgent.model_rebuild()
UserAccount.model_rebuild()
NodeSchema.model_rebuild()
AbstractRelationDef.model_rebuild()
RelationDef.model_rebuild()
Agent.model_rebuild()
Argument.model_rebuild()
Question.model_rebuild()
Claim.model_rebuild()
Evidence.model_rebuild()
Study.model_rebuild()
Request.model_rebuild()
Protocol.model_rebuild()
SourceDocument.model_rebuild()
