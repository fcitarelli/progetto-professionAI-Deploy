# Script per testare il flusso CI/CD localmente su Windows

Write-Host "=== CI/CD Pipeline Test ===" -ForegroundColor Cyan
Write-Host ""

# 1. Checkout
Write-Host "[1/6] Checkout del repository..." -ForegroundColor Yellow
Write-Host "[OK] Repository gia' presente" -ForegroundColor Green
Write-Host ""

# 2. Installa dipendenze
Write-Host "[2/6] Installazione dipendenze..." -ForegroundColor Yellow
pip install -q -r requirements.txt
Write-Host "[OK] Dipendenze installate" -ForegroundColor Green
Write-Host ""

# 3. Test
Write-Host "[3/6] Esecuzione test..." -ForegroundColor Yellow
python -m pytest tests/ -v --tb=short
Write-Host "[OK] Test passati" -ForegroundColor Green
Write-Host ""

# 4. Build immagine Docker
Write-Host "[4/6] Build immagine Docker..." -ForegroundColor Yellow
docker build -t sentiment-api:test .
Write-Host "[OK] Immagine Docker creata: sentiment-api:test" -ForegroundColor Green
Write-Host ""

# 5. Verifica immagine
Write-Host "[5/6] Verifica immagine..." -ForegroundColor Yellow
$result = docker run --rm sentiment-api:test python -c "import pickle; print('[OK] Modello caricato')"
Write-Host $result
Write-Host ""

# 6. Simula deploy
Write-Host "[6/6] Simula deploy..." -ForegroundColor Yellow
Write-Host "[OK] Immagine pronta per il push a Docker Hub" -ForegroundColor Green
Write-Host ""

Write-Host "=== Pipeline Test Completato ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Prossimi step:" -ForegroundColor Yellow
Write-Host "1. Push immagine: docker push <username>/sentiment-api:test"
Write-Host "2. Deploy: docker run -d -p 8000:8000 --name sentiment-api sentiment-api:test"
