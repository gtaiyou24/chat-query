import "next-auth/jwt"

declare module "next-auth" {
    interface TokenSet {
        access_token: string;
        refresh_token: string;
        token_type: 'bearer';
        expires_at: number;
    }
    interface Session {
        user: User["user"];
        accessToken?: string;
        refreshToken?: string;
        expiresAt?: number;
    }
    interface User {
        user: {
            name?: string | null;
            email?: string | null;
            tenant?: {
                id: string;
                name: string;
            };
            accounts: {
                provider: string;
                provider_account_id: string;
            }[];
        };
        accessToken?: string;
        refreshToken?: string;
        expiresAt?: number;
    }
}

declare module "next-auth/jwt" {
    interface JWT {
        accessToken?: string;
        refreshToken?: string;
        expiresAt?: number;
    }
}