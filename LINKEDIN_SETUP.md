# LinkedIn setup (one-time)

The app posts to your feed with the `ugcPosts` API. You need a member access
token with the `w_member_social` scope and your member URN. Do this once and
paste the results into `.env`.

## 1. Create a LinkedIn app
1. Go to https://www.linkedin.com/developers/apps and click **Create app**.
2. Associate it with a Company Page (required by LinkedIn, even a placeholder).
3. On the app's **Auth** tab, note the **Client ID** and **Client Secret**.
4. Add an **Authorized redirect URL**, e.g. `http://localhost:8000/callback`.

## 2. Request the product / scope
On the **Products** tab, add **Share on LinkedIn** (grants `w_member_social`).
Also add **Sign In with LinkedIn using OpenID Connect** if you want to fetch your
member id via the `userinfo` endpoint (step 4).

## 3. Get an access token (3-legged OAuth)
Open this URL in a browser (replace CLIENT_ID and REDIRECT_URI):

```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT_URI&scope=w_member_social%20openid%20profile
```

After you authorize, LinkedIn redirects to `REDIRECT_URI?code=XXODE`. Exchange
that code for a token:

```bash
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -d grant_type=authorization_code \
  -d code=THE_CODE \
  -d client_id=CLIENT_ID \
  -d client_secret=CLIENT_SECRET \
  -d redirect_uri=REDIRECT_URI
```

The response contains `access_token`. That is your `LINKEDIN_ACCESS_TOKEN`.

## 4. Get your author URN
With the token from step 3:

```bash
curl -H "Authorization: Bearer ACCESS_TOKEN" https://api.linkedin.com/v2/userinfo
```

The `sub` field is your member id. Your URN is `urn:li:person:<sub>`.

## 5. Fill in .env
```
LINKEDIN_ACCESS_TOKEN=your_access_token
LINKEDIN_AUTHOR_URN=urn:li:person:your_member_id
```

> Member tokens expire (typically ~60 days). When posting starts failing with a
> 401, repeat step 3 to get a fresh token.
