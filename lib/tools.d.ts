export declare const rag: {
  search(query: string, k: number, namespaces: string[], userId: string): Promise<any>;
};

export declare const budget: {
  analyze(userId: string, horizonDays: number): Promise<any>;
};

export declare const crm: {
  lookup(identifier: string): Promise<any>;
};

export declare const kyc: {
  verify(userId: string, docRefs: string[]): Promise<any>;
};

export declare const payments: {
  offerPreview(userId: string, productId: string): Promise<any>;
};

export declare const avatar: {
  speak(text: string, personaVoice: string, ssml?: string): Promise<any>;
};
