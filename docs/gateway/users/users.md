# https://gateway.octii.chat/users/[user_id]

Gets information on a user.

Response:
```ts
export interface Badges {
}

export interface UserData {
    disabled: boolean;
    id: string;
    developer: boolean;
    badges: Badges;
    state: string;
    username: string;
    email: string;
    color: string;
    avatar: string;
    discriminator: number;
}
```