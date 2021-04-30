# https://gateway.octii.chat/communities/[community_id]

Gets information on a community or "server".

Response:
```ts
export interface CommunityData {
    icon: string;
    large: boolean;
    owner_id: string;
    system_channel_id: string;
    name: string;
    id: string;
    base_permissions: number[];
    channels: string[];
    organization: boolean;
}
```