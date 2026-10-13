from urllib.parse import quote

from aioe621.enums import PostRating
from aioe621.objects import TagSet
from aioe621.schemas.posts import Post

HIDDEN_TAGS = ("conditional_dnp",)
PRETTY_RATINGS = {PostRating.SAFE: "🟢 Safe", PostRating.QUESTIONABLE: "🟡 Questionable",
                  PostRating.EXPLICIT: "🔴 Explicit"}


def get_tags_url(tagset: TagSet) -> str:
    return f"https://e621.net/posts?tags={quote(tagset.flattened())}"


def get_tags_href(tagset: TagSet) -> str:
    stripped_tagset = TagSet(tagset.difference(HIDDEN_TAGS))
    return f'<a href="{get_tags_url(stripped_tagset)}">{", ".join(stripped_tagset.as_strings())}</a>'


def get_post_url(post: Post) -> str:
    return f"https://e621.net/posts/{post.id}"


def get_pretty_rating(post: Post) -> str:
    return PRETTY_RATINGS[post.rating]
