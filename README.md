# 🦖 Sousa Arqueopaleo (Dinotour)

**Sousa Arqueopaleo** é um sistema web responsivo e interativo criado para o mapeamento e roteirização virtual voltado para a rica Bacia Paleontológica e Sítios Arqueológicos na região de Sousa/PB. Esta plataforma não só localiza pontos históricos e trilhas de dinossauros num mapa preciso, mas também oferece imersão virtual, permitindo que turistas visitem os pontos via YouTube em alta qualidade ou por Realidade Virtual 360º de dentro de casa.

## 🌟 Funcionalidades Principais
- **Mapa Interativo Cartográfico:** Interface robusta com a biblioteca Leaflet. O mapa apresenta terrenos interativos ("outdoors") auto-ajustando a visão baseada na totalidade de pontos marcados.
- **Painel Administrativo (`/admin`):** Um BackOffice seguro para que pesquisadores ou a gerência possa popular marcadores (Sítios, Pistas e Achados). Inclui formulário simples com uploads para fotos do cabeçalho de exibição no mapa.
- **Visualizador VR 360º Nativo:** O sistema isola arquivos esféricos (Modo Cardboard WebXR nativo via **A-Frame**). Sítios que têm foto panorâmica recebem um ícone de "Entrar em 360º" onde a página mergulha em uma experiência que faz uso nativo do giroscópio de smartphones.
- **Roteirização GMaps Externa:** A partir do pino da rocha/pista no mapa, o turista pode clicar em `Traçar Rota`, transferindo precisamente as coordenadas pro seu GPS instalado localmente.
- **Alerta Semântico:** Sítios não enriquecidos (sem foto 360 e sem Youtube) trocam a cor dos marcadores para **Vermelho**, guiando historiadores nos pontos que mais carecem de atenção midiática.

## 🚀 Stack & Tecnologias
- **Backend Core:** Python + Flask (SQLAlchemy, Login e Werkzeug ProxyFix/ScriptsName) 
- **Banco de Dados:** SQLite Local.
- **Frontend App:** HTML5 Puro, CSS Puro Vanilla + Jinja.
- **Integração de Mapas:** [Leaflet.js](https://leafletjs.com/) & OpenTopoMap Tiles.
- **Engine 360VR/WebXR:** [A-Frame](https://aframe.io/).
- **Orquestração e Deploy:** Docker (Imagem construída em gunicorn) + Traefik Middleware (para suportar Proxy reverso sobre um prefixo de subdiretório).

## 🛠️ Como Executar Localmente - Modo Dev

Certifique-se de estar com a versão do Python 3+ instalada.

1. **Crie e Inicie o seu ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   ## Ative a Venv
   venv\Scripts\activate # Windows
   # source venv/bin/activate # Linux
   ```

2. **Instale as Dependências necessárias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Injetar Banco de Dados (DMS2DD Converter):**
   Rodando isso pela 1ª vez, ele formatará a base inteira extraindo os dados iniciais escritos usando o conversor Grados-DMS -> Coordenadas Decimais do Google automaticamente.
   ```bash
   flask seed
   ```
   > **Credenciais de Gerência Padrão (`/admin`):**
   > - **Usuário:**  `admin`
   > - **Senha base:** `IntegraMaker2025`

4. **Inicie o Servidor:**
   ```bash
   python app.py
   # Escutando em: http://127.0.0.1:5000
   ```

---

## 🐋 Como Fazer Deploy de Produção (Docker + Traefik)

O repositório já está entregue com um _Dockerfile_ fechado sob Gunicorn e o `docker-compose.yml` otimizado para produção.  
O orquestrador dele foi redigido assumindo o uso real sob a *Proxy Network* do Traefik da instituição para o host final. O Flask aqui reage à variável `APPLICATION_ROOT` de forma automática, permitindo que a raiz física do Front receba a resposta da API respeitando subdiretórios como o `/dinotour` sem bugar recursos estáticos.

Basta instanciar onde desejar:
```bash
docker-compose up --build -d
```