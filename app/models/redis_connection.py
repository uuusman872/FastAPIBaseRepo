import redis.asyncio as redis
from config import Config
JTI_EXPIRY = 3600


token_blocklist = redis.Redis(
    host=Config.REDIS_HOST, 
    port=Config.REDIS_PORT,
    db=0,
    decode_responses=True
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.setex(
        name=jti,
        time=JTI_EXPIRY,
        value=""
    )

async def token_in_blacklist(jti: str) -> bool:
    return await token_blocklist.exists(jti) > 0
