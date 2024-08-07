import {auth} from "@/lib/auth/auth";
import {createBackendClient} from "@/lib/backend/create-client";
import {components} from "@/lib/backend/type";
import {TokenSet} from "next-auth";
import {User} from "@/lib/types";


export const postAuthToken = async (email: string, password: string)=> {
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
        emailAddress: data.emailAddress,
        tenants: data.tenants,
        accounts: data.accounts.map((account: components["schemas"]["Account"]) => {
            return {provider: account.provider, providerAccountId: account.provider_account_id};
        })
    } as User;
}