# Plano de Implementação: Sousa Arqueopaleo

Este documento descreve as etapas técnicas e a arquitetura para criar o sistema de mapeamento interativo, focando nas tecnologias solicitadas (Flask, SQLite, sem frameworks JS complexos) e no leiaute visual em tons terra com mapa em tela cheia.

## Visão Geral do Projeto

O sistema será uma aplicação monolítica Flask com renderização do lado do servidor (Jinja2) e uma integração leve e eficiente de JavaScript "vanilla" no lado do cliente apenas para instanciar e controlar o mapa (usando Leaflet.js).

> [!NOTE]
> Leaflet.js é a biblioteca JavaScript open-source padrão ouro para mapas interativos web. Ela é levíssima e se alinha perfeitamente à restrição de não usar frameworks mastodônticos como React/Vue/Angular.

## Tecnologias e Bibliotecas

- **Backend:** Python + Flask
- **Banco de Dados:** SQLite (com SQLAlchemy como ORM, permitindo alterar a string de conexão futura para PostgreSQL de forma muito simples).
- **Autenticação Administrativa:** Flask-Login + Werkzeug Security (para hashes de senhas).
- **Frontend / Leiaute:** 
  - HTML5 Semântico + Jinja2 (Templates)
  - CSS3 Vanilla (com variáveis CSS, Flexbox e Grid para responsividade, reproduzindo a interface verde-oliva vista no design).
  - Leaflet.js (para o rendering do mapa "slippy" cobrindo a tela).

## Estrutura do Banco de Dados (Modelos SQLite)

1. **`User`**
   - `id` (Integer, Primary Key)
   - `username` (String, unique)
   - `password_hash` (String)

2. **`Site` (Sítios)**
   - `id` (Integer, Primary Key)
   - `name` (String, nome do local)
   - `description` (Text, descrição breve)
   - `latitude` (Float)
   - `longitude` (Float)
   - `youtube_url` (String, link direto ou ID do vídeo)

## Proposed Changes

---

### Camada Backend e Configurações Core

#### [NEW] `app.py`
Instanciação do Flask, configurações gerais, banco de dados e rotas.

#### [NEW] `models.py`
Modelos do SQLAlchemy (User, Site).

#### [NEW] `routes.py` (ou inclusão no app.py)
Rotas principais da aplicação:
- `/`: Rota principal que carrega o mapa.
- `/api/sites`: Endpoint JSON de sítios.
- `/login`, `/logout`: Autenticação.
- `/admin`: CRUD Administrativo de sítios.

---

### Camada Frontend (Jinja2 Templates)

#### [NEW] `templates/base.html`
Leiaute esqueleto (Header + block content).

#### [NEW] `templates/index.html`
Instancia o mapa cobrindo a tela abaixo do cabeçalho. Ao clicar em ponto, abre o pop-up com as opções solicitadas.

#### [NEW] `templates/admin.html`, `templates/login.html`
Telas limpas para usuários logados com um formulário de cadastro/edição de Sítios Arqueológicos.

---

### Camada Estáticos

#### [NEW] `static/css/style.css`
Estilos do sistema seguindo a interface da imagem baseada nas cores terrosas.

#### [NEW] `static/js/map.js`
Código Leaflet.js para renderizar instâncias no mapa.

## Open Questions

> [!IMPORTANT]
> - Você já possui os links dos tutoriais de vídeos 360 prontos que colocaremos do lado do botão de vídeo, ou posso criar links cegos por enquanto?
> - Devo criar um usuário administrador padrão na inicialização do sistema? Quais seriam as credenciais temporárias (ex: `admin` / `admin123`)?

## Verification Plan

### Testes Manuais
- Verificar renderização responsiva do mapa e dos modais no navegador.
- Testar a inserção de novos Sítios pelo painel Admin.
- Garantir que clicando nos pinos, o Google Maps direcione corretamente para a latitude e longitude.
