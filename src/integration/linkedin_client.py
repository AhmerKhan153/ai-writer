"""LinkedIn posting client.

Publishes a text-only share to the authenticated member's feed via the
`ugcPosts` API. Requires two env vars obtained through a one-time OAuth flow:

    LINKEDIN_ACCESS_TOKEN  - member access token with the `w_member_social` scope
    LINKEDIN_AUTHOR_URN    - the member urn, e.g. "urn:li:person:AbC123"

See LINKEDIN_SETUP.md for the exact one-time registration + OAuth steps.
"""

from typing import Optional

import requests

from config import LINKEDIN_ACCESS_TOKEN, LINKEDIN_AUTHOR_URN

_UGC_POSTS_URL = "https://api.linkedin.com/v2/ugcPosts"


class LinkedInError(RuntimeError):
    pass


def _build_payload(content: str) -> dict:
    return {
        "author": LINKEDIN_AUTHOR_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }


def post_text(content: str) -> str:

    if not LINKEDIN_ACCESS_TOKEN or not LINKEDIN_AUTHOR_URN:
        raise LinkedInError(
            "LinkedIn is not configured. Set LINKEDIN_ACCESS_TOKEN and "
            "LINKEDIN_AUTHOR_URN (see LINKEDIN_SETUP.md)."
        )

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }

    response = requests.post(
        _UGC_POSTS_URL, headers=headers, json=_build_payload(content), timeout=20
    )

    if response.status_code not in (200, 201):
        raise LinkedInError(
            f"LinkedIn post failed ({response.status_code}): {response.text}"
        )

    post_urn: Optional[str] = response.headers.get("X-RestLi-Id") or (
        response.json().get("id") if response.content else None
    )
    if post_urn:
        return f"https://www.linkedin.com/feed/update/{post_urn}"
    return "https://www.linkedin.com/feed/"
