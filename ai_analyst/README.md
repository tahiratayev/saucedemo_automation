# AI Analyst — Nasıl Çalışır

Bu katman, test failure'larını otomatik olarak Claude API ile analiz eder.
Her fail olan test için root cause ve fix önerisi üretir.

---

## Mimari

```
conftest.py
    └── pytest_configure()
            └── AIAnalystPlugin() register edilir
                        │
                        ▼
            pytest_runtest_logreport()  ← her test sonrası çalışır
                        │
                    fail mi?
                    /       \
                 EVET        HAYIR → hiçbir şey yapma
                   │
                   ▼
            FailureContext oluştur
            (test adı, dosya, hata, traceback)
                   │
                   ▼
            TestFailureAnalyzer.analyze()
            → Claude API'ye gönder
            → JSON cevap al
                   │
                   ▼
            AnalysisResult
            (root_cause, fix_suggestion, confidence)
                   │
                   ├── terminal'e inline yazdır
                   └── AnalysisReport.add()
                               │
                               ▼
                   pytest_sessionfinish()
                   → reports/ai_analysis/*.json
                   → reports/ai_analysis/*.md
```

---

## Dosyalar

| Dosya | Görevi |
|-------|--------|
| `analyzer.py` | Claude API ile konuşur, FailureContext → AnalysisResult |
| `pytest_plugin.py` | pytest hook'larını dinler, failure tetiklenince analiz başlatır |
| `report.py` | Sonuçları JSON ve Markdown olarak kaydeder |

---

## Agentic Adımlar — Detay

### Adım 1: Hook — failure tespiti
```python
# pytest_plugin.py
def pytest_runtest_logreport(self, report):
    if report.when != "call" or not report.failed:
        return
    self._analyze_failure(report)
```
pytest her test phase'inden sonra bu hook'u çağırır.
Sadece `call` (testin kendisi) ve `failed` olanları filtreler.
Setup/teardown hataları ve geçen testler atlanır.

### Adım 2: Context toplama
```python
# pytest_plugin.py → _analyze_failure()
context = FailureContext(
    test_name=test_name,
    test_file=test_file,
    error_message=error_message,
    traceback=traceback_text[:3000],  # token tasarrufu için kırpılır
    feature=feature,
    scenario=scenario,
)
```
Traceback 3000 karakterde kesilir — ilk 3000 karakter genellikle yeterli,
geri kalanı Claude'a gönderilince gereksiz token harcar.

### Adım 3: Claude API çağrısı
```python
# analyzer.py → analyze()
response = httpx.post(
    "https://api.anthropic.com/v1/messages",
    json={
        "model": "claude-sonnet-4-6",
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,   # ← kritik: sadece JSON döndür
        "messages": [{"role": "user", "content": prompt}],
    }
)
```
System prompt Claude'u kısıtlar: sadece JSON döndür, preamble yok,
markdown yok. Bu olmadan parse etmek zorlaşır.

### Adım 4: JSON parse + fallback
```python
# analyzer.py
try:
    parsed = json.loads(raw)
except json.JSONDecodeError:
    # Model bazen backtick ekler — regex ile JSON'u çıkar
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    parsed = json.loads(match.group()) if match else fallback
```
Claude bazen ```json ... ``` wrapper ekler.
Fallback bu durumu handle eder — plugin asla crash etmez.

### Adım 5: Inline çıktı + rapor
```
────────────────────────────────────────────────────
🤖 AI Analysis — test_wrong_url_assertion
   🟢 Root cause: Login adımı eksik...
   💡 Fix: page.fill('#user-name', ...) ...
────────────────────────────────────────────────────
```
Terminal'de her failure'ın hemen altında görünür.
Session sonunda `reports/ai_analysis/` klasörüne kaydedilir.

---

## Çalıştırma

```bash
# .env içinde ANTHROPIC_API_KEY olmalı
pytest --tb=short

# Sadece belirli testleri analiz ettirmek için
pytest -m smoke --tb=short

# API key yoksa plugin sessizce devre dışı kalır
# ⚠️ AI Test Analyst: disabled (set ANTHROPIC_API_KEY to enable)
```

---

## Raporlar

```
reports/
└── ai_analysis/
    ├── analysis_20260625_204354.json   ← makine okunabilir (CI için)
    └── analysis_20260625_204354.md     ← insan okunabilir (GitHub'da render olur)
```

JSON formatı:
```json
[
  {
    "test_name": "test_wrong_url_assertion",
    "root_cause": "Login adımı eksik...",
    "fix_suggestion": "page.fill('#user-name', ...",
    "confidence": "high"
  }
]
```

---

## Neden Bu Yaklaşım

Klasik flow: test fail → log'a bak → hatayı analiz et → fix yaz → 5-15 dk
Bu flow:    test fail → AI analiz → root cause + fix → 10 saniye

Sabah CI'dan 3 fail geldiğinde, her birinin yanında hazır analiz var.
Log açmadan, IDE'ye geçmeden neyin yanlış gittiğini anlarsın.
