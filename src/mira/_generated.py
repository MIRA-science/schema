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
    """
    An activity is something that occurs over a period of time and acts upon or with entities; it may include consuming, processing, transforming, modifying, relocating, using, or generating entities.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity', 'from_schema': 'http://www.w3.org/ns/prov#'})

    pass


class Entity(ConfiguredBaseModel):
    """
    An entity is a physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity', 'from_schema': 'http://www.w3.org/ns/prov#'})

    pass


class CreativeWork(ConfiguredBaseModel):
    """
    (Schema.org) The most generic kind of creative work, including books, movies, photographs, software programs, etc.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:CreativeWork', 'from_schema': 'http://schema.org/'})

    pass


class Container(ConfiguredBaseModel):
    """
    An area in which content Items are contained.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'sioc:Container', 'from_schema': 'http://rdfs.org/sioc/ns#'})

    pass


class Item(ConfiguredBaseModel):
    """
    An Item is something which can be in a Container.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'sioc:Item', 'from_schema': 'http://rdfs.org/sioc/ns#'})

    format: Optional[str] = Field(default=None, description="""Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME].""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, description="""The content of the Item in plain text format.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })
    has_container: Optional[Container] = Field(default=None, description="""The Container to which this Item belongs.""", json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    creator: Optional[list[UserAccount]] = Field(default=None, description="""Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })


class FoafAgent(ConfiguredBaseModel):
    """
    An agent (eg. person, group, software or physical artifact).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'foaf:Agent',
         'from_schema': 'http://rdfs.org/sioc/ns#'})

    pass


class UserAccount(ConfiguredBaseModel):
    """
    A user account in an online community site.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'sioc:UserAccount', 'from_schema': 'http://rdfs.org/sioc/ns#'})

    accountName: Optional[str] = Field(default=None, description="""Indicates the name (identifier) associated with this online account.""", json_schema_extra = { "linkml_meta": {'domain': 'UserAccount',
         'domain_of': ['UserAccount'],
         'slot_uri': 'foaf:accountName'} })


