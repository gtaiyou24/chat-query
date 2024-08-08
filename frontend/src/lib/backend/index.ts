import {auth} from "@/lib/auth/auth";
import {createBackendClient} from "@/lib/backend/create-client";
import {components} from "@/lib/backend/type";
import {TokenSet} from "next-auth";
import {User} from "@/lib/types";


export const postRegisterUser = async (username: string, email: string, password: string) =>  {
    const {error} = await createBackendClient().POST("/auth/register", {
        cache: "no-cache",
        body: {
            username: username,
            email_address: email,
            password: password
        }
    });
    if (error) {
        console.log(error);
        throw Error('ユーザー登録に失敗しました。');
    }
}

export const postVerifyEmail = async (token: string): Promise<TokenSet> => {
    const { data, error } = await createBackendClient().POST("/auth/verify-email/{token}", {
        headers: { 'Content-Type': 'application/json' },
        params: { path: { token: token } },
    })
    if (error) {
        throw Error();
    }
    return data as TokenSet;
}

export const postAuthToken = async (email: string, password: string): Promise<TokenSet>=> {
    const {data, error} = await createBackendClient().POST("/auth/token", {
        cache: "no-cache",
        body: {
            email_address: email,
            password: password
        }
    });
    if (error?.type) {
        switch (error.type) {
            case 'USER_IS_NOT_VERIFIED':
                throw '確認メールを送信しました。メールをご確認してください。';
            case 'LOGIN_BAD_CREDENTIALS':
                throw 'メールアドレスまたはパスワードが間違っています';
            default:
                throw 'システムエラーが発生しました。しばらくお待ちください。';
        }
    }
    return data as TokenSet;
}

export const putAuthToken = async (token?: string): Promise<TokenSet> => {
    const {data, error} = await createBackendClient().PUT("/auth/token", {
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": `bearer ${token ? token : (await auth())?.refreshToken}`
        },
        cache: "no-cache",
    });
    if (error) {
        console.error(`トークンのリフレッシュに失敗しました。${error}`);
    }
    return data as TokenSet;
};

export const logout = async (token?: string) => {
    const { error } = await createBackendClient().DELETE("/auth/token", {
        headers: { "Authorization": `bearer ${token ? token : (await auth())?.accessToken}` },
        cache: 'no-cache'
    });
    if (error) {
        console.error(error);
    }
}


export const getMe = async (token?: string): Promise<User> => {
    const { data, error } = await createBackendClient().GET("/users/me", {
        headers: { "Authorization": `bearer ${token ? token : (await auth())?.accessToken}` },
        cache: 'no-cache'
    });
    if (error) {
        console.error(error);
    }
    return {
        username: data.username,
        emailAddress: data.email_address,
        tenants: [],
        accounts: data.accounts.map((account: components["schemas"]["Account"]) => {
            return {provider: account.provider, providerAccountId: account.provider_account_id};
        })
    } as User;
}