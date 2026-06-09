

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
 * Abstract class for node definitions
 */
export interface NodeSchema extends Item {
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
 * Abstract meta-class for relation definitions
 */
export interface AbstractRelationDef extends NodeSchema {
}


/**
 * Abstract class for relation definitions
 */
export interface RelationDef extends AbstractRelationDef {
    /** A domain of the subject property. */
    domain?: NodeSchema,
    /** A range of the subject property. */
    range?: NodeSchema,
}


/**
 * Abstract class for relation definitions
 */
export interface RelationInstance extends Statement, NodeSchema {
    /** The source of a binary relation */
    source?: "rdf_subject",
    /** The destination of a binary relation */
    destination?: "rdf_object",
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
    supports?: ("RelationDef" | "observationBase")[],
    opposes?: ("RelationDef" | "observationBase")[],
}


/**
 * Scientific unknowns that we want to make known, and are addressable by the systematic application of research methods
 */
export interface Question extends NodeSchema {
}


/**
 * Atomic, generalized assertions about the world that (propose to) answer research questions
 */
export interface Claim extends NodeSchema {
    addresses?: ("RelationDef" | "observationBase")[],
}


/**
 * A specific empirical observation from a particular application of a research method
 */
export interface Evidence extends NodeSchema {
    grounds?: Evidence[],
    observationStatement?: "RelationDef" | "observationBase",
    /** An experiment or study at the origin of the data on which the observation is based */
    observationOriginActivity?: "RelationDef" | "observationBase",
    /** The data on which the observation is based */
    observationBase?: Entity,
    /** A document that described the activity which led to the data on which the observation is based */
    sourceDocument?: "RelationDef" | "observationBase",
}


/**
 * An activity — an experiment or analysis — that produces evidence.
 */
export interface Study extends NodeSchema, Activity {
    request_for?: Study[],
    follows?: Protocol[],
    grounds?: Evidence[],
}


/**
 * A unit of work the community can pick up — issue-tracker-shaped.
 */
export interface Request extends NodeSchema {
    request_for?: Study[],
    request_target?: Claim[],
}


/**
 * The method or experimental approach a Study follows to generate the evidence.
 */
export interface Protocol extends NodeSchema, Activity {
}


/**
 * Some research source document that reports/generates evidence, like a book, conference paper, or journal article
 */
export interface SourceDocument extends CreativeWork, NodeSchema {
    describesActivity?: "subject",
}


/**
 * A criterion by which a node (proposal, claim or activity) is evaluated.
 */
export interface Criterion {
}


/**
 * The scale against which a specific endorsement is measured
 */
export interface EvaluationScale extends NodeSchema {
    minimum?: number,
    maximum?: number,
    criterion?: Criterion,
}


/**
 * An evaluation by an agent that a node (proposal, claim or activity) falls somewhere on a scale.
 */
export interface Evaluation {
    /** Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity. */
    creator?: UserAccount[],
    scale?: EvaluationScale,
    magnitude?: number,
    created?: string,
    modified?: string,
    /** The destination of a binary relation */
    destination?: "rdf_object",
    /** The Container to which this Item belongs. */
    has_container?: Container,
}


