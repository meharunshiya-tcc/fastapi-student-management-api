import logging
import time

from fastapi import Request

logger = logging.getLogger("api")
logging.basicConfig(level=logging.INFO)

async def logging_middleware(request: Request, call_next):

    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    logger.info(
        "%s %s | Status: %s | Time: %.4f seconds",
        request.method,
        request.url.path,
        response.status_code,
        process_time
    )

    response.headers["X-Process-Time"] = str(process_time)

    return response