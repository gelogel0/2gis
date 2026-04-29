"""Instagram enrichment через Instaloader.

Внимание:
- Instagram aktivно банит scraping. Использование без логина — 50-200 запросов/час.
- С анонимным контекстом получаем: bio, followers, последние 12 постов (caption + likes).
- Если Instagram заблокирует — используй небольшие batch'и + sleep + смена IP.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any

import instaloader

log = logging.getLogger(__name__)


@dataclass
class IgProfile:
    username: str
    bio: str = ""
    followers: int = 0
    posts: list[dict[str, Any]] = field(default_factory=list)


def _get_loader() -> instaloader.Instaloader:
    return instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        post_metadata_txt_pattern="",
    )


def fetch_profile(username: str, max_posts: int = 3) -> IgProfile | None:
    """Возвращает bio + followers + последние max_posts постов.
    None если профиль не найден или приватный."""
    if not username:
        return None
    username = username.lstrip("@").strip()
    loader = _get_loader()
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
    except instaloader.exceptions.ProfileNotExistsException:
        log.warning("IG profile not found: @%s", username)
        return None
    except Exception as exc:
        log.warning("IG fetch error for @%s: %s", username, exc)
        return None

    if profile.is_private:
        log.info("IG @%s is private — пропускаем посты", username)
        return IgProfile(
            username=username,
            bio=profile.biography or "",
            followers=profile.followers,
            posts=[],
        )

    posts: list[dict[str, Any]] = []
    try:
        for idx, post in enumerate(profile.get_posts()):
            if idx >= max_posts:
                break
            posts.append({
                "url": f"https://www.instagram.com/p/{post.shortcode}/",
                "caption": (post.caption or "")[:500],
                "likes": post.likes,
                "date": post.date_utc.isoformat(),
            })
            time.sleep(0.5)  # вежливый delay
    except Exception as exc:
        log.warning("IG posts fetch error for @%s: %s", username, exc)

    return IgProfile(
        username=username,
        bio=profile.biography or "",
        followers=profile.followers,
        posts=posts,
    )
