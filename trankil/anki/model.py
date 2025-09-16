import genanki

my_model = genanki.Model(
    1154577639,
    "trankil model",
    fields=[{"name": "Front"}, {"name": "Back"}],
    templates=[{"name": "trankil card", "qfmt": "{{Front}}", "afmt": "{{Back}}"}],
    css="""
.card {
  font-family: Arial;
  font-size: 18px;
  text-align: left;
  color: #333;
  background-color: #f8f9fa;
  padding: 20px;
}

.word {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 12px;
}

.type_word {
  font-style: italic;
  font-size: 18px;
  color: #555;
}

.group {
  margin-bottom: 16px;
}

.translation_title {
  font-weight: bold;
  font-style: italic;
  color: #888;
  margin-bottom: 6px;
}

.meaning {
  font-weight: bold;
  color: #007bff;
  margin-bottom: 5px;
}

ul {
  list-style-type: disc;
  margin-left: 20px;
}

i {
  color: #666;
}
""",
)
