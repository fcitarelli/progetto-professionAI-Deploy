Deploy e monitoraggio di un modello di Sentiment Analysis per recensioni
Contesto aziendale
Una piattaforma di e-commerce riceve migliaia di recensioni sui prodotti ogni giorno. Analizzare il sentimento di queste recensioni (positivo, negativo, neutro) è cruciale per migliorare i prodotti e il servizio clienti. L'azienda desidera implementare un sistema automatizzato per il deploy e il monitoraggio di un modello di Sentiment Analysis, garantendo scalabilità e affidabilità.

Obiettivi del progetto
Lo studente dovrà: 1. Implementare un modello di Sentiment Analysis utilizzando un framework di Machine Learning (ad esempio TensorFlow, PyTorch o Huggingface). 2. Creare un pipeline di Continuous Integration/Continuous Deployment (CI/CD) con Jenkins per automatizzare il deploy del modello. 3. Configurare un'infrastruttura di monitoraggio utilizzando Prometheus e Grafana per registrare metriche come tempi di risposta, errore del modello e utilizzo delle risorse. 4. Documentare e gestire il progetto su un repository GitHub o GitLab.

Specifiche tecniche
1. Modello di Sentiment Analysis
Si può utilizzare il modello esposto in formato pickle disponibile a questo link: https://github.com/Profession-AI/progetti-devops/raw/refs/heads/main/Deploy%20e%20monitoraggio%20di%20un%20modello%20di%20sentiment%20analysis%20per%20recensioni/sentimentanalysismodel.pkl. Lavora su testi in lingua inglese.

Esempio di utilizzo:

import pickle
# Scaricare preliminarmente il file nella cartella corrente

filename = 'language_detection_pipeline.pkl'
loaded_pipeline = pickle.load(open(filename, 'rb'))

# Testo da prevedere (lista di stringhe)
text_to_predict = ["Questo è un testo di esempio in italiano."]

# Previsione
predicted_language = loaded_pipeline.predict(text_to_predict)
print(f"Predicted language: {predicted_language[0]}")
2. CI/CD con Jenkins
Configurare un repository GitHub o GitLab per il progetto.
Implementare uno script Jenkinsfile per automatizzare:
L’esecuzione dei test (unit test e test di integrazione).
Il deploy del modello su un server o container (ad esempio Docker o Kubernetes).
Notifiche in caso di errore o successo della pipeline.
3. Monitoraggio con Prometheus
Integrare il servizio REST API per il modello con Prometheus per raccogliere metriche:
Tempo di risposta delle richieste.
Errori di predizione.
Utilizzo della CPU e della memoria.
Configurare Grafana per visualizzare dashboard interattive basate sulle metriche raccolte.
4. API per il modello
Creare un REST API con Flask o FastAPI per servire il modello.
Endpoint richiesti:
POST /predict: accetta una recensione in formato JSON e restituisce il sentimento analizzato.
GET /metrics: espone le metriche del sistema in formato leggibile da Prometheus.
Benefici aziendali
Automazione: La pipeline CI/CD assicura che ogni modifica al modello venga testata e distribuita in modo rapido e affidabile.
Monitoraggio proattivo: Prometheus e Grafana permettono di identificare e risolvere rapidamente eventuali problemi nel modello o nel sistema.
Decisioni basate sui dati: Il modello di Sentiment Analysis fornisce insight utili per migliorare i prodotti e l’esperienza dei clienti.
Flusso del progetto
1. Pipeline CI/CD con Jenkins
Trigger automatico: La pipeline si attiva quando viene effettuato un commit nel repository.
Build: Compilazione del modello e creazione dell'immagine Docker.
Test: Esecuzione di test automatizzati per validare le previsioni del modello.
Deploy: Pubblicazione del modello su un ambiente di produzione o staging.
2. Monitoraggio
Configurare Prometheus per raccogliere metriche esposte dall’API REST.
Creare dashboard in Grafana per visualizzare in tempo reale le prestazioni del sistema.
3. Esempio di API
Richiesta
POST /predict
{
  "review": "This product is amazing! I love it."
}
Risposta
{
  "sentiment": "positive",
  "confidence": 0.95
}
Risultati attesi
Pipeline CI/CD funzionante: La pipeline deve effettuare build, test e deploy senza intervento manuale.
Modello in produzione: L’API REST deve essere attiva e rispondere correttamente alle richieste di previsione.
Dashboard di monitoraggio: Grafana deve visualizzare in tempo reale metriche chiave come tempo di risposta e utilizzo delle risorse.
Documentazione completa: Il repository GitHub o GitLab deve includere istruzioni per la configurazione, l’uso e la manutenzione del sistema.
Modalità di consegna:
File zip
