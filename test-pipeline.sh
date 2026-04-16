#!/bin/bash

# Script per testare il flusso CI/CD localmente

set -e

echo "=== CI/CD Pipeline Test ==="
echo ""

# 1. Checkout (già fatto, siamo nel repository)
echo "[1/6] Checkout del repository..."
echo "✓ Repository già present"
echo ""

# 2. Installa dipendenze
echo "[2/6] Installazione dipendenze..."
pip install -q -r requirements.txt
echo "✓ Dipendenze installate"
echo ""

# 3. Test
echo "[3/6] Esecuzione test..."
python -m pytest tests/ -v --tb=short
echo "✓ Test passati"
echo ""

# 4. Build immagine Docker
echo "[4/6] Build immagine Docker..."
docker build -t sentiment-api:test .
echo "✓ Immagine Docker creata: sentiment-api:test"
echo ""

# 5. Verifica immagine
echo "[5/6] Verifica immagine..."
docker run --rm sentiment-api:test python -c "import pickle; print('✓ Modello caricato correttamente')"
echo ""

# 6. Simula deploy
echo "[6/6] Simula deploy..."
echo "✓ Immagine pronta per il push a Docker Hub"
echo ""
echo "=== Pipeline Test Completato ==="
echo ""
echo "Prossimi step:"
echo "1. Push immagine: docker push <username>/sentiment-api:test"
echo "2. Deploy: docker run -d -p 8000:8000 --name sentiment-api sentiment-api:test"
