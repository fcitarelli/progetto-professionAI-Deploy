# CI/CD Pipeline Test & Grafana Setup Guide

## Testing the CI/CD Pipeline

### Option 1: Local Testing (Windows PowerShell)
Esegui lo script per simulare l'intera pipeline CI/CD localmente:

```powershell
.\test-pipeline.ps1
```

Il script:
1. ✓ Verifica che il repository sia presente
2. ✓ Installa le dipendenze Python
3. ✓ Esegue i test automatici
4. ✓ Costruisce l'immagine Docker
5. ✓ Verifica che l'immagine sia funzionante
6. ✓ Prepara il deploy

### Option 2: Local Testing (Bash/Linux/macOS)
```bash
chmod +x test-pipeline.sh
./test-pipeline.sh
```

### Option 3: Step-by-Step Manual Testing

#### Step 1: Installa le dipendenze
```bash
pip install -r requirements.txt
```

#### Step 2: Esegui i test
```bash
python -m pytest tests/ -v
```

Aspettati output:
```
tests/test_api.py::test_health_check PASSED
tests/test_api.py::test_predict_returns_sentiment PASSED
tests/test_api.py::test_predict_empty_review PASSED
tests/test_api.py::test_metrics_endpoint PASSED

4 passed in 1.76s
```

#### Step 3: Build immagine Docker
```bash
docker build -t sentiment-api:latest .
```

#### Step 4: Test immagine Docker
```bash
docker run --rm sentiment-api:latest python -c "import pickle; print('Model loaded')"
```

#### Step 5: Push a Docker Hub
```bash
# Dopo aver fatto login
docker login

# Tagger l'immagine con il tuo username
docker tag sentiment-api:latest <your-username>/sentiment-api:latest

# Push
docker push <your-username>/sentiment-api:latest
```

## Setting Up Grafana Dashboard

### Option 1: With Docker Compose (Recommended)

#### Prerequisiti
- Docker
- Docker Compose

#### Start everything:
```bash
docker-compose up -d
```

Questo avvia:
- **Sentiment API**: http://localhost:8000
  - Health check: `GET http://localhost:8000/`
  - Predict: `POST http://localhost:8000/predict`
  - Metrics: `GET http://localhost:8000/metrics`

- **Prometheus**: http://localhost:9090
  - Scrapa le metriche dall'API ogni 15 secondi
  - Query Explorer disponibile

- **Grafana**: http://localhost:3000
  - Username: `admin`
  - Password: `admin`

#### Verifica che tutto sia running:
```bash
docker-compose ps
```

### Option 2: Manual Docker Setup

#### 1. Build and run API
```bash
docker build -t sentiment-api:latest .
docker run -d -p 8000:8000 --name sentiment-api sentiment-api:latest
```

#### 2. Run Prometheus
```bash
docker run -d \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml:ro \
  --name prometheus \
  prom/prometheus:latest
```

#### 3. Run Grafana
```bash
docker run -d \
  -p 3000:3000 \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  --name grafana \
  grafana/grafana:latest
```

### Option 3: Manual Local Setup (No Docker)

#### 1. Avvia l'API
```bash
uvicorn API.modelPrediction:app --host 0.0.0.0 --port 8000
```

#### 2. Scarica e configura Prometheus
- Scarica Prometheus da: https://prometheus.io/download/
- Copia il file `prometheus.yml` dalla repo
- Avvia: `./prometheus --config.file=prometheus.yml`
- Accedi a: http://localhost:9090

#### 3. Scarica e configura Grafana
- Scarica Grafana da: https://grafana.com/grafana/download
- Installa e avvia
- Accedi a: http://localhost:3000 (admin/admin)
- Aggiungi Prometheus come data source: http://localhost:9090

## Using the Grafana Dashboard

### Accedi a Grafana
1. Apri http://localhost:3000
2. Login: `admin` / `admin`

### La dashboard preconfigurata mostra:
- **API Requests Rate**: Numero di richieste per secondo (ultimi 5 minuti)
- **API Latency (p95)**: Tempo di risposta al 95° percentile
- **API Latency Distribution**: Distribuzione dei tempi di risposta nel tempo
- **Requests by Status Code**: Grafico a torta dei codici HTTP risposti

### Testare le metriche

#### 1. Genera traffico sull'API
```bash
# Requests positive
for i in {1..10}; do
  curl -X POST http://localhost:8000/predict \
    -H "Content-Type: application/json" \
    -d '{"review": "This is amazing!"}'
done

# Requests con errore (body vuoto)
for i in {1..5}; do
  curl -X POST http://localhost:8000/predict \
    -H "Content-Type: application/json" \
    -d '{"review": ""}'
done
```

#### 2. Verifica le metriche raw
```bash
curl http://localhost:8000/metrics
```

Dovresti vedere:
```
# HELP api_requests_total Total API Requests
# TYPE api_requests_total counter
api_requests_total{endpoint="/predict",http_status="200",method="POST"} 10.0
api_requests_total{endpoint="/predict",http_status="400",method="POST"} 5.0
```

#### 3. Visualizza in Grafana
Attendi 15-30 secondi (intervallo di scrape) e vedi i dati sulla dashboard.

## Cleanup

Per fermare e rimuovere i container:

```bash
# Con docker-compose
docker-compose down -v

# Oppure manualmente
docker stop sentiment-api prometheus grafana
docker rm sentiment-api prometheus grafana
```

## Troubleshooting

### Prometheus non scrapa le metriche
- Verifica che `prometheus.yml` abbia il target corretto
- Controlla http://localhost:9090/targets per lo stato del target

### Grafana non carica la dashboard
- Attendi che Prometheus raccolga almeno un dato (15 secondi)
- Verifica che il data source sia configurato correttamente in Grafana

### API non risponde
- Verifica che il file del modello `sentiment_analysis_model.pkl` sia presente
- Controlla i log: `docker logs sentiment-api`

## Next Steps

1. **Configurare Jenkins** per automatizzare il pipeline
2. **Aggiungere alert** in Grafana per latenze elevate
3. **Scalare orizzontalmente** con Kubernetes
4. **Implementare load balancing** per multiple API instances
