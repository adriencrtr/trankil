<p align="center">
  <img src="doc/images/trankil_logo.png" alt="Trankil logo" width="220"/>
</p>

# 🧠 Trankil

**Trankil** is a lightweight Python tool that helps you build custom multilingual **translations** **Anki decks**.  
Its main goal is to make vocabulary acquisition _trankillement_ easy and efficient by generating flashcards from user input.

## ✨ Features

- 🔁 Fetch **translations** and example usages from external APIs (Linguee.)
- 🧠 Generate fully formatted **Anki cards** with support for:
  - Multiple translations
  - Example sentences
  - Part-of-speech tagging
- 📦 Export `.apkg` decks ready to import into Anki
- ⚙️ Simple CLI or script-based usage
- 🪶 Lightweight and configurable

## 🚀 Installation

### Avec `pip` :

```bash
pip install trankil
```

### Usage
```
poetry run trankil
```

- Actions manuelles:
  - Ecrire les mots dans le fichier d'origine.
  - Gérer les erreurs à la main, correction
  - Merger les decks sur Anki

### Dev usage

To run the pytest coverage and get a report run the command:
```
poetry run pytest --cov=trankil --cov-report=html .\tests
```

##### Notes

Discutter du choix du type de carte.
Expliquer le choix sur les notes sauvegardées en json.
Détailler le choix API et les limites. Les paramètres en dur + les temps de pause.