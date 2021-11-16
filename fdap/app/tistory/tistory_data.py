from dataclasses import dataclass
from fdap.app.contracts.blog_client import BlogLoginInfo, BlogPostData


@dataclass(frozen=True)
class LoginInfo(BlogLoginInfo):
    client_id: str
    client_secret: str
    redirect_uri: str
    response_type: str
    kakao_id: str
    kakao_password: str
    state: str = ''


@dataclass(frozen=True)
class AccessTokenRequest:
    client_id: str
    client_secret: str
    redirect_uri: str
    code: str
    grant_type: str = 'authorization_code'


@dataclass(frozen=False)
class PostData(BlogPostData):
    title: str
    content: str
    published: str = None
    slogan: str = None
    tag: str = None
    password: str = None
    visibility: int = 0
    category: int = 0
    acceptComment: int = 1


class PostDto(PostData):
    sector: str = None
    year: str = None
    report_code: str = None
    url: str = None
    is_success: bool = False
