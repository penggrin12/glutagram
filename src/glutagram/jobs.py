import asyncio
import time
from random import random

from aioe621.enums import PostRating
from aioe621.objects import TagSet
from aioe621.schemas.posts import Post
from aiogram.enums import ParseMode
from aiogram.exceptions import AiogramError, TelegramRetryAfter

from glutagram.config import Config, config
from glutagram.globals import e621, bot
from glutagram.storage import Storage
from glutagram.utils import get_post_url, get_pretty_rating, get_tags_href


def _should_spoiler(post: Post, chat: Config.TelegramChat) -> bool:
    return chat.spoiler_non_safe and post.rating != PostRating.SAFE


def _get_caption(post: Post, chat: Config.TelegramChat) -> str | None:
    if not chat.add_caption:
        return None

    return (
        f'<a href="{get_post_url(post)}">{post.id}</a> by {get_tags_href(post.tags.artist)}'
        f"\n❤️ <i>{post.score.total}</i> ⭐️ <i>{post.stats.fav_count}</i>"
        f"\n<b>{get_pretty_rating(post)}</b>"
    )


async def _send_post(post: Post, chat_id: int, chat: Config.TelegramChat) -> None:
    if post.sample.url is None:
        print(f"[-] failed sending {post.id}: .sample.url is None")
        return

    try:
        await bot.send_photo(chat_id=chat_id, photo=post.sample.url, caption=_get_caption(post, chat),
                             has_spoiler=_should_spoiler(post, chat), parse_mode=ParseMode.HTML)
        print(f"[+] sent {post.id}")
    except TelegramRetryAfter as e:
        print(f"[-] got a 429 while sending {post.id}. waiting {e.retry_after}s.")
        time.sleep(e.retry_after)  # not async, cuz it needs to be global
    except AiogramError as e:
        print(f"[-] failed sending {post.id}: {e}")


async def gather(storage: Storage, chat_id: int, chat: Config.TelegramChat) -> None:
    tagset = TagSet(chat.watching) \
        .with_blacklist(config.global_blacklist + chat.blacklist)
    # .with_order(PostSortOrder.ID) \

    posts = await e621.posts.list(tagset, limit=10)
    print(f"found {len(posts)}")
    for post in posts:
        if not storage.try_appending(post.id):
            print(f"skipped {post.id}")
            continue
        await _send_post(post, chat_id, chat)

        # wait 5 + (0..2) seconds
        await asyncio.sleep(5.0 + (random() * 2.0))
