# Analytics GPT

## 🛠️How To
### 🏃Start

**Step.1**<br/>
Create a `.env` file at `./backend` folder.
```bash
cp backend/.env.local backend/.env
```

**Step.2**<br/>
Then run `docker-compose up` to start the server.
```bash
docker-compose up --build
```

 - [Front](http://localhost:3000)
 - [Swagger UI](http://localhost:8000/docs)
 - [MailHog](http://0.0.0.0:8025/)

**Appendix**

```bash
# connect to redis
redis-cli
```

```bash
mysql -h 127.0.0.1 -P 3306 -u user -p
# Enter password: pass
```

### 🛠️ Generate Typescript types from OpenAPI

```bash
cd frontend
npm i openapi-fetch
npm i -D openapi-typescript typescript
```

```bash
npx openapi-typescript http://localhost:8000/openapi.json -o ./src/lib/backend/type.ts
```

Appendix

 - [openapi-typescript | OpenAPI TypeScript](https://openapi-ts.pages.dev/introduction)

### ✅ Test

```bash
pip install pytest pytest-env httpx
pytest -v ./test
```