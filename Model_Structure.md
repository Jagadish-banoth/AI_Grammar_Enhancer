grammar_enhancer/
│
├── app.py                     # Streamlit web app (Frontend)
├── run_all.py                  # Automated test suite (Phase 6–10)
├── main.py / pipeline.py       # Orchestrates all correction phases
│
├── src/
│   ├── __init__.py
│   |
│   ├── utils.py                # Common helper functions
│   │
│   ├── phase6_subject_verb.py  # Phase 6: Subject–Verb Agreement correction
│   ├── phase7_tense.py         # Phase 7: Tense consistency correction
│   ├── phase8_pronoun.py       # Phase 8: Pronoun reference correction
│   ├── phase9_conjunction.py   # Phase 9: Conjunction consistency correction
│   ├── phase10_articles.py     # Phase 10: Article and determiner correction
│   │
│   | 
│   └── pipeline.py             # Main orchestrator connecting all phases
│
├── tests/
│   ├── test_phase6.py          # Unit tests for Phase 6
│   ├── test_phase7.py          # Unit tests for Phase 7
│   ├── test_phase8.py
│   ├── test_phase9.py
│   ├── test_phase10.py
│   ├── test_pipeline.py        # Integration test (end-to-end)
│   └── conftest.py             # Pytest configuration
│
├── outputs/                    # Logs, reports, BLEU results
├── docs/                       # Documentation (README, Architecture)
│   ├── README.md
│   ├── ARCHITECTURE.md
│   └── USAGE.md
│
├── requirements.txt            # Dependencies
├── lt_server/                  # Optional local LanguageTool directory
│    ├── languagetool-server.jar
│   
└── venv/                       # Virtual environment
