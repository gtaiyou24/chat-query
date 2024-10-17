# Chat Query

## 🛠Technology
### 🔨Backend

 - 開発言語 : Python
 - フレームワーク : [FastAPI](https://fastapi.tiangolo.com/)
 - DB : MySQL / Redis
 - CI/CD : [GitHub Actions](https://docs.github.com/ja/actions)

### 🔧Frontend

 - 開発言語 : TypeScript
 - フレームワーク : [Next.js 14 App Router](https://nextjs.org/docs)
 - 認証 : [Auth.js(NextAuth.js V5)](https://authjs.dev/)
 - CSS : [Tailwind](https://tailwindcss.com/) / [shadcn/ui](https://ui.shadcn.com/) / [Headless UI](https://headlessui.com/)
 - グローバルステート管理 : [zustand](https://zustand-demo.pmnd.rs/)
 - CI/CD : [GitHub Actions](https://docs.github.com/ja/actions)

### ⚙️Infrastructure

 - インフラ環境 : GCP Cloud Run / [Neon](https://neon.tech/) / [Upstash](https://upstash.com/)
 - IaC : Terraform
 - エラー/ログ監視 : Sentry / New Relic

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

<details><summary><b>🛠️ Generate client code types from OpenAPI</b></summary>

```bash
cd frontend
npm run generate-client
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
