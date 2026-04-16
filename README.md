# progetto-professionAI-Deploy
Deploy e monitoraggio di un modello di Sentiment Analysis per recensioni.

## Descrizione del progetto
Questo repository serve un modello di Sentiment Analysis tramite una REST API FastAPI e espone metriche Prometheus per il monitoraggio.

## Cosa è stato implementato
- API REST con FastAPI
- Endpoint `POST /predict` per classificare il sentimento di una recensione
- Endpoint `GET /metrics` per esportare metriche Prometheus
- Dockerfile per containerizzare l'applicazione
- Jenkinsfile per la pipeline CI/CD
- Test automatici con `pytest`

## Struttura del repository
- `API/modelPrediction.py`: applicazione FastAPI principale
- `API/prometheusMonitoring.py`: middleware Prometheus per contare richieste e latenze
- `sentiment_analysis_model.pkl`: modello pickle usato per inferenza
- `requirements.txt`: dipendenze Python
- `Dockerfile`: immagine container per l'app
- `docker-compose.yml`: orchestrazione di API, Prometheus e Grafana
- `prometheus.yml`: configurazione Prometheus per lo scraping delle metriche
- `grafana/provisioning/`: configurazione automatica di datasource e dashboard
- `jenkinsfile`: pipeline CI/CD
- `tests/test_api.py`: test automatici
- `GRAFANA_SETUP.md`: guida completa per Grafana e testing del CI/CD
- `test-pipeline.ps1`: script per testare il pipeline su Windows
- `test-pipeline.sh`: script per testare il pipeline su Linux/macOS

## Requisiti
- Python 3.11+
- Docker (per eseguire l'immagine container)
- Jenkins (per CI/CD)

## Installazione locale
1. Crea e attiva un ambiente virtuale:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate    # Windows PowerShell
```
2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```
3. Avvia l'API:
```bash
uvicorn API.modelPrediction:app --host 0.0.0.0 --port 8000
```

## Endpoints disponibili
### POST /predict
Richiede JSON con chiave `review`.
Esempio:
```json
{
  "review": "This product is amazing! I love it."
}
```
Risposta:
```json
{
  "sentiment": "positive",
  "confidence": 0.95
}
```

### GET /metrics
Espone metriche Prometheus in formato testo.
Esempio:
```
# HELP api_requests_total Total API Requests
# TYPE api_requests_total counter
api_requests_total{method="GET",endpoint="/",http_status="200"} 1.0
```

## Eseguire i test
```bash
python -m pytest tests
```

## Eseguire con Docker
```bash
docker build -t sentiment-api:latest .
docker run -d -p 8000:8000 --name sentiment-api sentiment-api:latest
```

## Monitoraggio con Prometheus e Grafana

### Quick Start con Docker Compose
```bash
docker-compose up -d
```

Questo avvia automaticamente:
- **API**: http://localhost:8000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

La dashboard di Grafana è preconfigurata e mostra in tempo reale:
- Tasso di richieste API
- Latenza delle richieste (p95)
- Distribuzione dei tempi di risposta
- Status code delle risposte

**Nota**: Attendi 15-30 secondi perché Prometheus raccolga i primi dati.

Per la guida completa, vedi [GRAFANA_SETUP.md](GRAFANA_SETUP.md)

## CI/CD Pipeline - Testing Locale

### Quick Test su Windows PowerShell
```powershell
.\test-pipeline.ps1
```

### Quick Test su Linux/macOS
```bash
chmod +x test-pipeline.sh
./test-pipeline.sh
```

### Test Manuale (step by step)
1. Installa dipendenze: `pip install -r requirements.txt`
2. Esegui test: `python -m pytest tests/ -v`
3. Build Docker: `docker build -t sentiment-api:test .`
4. Verifica: `docker run --rm sentiment-api:test python -c "import pickle; print('✓ Model loaded')"`
5. (Opzionale) Push: `docker push <username>/sentiment-api:test`

## CI/CD
La pipeline Jenkins esegue:
1. checkout del repository
2. installazione dipendenze
3. esecuzione test
4. build dell'immagine Docker
5. push su registry Docker
6. deploy del container

**Configurazione Jenkins**: 
- Crea una new pipeline job in Jenkins
- Seleziona "Pipeline script from SCM"
- Repository URL: `https://github.com/fcitarelli/progetto-professionAI-Deploy`
- Script path: `jenkinsfile`
- Aggiungi credenziali Docker Hub (settare come `dockerhub-credentials` in Jenkins)
- Aggiorna `DOCKER_IMAGE` nel jenkinsfile con il tuo username

## Note aggiuntive
- Il modello è già presente in `sentiment_analysis_model.pkl`.
- Se vuoi usare Grafana, configura un data source Prometheus che legge `http://<host>:8000/metrics`.
- Se usi Docker Hub, sostituisci `your-dockerhub-username/ml-model` con il nome reale del tuo repository.
