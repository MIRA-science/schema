


export interface Activity {
}



export interface Entity {
}



export interface CreativeWork {
}



export interface Container {
}



export interface Item {
    format?: string,
    content?: string,
    has_container?: Container,
    creator?: UserAccount[],
}



export interface FoafAgent {
}



export interface UserAccount {
    accountName?: string,
}



export interface Any {
}



export interface NodeSchema extends Item {
    created?: string,
    modified?: string,
    creator?: UserAccount[],
    title?: string,
    description?: Item,
    has_container?: Container,
}



export interface AbstractRelationDef extends NodeSchema {
}



export interface RelationDef extends AbstractRelationDef {
    domain?: NodeSchema,
    range?: NodeSchema,
}


/**
 * An agent engaging in an activity, and posting MIRA nodes.
 */
export interface Agent extends FoafAgent {
    name?: string,
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
}


/**
 * A specific empirical observation from a particular application of a research method
 */
export interface Evidence extends NodeSchema {
}



export interface Study extends NodeSchema, Activity {
}



export interface Request extends NodeSchema {
}



export interface Protocol extends NodeSchema, Activity {
}


/**
 * Some research source document that reports/generates evidence, like a book, conference paper, or journal article
 */
export interface SourceDocument extends CreativeWork, NodeSchema {
}



