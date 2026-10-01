# Digital Twin

Un chatbot che risponde al posto mio a chi vuole sapere qualcosa sul mio percorso: esperienze, competenze tecniche, progetti, interessi. L'ho pensato per recruiter e contatti professionali che arrivano sul mio profilo e vogliono farsi un'idea senza aspettare una mia risposta.

Demo: https://twin-zdpe.onrender.com/ (al primo accesso può servire un minuto, il servizio gratuito si "addormenta")

## Come funziona

Il modello (OpenAI, `gpt-5.4-mini` di default) riceve un prompt di sistema costruito con due file di testo:

- `summary.txt`: chi sono, in breve, anche fuori dal lavoro
- `technical.txt`: profilo professionale dettagliato, ruoli, tecnologie, progetti

Il prompt (`context.py`) fissa regole precise. Il twin dice di essere un'AI e non finge di essere me. Non inventa esperienze o certificazioni che non sono nei file, e se non sa una cosa lo dice.

Il modello ha a disposizione due strumenti (function calling):

- `record_user_details`: quando un visitatore lascia la sua email per essere ricontattato
- `record_unknown_question`: quando arriva una domanda a cui il twin non sa rispondere

Entrambi mi mandano una notifica sul telefono tramite [ntfy.sh](https://ntfy.sh). Così so chi vuole contattarmi e quali informazioni mancano nei file. Se il modello chiede di usare uno strumento, `app.py` lo esegue, gli restituisce il risultato e chiede di nuovo la risposta, finché non ne arriva una di testo.

L'invio delle notifiche ritenta da solo in caso di errori di rete. Un errore di uno strumento viene restituito al modello come messaggio, senza far cadere la chat.

## Avvio in locale

```bash
cp .env.example .env     # OPENAI_API_KEY e, se vuoi le notifiche, NTFY_TOPIC
uv venv && uv pip install -r requirements.txt
uv run app.py
```

Per ricevere le notifiche installa l'app ntfy e iscriviti allo stesso topic messo in `NTFY_TOPIC`. Scegli un nome lungo e difficile da indovinare: sul server pubblico chi conosce il topic può leggere i messaggi.

Test: `uv pip install -r requirements-dev.txt` e poi `pytest`.

## File

```
app.py         interfaccia Gradio e ciclo di chiamate al modello
context.py     prompt di sistema, costruito da summary.txt e technical.txt
tools.py       strumenti del modello e notifiche ntfy
styles.py      CSS, script ed esempi dell'interfaccia
summary.txt    presentazione personale
technical.txt  profilo professionale
```

Per adattarlo a un'altra persona basta riscrivere `summary.txt`, `technical.txt` e i nomi in `context.py`.
