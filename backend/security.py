import os


def allowed_origins() -> list[str]:
    environment = os.getenv("APP_ENV", "development").strip().lower()
    configured = os.getenv("CORS_ORIGINS")
    if environment == "production" and not configured:
        hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
        if hostname:
            hostname = hostname.removeprefix("https://").removeprefix("http://")
            return [f"https://{hostname}"]
        raise RuntimeError("CORS_ORIGINS must be set in production.")
    if configured is None:
        return ["http://localhost:5173", "http://localhost:3000"]

    origins = [origin.strip().rstrip("/") for origin in configured.split(",") if origin.strip()]
    if "*" in origins:
        raise RuntimeError("Wildcard CORS origins are not permitted.")
    for origin in origins:
        secure = origin.startswith("https://")
        local_dev = environment != "production" and origin.startswith(
            ("http://localhost", "http://127.0.0.1")
        )
        if not (secure or local_dev):
            raise RuntimeError("CORS origins must use HTTPS outside local development.")
    return origins
