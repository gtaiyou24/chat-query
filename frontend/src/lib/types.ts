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