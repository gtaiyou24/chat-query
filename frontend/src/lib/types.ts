export type User = {
    username: string;
    emailAddress: string;
    tenants: {
        id: string;
        name: string;
    }[];
    accounts: {
        provider: string;
        providerAccountId: string;
    }[];
}

export type Tenant = {
    id: string;
    name: string;
};

export type Project = {
    id: string;
    name: string;
};


export type SemanticType = 'quantitative' | 'nominal' | 'ordinal' | 'temporal';

export interface Field {
    fid: string;
    name: string;
    semanticType: SemanticType;
}

export interface Row {
    [key: string]: any;
}

export interface Dataset {
    fields: Field[];
    dataSource: Row[];
}


export interface ChatMessage {
    role: "user" | "assistant" | "system";
    content: string;
}
export interface ChatResponse {
    id: string;
    object: string;
    model: string;
    usage: {
        prompt_tokens: number;
        completion_tokens: number;
        total_tokens: number;
    };
    choices: { message: ChatMessage }[];
}