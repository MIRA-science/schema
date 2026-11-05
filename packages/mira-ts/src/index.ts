

/**
 * An activity is something that occurs over a period of time and acts upon or with entities; it may include consuming, processing, transforming, modifying, relocating, using, or generating entities.
 */
export interface Activity {
}


/**
 * An entity is a physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary.
 */
export interface Entity {
}


/**
 * (Schema.org) The most generic kind of creative work, including books, movies, photographs, software programs, etc.
 */
export interface CreativeWork {
}


/**
 * An area in which content Items are contained.
 */
export interface Container {
}


/**
 * An Item is something which can be in a Container.
 */
export interface Item {
    /** Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME]. */
    format?: string,
    /** The content of the Item in plain text format. */
    content?: string,
    /** The Container to which this Item belongs. */
    has_container?: Container,
    /** Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity. */
    creator?: UserAccount[],
}


/**
 * An agent (eg. person, group, software or physical artifact).
 */
export interface FoafAgent {
}


/**
 * A user account in an online community site.
 */
export interface UserAccount {
    /** Indicates the name (identifier) associated with this online account. */
    accountName?: string,
}


/**
 * The class resource, everything.
 */
export interface Resource {
}



export interface Statement {
    /** The subject of the subject RDF statement. */
    rdf_subject?: Resource,
    /** The predicate of the subject RDF statement. */
    rdf_predicate?: Resource,
    /** The object of the subject RDF statement. */
    rdf_object?: Resource,
}



export interface Any {
}


/**
 * Superclass of all discourse graph nodes
 */
export interface Node extends Item {
    created?: string,
    modified?: string,
    /** Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity. */
    creator?: UserAccount[],
    /** A name given to the resource. */
    title?: string,
    /** Description may include but is not limited to: an abstract, a table of contents, a graphical representation, or a free-text account of the resource. */
    description?: Item,
    /** The Container to which this Item belongs. */
    has_container?: Container,
}


/**
 * Metaclass of node types
 */
export interface NodeSchema {
    created?: string,
    modified?: string,
    /** Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity. */
    creator?: UserAccount[],
}


/**
 * Abstract class for relation definitions
 */
export interface RelationDef extends NodeSchema {
    /** A domain of the subject property. */
    domain?: NodeSchema,
    /** A range of the subject property. */
    range?: NodeSchema,
}


/**
 * Deprecated alias of RelationDef
 */
export interface AbstractRelationDef extends RelationDef {
}


/**
 * Abstract class for relation instances
 */
export interface RelationInstance extends Statement, Node {
    /** The source of a binary relation */
    source?: Node,
    /** The destination of a binary relation */
    destination?: Node,
}


/**
 * An agent engaging in an activity, and posting nodes.
 */
export interface Agent extends FoafAgent {
    /** A name for some thing. */
    name?: string,
    /** Indicates an account held by this agent. */
    account?: UserAccount[],
}


/**
 * A node that can support or oppose another node
 */
export interface Argument {
    supports?: Claim[],
    opposes?: Claim[],
}


/**
 * Scientific unknowns that we want to make known, and are addressable by the systematic application of research methods
 */
export interface Question extends Node {
}


/**
 * Atomic, generalized assertions about the world that (propose to) answer research questions
 */
export interface Claim extends Node, Argument {
    addresses?: Question[],
}


/**
 * A specific empirical observation from a particular application of a research method
 */
export interface Evidence extends Node, Argument {
    grounds?: Evidence[],
    observationStatement?: Claim,
    /** An experiment or study at the origin of the data on which the observation is based */
    observationOriginActivity?: Activity,
    /** The data on which the observation is based */
    observationBase?: Entity,
    /** A document that described the activity which led to the data on which the observation is based */
    sourceDocument?: SourceDocument,
}


/**
 * An activity — an experiment or analysis — that produces evidence.
 */
export interface Study extends Node, Activity {
    request_for?: Study[],
    follows?: Protocol[],
    grounds?: Evidence[],
}


/**
 * A unit of work the community can pick up — issue-tracker-shaped.
 */
export interface Request extends Node {
    request_for?: Study[],
    request_target?: Claim[],
}


/**
 * The method or experimental approach a Study follows to generate the evidence.
 */
export interface Protocol extends Node, Activity {
}


/**
 * Some research source document that reports/generates evidence, like a book, conference paper, or journal article
 */
export interface SourceDocument extends CreativeWork, Node {
    describesActivity?: Activity,
}


