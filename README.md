# Klass Backend

Backend Django para gestão de matrículas com foco em pronto para produção.

## Configuração de ambiente
Defina as variáveis no `.env` (ou variáveis do sistema) antes de iniciar:

- `DJANGO_SECRET_KEY`: chave secreta forte para produção.
- `DJANGO_DEBUG`: use `False` em produção.
- `DJANGO_ALLOWED_HOSTS`: lista separada por vírgulas de domínios/IPs permitidos.
- `DATABASE_URL`: URL do banco (PostgreSQL/MySQL/SQLite) no formato `scheme://user:pass@host:port/dbname`.
- `DB_CONN_MAX_AGE`: (opcional) tempo de conexão persistente, padrão 60s.
- `DB_SSL_REQUIRE`: `true` para forçar SSL no banco gerenciado.
- `CORS_ALLOWED_ORIGINS`: origens permitidas para o front-end.
- `CSRF_TRUSTED_ORIGINS`: domínios confiáveis para CSRF.
- `SESSION_COOKIE_SECURE` e `CSRF_COOKIE_SECURE`: `true` para cookies apenas via HTTPS.
- `JWT_ACCESS_MINUTES` e `JWT_REFRESH_DAYS`: ajustes de tempo de vida dos tokens.

## Setup local
1. Crie o ambiente virtual e instale as dependências:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Execute migrações e crie um superusuário:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
3. Rode localmente (debug apenas em dev):
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Deploy em produção
1. Defina todas as variáveis de ambiente acima com valores de produção (chave secreta forte, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS` com domínios, `DATABASE_URL` de banco gerenciado, e origens CORS/CSRF do front-end).
2. Colete arquivos estáticos e aplique migrações:
   ```bash
   python manage.py collectstatic --noinput
   python manage.py migrate --noinput
   ```
3. Inicie a aplicação com um servidor WSGI (ex.: `gunicorn`), atrás de um proxy que termine HTTPS:
   ```bash
   gunicorn klass_backend.wsgi:application --bind 0.0.0.0:8000 --workers 3
   ```
4. Configure o proxy (Nginx/Traefik) para encaminhar para o Gunicorn, servir `staticfiles/` e adicionar cabeçalho `X-Forwarded-Proto` para suportar `SECURE_PROXY_SSL_HEADER`.
5. Crie um superusuário e cadastre professores/alunos conforme necessário.

## APIs relevantes pós-hardening
- Autenticação JWT: `POST /api/auth/token/` para obter `access`/`refresh`; `POST /api/auth/token/refresh/` para renovar.
- Documentação interativa: `GET /api/docs/` (Swagger) e `GET /api/schema/`.
- Endpoints de contas, cursos e matrículas permanecem sob autenticação padrão, agora priorizando JWT.

## Impacto das mudanças recentes
- Configurações dependem de variáveis de ambiente para chave secreta, debug, hosts, cookies e CORS/CSRF.
- Banco pode ser configurado via `DATABASE_URL` com suporte a SSL e pooling simples.
- Autenticação padrão passou a ser JWT (SimpleJWT) com tokens configuráveis e endpoints adicionados.
- Cookies de sessão/CSRF são seguros por padrão e o static root foi definido para `collectstatic` em produção.