class NodeSchema(Item):
    """
    Abstract class for node definitions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'dgb:NodeSchema',
         'from_schema': 'https://discoursegraphs.com/schema/dg_base',
         'mixin': True})

    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, description="""Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    title: Optional[str] = Field(default=None, description="""A name given to the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:title'} })
    description: Optional[Item] = Field(default=None, description="""Description may include but is not limited to: an abstract, a table of contents, a graphical representation, or a free-text account of the resource.""", json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, description="""The Container to which this Item belongs.""", json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, description="""Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME].""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, description="""The content of the Item in plain text format.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class AbstractRelationDef(NodeSchema):
    """
    Abstract meta-class for relation definitions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'dgb:AbstractRelationDef',
         'from_schema': 'https://discoursegraphs.com/schema/dg_base',
         'mixin': True})

    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, description="""Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    title: Optional[str] = Field(default=None, description="""A name given to the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:title'} })
    description: Optional[Item] = Field(default=None, description="""Description may include but is not limited to: an abstract, a table of contents, a graphical representation, or a free-text account of the resource.""", json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, description="""The Container to which this Item belongs.""", json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, description="""Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME].""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, description="""The content of the Item in plain text format.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class RelationDef(AbstractRelationDef):
    """
    Abstract class for relation definitions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'dgb:RelationDef',
         'from_schema': 'https://discoursegraphs.com/schema/dg_base',
         'mixin': True,
         'mixins': ['AbstractRelationDef']})

    domain: Optional[str] = Field(default=None, description="""A domain of the subject property.""", json_schema_extra = { "linkml_meta": {'domain': 'RelationDef',
         'domain_of': ['RelationDef'],
         'slot_uri': 'rdfs:domain'} })
    range: Optional[str] = Field(default=None, description="""A range of the subject property.""", json_schema_extra = { "linkml_meta": {'domain': 'RelationDef',
         'domain_of': ['RelationDef'],
         'slot_uri': 'rdfs:range'} })
    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, description="""Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    title: Optional[str] = Field(default=None, description="""A name given to the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:title'} })
    description: Optional[Item] = Field(default=None, description="""Description may include but is not limited to: an abstract, a table of contents, a graphical representation, or a free-text account of the resource.""", json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, description="""The Container to which this Item belongs.""", json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, description="""Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME].""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, description="""The content of the Item in plain text format.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class Agent(FoafAgent):
    """
    An agent engaging in an activity, and posting nodes.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'dgb:Agent',
         'from_schema': 'https://discoursegraphs.com/schema/dg_base'})

    name: Optional[str] = Field(default=None, description="""A name for some thing.""", json_schema_extra = { "linkml_meta": {'domain': 'FoafAgent', 'domain_of': ['Agent'], 'slot_uri': 'foaf:name'} })
    account: Optional[list[UserAccount]] = Field(default=None, description="""Indicates an account held by this agent.""", json_schema_extra = { "linkml_meta": {'domain': 'FoafAgent', 'domain_of': ['Agent'], 'slot_uri': 'foaf:account'} })


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
    creator: Optional[list[UserAccount]] = Field(default=None, description="""Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    title: Optional[str] = Field(default=None, description="""A name given to the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:title'} })
    description: Optional[Item] = Field(default=None, description="""Description may include but is not limited to: an abstract, a table of contents, a graphical representation, or a free-text account of the resource.""", json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, description="""The Container to which this Item belongs.""", json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, description="""Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME].""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, description="""The content of the Item in plain text format.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class Claim(NodeSchema):
    """
    Atomic, generalized assertions about the world that (propose to) answer research questions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'mira:Claim',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixins': ['NodeSchema']})

    addresses: Optional[list[Question]] = Field(default=None, title="Addresses", json_schema_extra = { "linkml_meta": {'domain': 'Claim',
         'domain_of': ['Claim'],
         'slot_uri': 'mira:addresses',
         'subproperty_of': 'RelationDef'} })
    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, description="""Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    title: Optional[str] = Field(default=None, description="""A name given to the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:title'} })
    description: Optional[Item] = Field(default=None, description="""Description may include but is not limited to: an abstract, a table of contents, a graphical representation, or a free-text account of the resource.""", json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, description="""The Container to which this Item belongs.""", json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, description="""Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME].""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, description="""The content of the Item in plain text format.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class Evidence(NodeSchema):
    """
    A specific empirical observation from a particular application of a research method
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'mira:Evidence',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixins': ['NodeSchema']})

    grounds: Optional[list[Evidence]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Study',
         'domain_of': ['Evidence', 'Study'],
         'inverse': 'is_grounded_in'} })
    observationStatement: Optional[Claim] = Field(default=None, title="Observation statement", json_schema_extra = { "linkml_meta": {'domain': 'Evidence',
         'domain_of': ['Evidence'],
         'slot_uri': 'mira:observationStatement',
         'subproperty_of': 'RelationDef'} })
    observationOriginActivity: Optional[Activity] = Field(default=None, title="Observation origin process", description="""An experiment or study at the origin of the data on which the observation is based""", json_schema_extra = { "linkml_meta": {'domain': 'Evidence',
         'domain_of': ['Evidence'],
         'slot_uri': 'mira:observationOriginActivity',
         'subproperty_of': 'RelationDef'} })
    observationBase: Optional[Entity] = Field(default=None, title="Observation base", description="""The data on which the observation is based""", json_schema_extra = { "linkml_meta": {'domain': 'Evidence',
         'domain_of': ['Evidence'],
         'mixins': ['RelationDef'],
         'slot_uri': 'mira:observationBase'} })
    sourceDocument: Optional[SourceDocument] = Field(default=None, title="Source document", description="""A document that described the activity which led to the data on which the observation is based""", json_schema_extra = { "linkml_meta": {'domain': 'Evidence',
         'domain_of': ['Evidence'],
         'slot_uri': 'mira:sourceDocument',
         'subproperty_of': 'RelationDef'} })
    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, description="""Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    title: Optional[str] = Field(default=None, description="""A name given to the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:title'} })
    description: Optional[Item] = Field(default=None, description="""Description may include but is not limited to: an abstract, a table of contents, a graphical representation, or a free-text account of the resource.""", json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, description="""The Container to which this Item belongs.""", json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, description="""Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME].""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, description="""The content of the Item in plain text format.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class Study(NodeSchema, Activity):
    """
    An activity — an experiment or analysis — that produces evidence.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'mira:Study',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixins': ['NodeSchema', 'Activity']})

    request_for: Optional[list[Study]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Request', 'domain_of': ['Study', 'Request']} })
    follows: Optional[list[Protocol]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Study', 'domain_of': ['Study']} })
    grounds: Optional[list[Evidence]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Study',
         'domain_of': ['Evidence', 'Study'],
         'inverse': 'is_grounded_in'} })
    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, description="""Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    title: Optional[str] = Field(default=None, description="""A name given to the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:title'} })
    description: Optional[Item] = Field(default=None, description="""Description may include but is not limited to: an abstract, a table of contents, a graphical representation, or a free-text account of the resource.""", json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, description="""The Container to which this Item belongs.""", json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, description="""Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME].""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, description="""The content of the Item in plain text format.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class Request(NodeSchema):
    """
    A unit of work the community can pick up — issue-tracker-shaped.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'mira:Request',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixins': ['NodeSchema']})

    request_for: Optional[list[Study]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Request', 'domain_of': ['Study', 'Request']} })
    request_target: Optional[list[Claim]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'Request', 'domain_of': ['Request']} })
    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, description="""Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    title: Optional[str] = Field(default=None, description="""A name given to the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:title'} })
    description: Optional[Item] = Field(default=None, description="""Description may include but is not limited to: an abstract, a table of contents, a graphical representation, or a free-text account of the resource.""", json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, description="""The Container to which this Item belongs.""", json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, description="""Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME].""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, description="""The content of the Item in plain text format.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class Protocol(NodeSchema, Activity):
    """
    The method or experimental approach a Study follows to generate the evidence.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'mira:Protocol',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixins': ['NodeSchema', 'Activity']})

    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, description="""Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    title: Optional[str] = Field(default=None, description="""A name given to the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:title'} })
    description: Optional[Item] = Field(default=None, description="""Description may include but is not limited to: an abstract, a table of contents, a graphical representation, or a free-text account of the resource.""", json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, description="""The Container to which this Item belongs.""", json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, description="""Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME].""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, description="""The content of the Item in plain text format.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


class SourceDocument(NodeSchema, CreativeWork):
    """
    Some research source document that reports/generates evidence, like a book, conference paper, or journal article
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'dg:SourceDocument',
         'from_schema': 'http://purl.org/mira-science/mira#',
         'mixins': ['NodeSchema'],
         'title': 'Source document'})

    describesActivity: Optional[Activity] = Field(default=None, title="Describes activity", json_schema_extra = { "linkml_meta": {'domain': 'CreativeWork',
         'domain_of': ['SourceDocument'],
         'slot_uri': 'mira:describesActivity',
         'subproperty_of': 'subject'} })
    created: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:created'} })
    modified: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:modified'} })
    creator: Optional[list[UserAccount]] = Field(default=None, description="""Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item', 'NodeSchema'], 'slot_uri': 'dct:creator'} })
    title: Optional[str] = Field(default=None, description="""A name given to the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NodeSchema'], 'slot_uri': 'dct:title'} })
    description: Optional[Item] = Field(default=None, description="""Description may include but is not limited to: an abstract, a table of contents, a graphical representation, or a free-text account of the resource.""", json_schema_extra = { "linkml_meta": {'domain': 'NodeSchema',
         'domain_of': ['NodeSchema'],
         'slot_uri': 'dct:description'} })
    has_container: Optional[Container] = Field(default=None, description="""The Container to which this Item belongs.""", json_schema_extra = { "linkml_meta": {'domain': 'Item',
         'domain_of': ['Item', 'NodeSchema'],
         'inverse': 'container_of',
         'slot_uri': 'sioc:has_container'} })
    format: Optional[str] = Field(default=None, description="""Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME].""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'dct:format'} })
    content: Optional[str] = Field(default=None, description="""The content of the Item in plain text format.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Item'], 'slot_uri': 'sioc:content'} })


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
