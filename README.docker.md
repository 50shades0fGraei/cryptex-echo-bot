Docker setup for Cryptex Echo

Quick start (requires Docker and Docker Compose):

1. Build and run both services:

```bash
# from project root
docker compose up --build
```

This will:
- Build and run the backend FastAPI app on http://localhost:5050
- Build and run the Next.js frontend on http://localhost:3000

2. Development notes:
- If you want hot-reload for the backend, uncomment the `volumes` section for the `backend` service in `docker-compose.yml` and add `--reload` to the uvicorn command in `Dockerfile.backend` or use an override docker-compose file.
- Frontend production image uses `npm run build` and `npm run start`. For local development use `cd frontend && npm run dev`.

Troubleshooting:
- If the frontend fails to build due to platform-specific swc binary issues on Windows, build using a non-alpine image (the provided Dockerfile uses Debian slim-based image to avoid that).
- If you need to add more Python dependencies, update `requirements.txt` and rebuild.
