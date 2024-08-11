# Analytics GPT

## 🛠Technology
### 🔨Backend

 - Language : Python
 - Framework : FastAPI
 - DataBase : MySQL / Redis
 - Infra : GCP Cloud Run / [Neon](https://neon.tech/) / [Upstash](https://upstash.com/)
 - CI/CD : GitHub Actions

### 🔧Frontend

 - Language : TypeScript
 - Framework : Next.js 14 App Router
 - Auth : [Auth.js(NextAuth.js V5)](https://authjs.dev/)
 - CSS : [Tailwind](https://tailwindcss.com/) / [shadcn/ui](https://ui.shadcn.com/) / [Headless UI](https://headlessui.com/)
 - Global State : [zustand](https://zustand-demo.pmnd.rs/)
 - CI/CD : GitHub Actions

## ❓How To
<details><summary><b>🏃 Start</b></summary>

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

</details>

<details><summary><b>🔌 Connect to local DB</b></summary>

Connect to Redis
```bash
redis-cli
```

Connect to MySQL
```bash
mysql -h 127.0.0.1 -P 3306 -u user -p
# Enter password: pass
```

</details>

<details><summary><b>🛠️ Generate Typescript types from OpenAPI</b></summary>

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

</details>

<details><summary><b>✅ Test</b></summary>

```bash
pip install pytest pytest-env httpx
pytest -v ./test
```

</details>
