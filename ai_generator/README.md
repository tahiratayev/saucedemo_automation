# AI Test Generator — Nasıl Çalışır

URL ver → sayfa otomatik incelenir → Claude BDD test yazar.

---

## Mimari

```
generate_tests.py (CLI)
        │
        ├── 1. PageInspector.inspect(url)
        │           └── Playwright ile sayfaya girer
        │           └── DOM'dan tüm elementleri çeker
        │           └── PageSnapshot döner
        │
        ├── 2. TestGenerator.generate(snapshot, page_name)
        │           └── Snapshot'ı Claude'a gönderir
        │           └── System prompt: "sadece JSON döndür"
        │           └── feature_file + steps_file içeren JSON alır
        │
        └── 3. FileWriter.write(page_name, feature, steps)
                    └── ai_generated/features/*.feature
                    └── ai_generated/steps/test_*_steps.py
```

---

## Agentic Adımlar — Detay

### Adım 1: DOM Extraction
```python
# page_inspector.py
inspector = PageInspector()
snapshot = inspector.inspect("https://www.saucedemo.com/inventory.html")
```
Playwright headless modda sayfaya girer.
SauceDemo sayfaları için önce login yapar (URL'den anlar).
Butonlar, input'lar, linkler, select dropdown'ları çeker.

Selector öncelik sırası (en stabil → en kırılgan):
1. `data-test` attribute → `[data-test='login-button']`
2. `id` → `#user-name`
3. `name` attribute → `input[name='username']`
4. CSS class → `button.btn_action`

### Adım 2: Snapshot → Prompt
```
URL: https://www.saucedemo.com
Title: Swag Labs
Interactive elements:
  [INPUT] 'user-name' | selector: #user-name type='text' placeholder='Username'
  [INPUT] 'password'  | selector: #password  type='password'
  [BUTTON] 'Login'    | selector: #login-button data-test='login-button'
```
Claude'a ne göndereceğimizi minimize ettik — sadece etkileşilebilir elementler,
gereksiz HTML yok. Token tasarrufu + daha iyi output kalitesi.

### Adım 3: Claude API
```python
# test_generator.py
response = httpx.post(
    "https://api.anthropic.com/v1/messages",
    json={
        "model": "claude-sonnet-4-6",
        "max_tokens": 4096,   # testler için daha fazla token gerekli
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}],
    }
)
```
max_tokens 4096 — feature + steps birlikte uzun olabilir.

### Adım 4: Dosya yazma
Üretilen dosyalar direkt `features/` ve `steps/`'e gitmiyor.
Önce `ai_generated/` klasörüne gidiyor.
Sen review edersin, beğenirsen ana klasöre taşırsın.

Bu kasıtlı — AI çıktısı her zaman review edilmeli.

---

## Kullanım

```bash
# API key .env'de olmalı: ANTHROPIC_API_KEY=sk-ant-...

# Önce preview — dosya yazmadan göster
python generate_tests.py --url https://www.saucedemo.com --name Login --preview

# Kaydet
python generate_tests.py --url https://www.saucedemo.com --name Login

# Inventory sayfası
python generate_tests.py --url https://www.saucedemo.com/inventory.html --name Inventory

# Cart sayfası (login gerekiyor, otomatik handle eder)
python generate_tests.py --url https://www.saucedemo.com/cart.html --name Cart
```

---

## Output

```
ai_generated/
├── features/
│   └── login.feature       ← review et, beğenince features/'a taşı
└── steps/
    └── test_login_steps.py ← review et, beğenince steps/'a taşı
```

---

## Maliyet

Her çalıştırma ~2000-4000 token → ~$0.01-0.02
Kullandığında .env'e key ekle, işin bitince kaldır.
