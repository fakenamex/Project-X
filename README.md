# Project-X

Autonomer KI-Newsroom mit 9 spezialisierten Agenten.

## Funktionen

- 9 KI-Agenten gemäß deiner Rollenbeschreibung
- Vollautomatische Tageszyklen nach Serverstart (keine manuellen Befehle nötig)
- Mindestens 10 Artikel pro Tag (konfigurierbar)
- Qualitäts- und EU-Compliance-Check im Workflow
- Erweiterbares Agenten-Registry-Design, damit neue Agenten leicht ergänzt werden können
- Frontend (`/`) und Backend-API (`/api/articles`)

## Start

```bash
python main.py
```

Danach:

- Homepage: `http://localhost:8080/`
- API: `http://localhost:8080/api/articles`

## Agenten

1. FrontendDeveloperAgent
2. BackendDeveloperAgent
3. ResearchSpecialistAgent
4. TextWriterAgent
5. PublisherAgent
6. QualityManagerAgent
7. MarketingManagerAgent
8. SocialMediaManagerAgent
9. CEOAgent

## Weitere Agenten hinzufügen

In `src/project_x/orchestrator.py`:

- Neue Agent-Klasse implementieren (am besten in `src/project_x/agents/team.py` oder eigener Datei)
- Mit `registry.add(DeinNeuerAgent())` registrieren
- Oder `AgentRegistry.default()` erweitern

Alle Agenten laufen dann automatisch im täglichen Zyklus mit.
