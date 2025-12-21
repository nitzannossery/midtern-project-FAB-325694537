# Quick Start Guide

**Note:** Use `python3` (not `python`) on macOS.

## ✅ בדיקת תקינות מהירה (10-15 דקות)

### 1) התקנת תלויות
```bash
cd "/Users/nitzannossery/Financial Analyst bot- midtern project"
python3 -m pip install -r requirements.txt
```

### 2) בדיקת ייבואים
```bash
python3 test_setup.py
```

אמור להציג:
```
✓ Orchestrator imported successfully
✓ MarketDataAgent imported successfully
✓ FundamentalNewsAgent imported successfully
✓ PortfolioRiskAgent imported successfully
✓ DataFetcher imported successfully
✓ FinancialCalculator imported successfully

✅ All imports successful!
```

### 3) הרצת UI
```bash
python3 -m streamlit run ui/app.py
```

מה צריך לראות:
- נפתח דפדפן עם ה-UI
- אין שגיאות אדומות בטרמינל/בדפדפן
- Sidebar עם Query Parameters
- כפתור "Run Analysis"

### 4) בדיקת "שאלה פשוטה" (Query Type 1)
ב-UI:
- Symbol: **AAPL**
- Risk: **moderate**
- Horizon: **12**
- לחץ **Run**

מה צריך לבדוק:
- ✓ יש פלט ל-Market Data Agent
- ✓ יש פלט ל-Fundamental & News Agent
- ✓ יש פלט ל-Portfolio & Risk Agent
- ✓ יש Final Answer ברור
- ✓ כל הטאבים עובדים

### 5) בדיקת "שאלה מורכבת" (Query Type 2)
ב-UI:
- Symbol: **TSLA**
- Risk: **conservative**
- Horizon: **24**
- לחץ **Run**

מה צריך לבדוק:
- ✓ התוצאה שונה מהשאלה הפשוטה
- ✓ Portfolio & Risk Agent מדגיש מגבלות סיכון / זהירות
- ✓ Final Answer משקף conservative profile
- ✓ Horizon של 24 חודשים נלקח בחשבון

### 6) בדיקת מבנה הפרויקט
```bash
ls -la
```

צריך לראות:
- ✓ agents/ (עם 3 קבצי agent)
- ✓ tools/ (עם data_fetcher.py ו-financial_calculator.py)
- ✓ ui/ (עם app.py)
- ✓ evaluation/ (עם ground_truth.md ו-screenshots/)
- ✓ orchestrator.py
- ✓ requirements.txt
- ✓ README.md

### 7) בדיקת שמות (טעויות נפוצות)
```bash
grep -r "portfolio" --include="*.py" --include="*.md" | grep -i "portofolio\|portfolioo"
```

אמור להיות ריק (אין שגיאות כתיב)

## 🎥 החלק שלך (אחרי הבדיקה)

### הקלטת מסך:
1. AAPL (פשוטה) → Run → להראות Output + Final Answer
2. TSLA (מורכבת) → Run → להראות Output + Final Answer
   (≤ 1:30)

### 3 צילומי מסך Evaluation:
- `evaluation/screenshots/correctness.png`
- `evaluation/screenshots/faithfulness.png`
- `evaluation/screenshots/coverage.png`

### העלאה:
- Drive + לינק GitHub

## 🐛 פתרון בעיות

### שגיאת "ModuleNotFoundError"
```bash
python3 -m pip install -r requirements.txt
```

### שגיאת "streamlit: command not found"
```bash
python3 -m pip install streamlit
```

### שגיאת ייבוא
```bash
python3 test_setup.py
```

אם יש שגיאות, בדוק ש:
- כל הקבצים קיימים
- `__init__.py` קיים ב-agents/ ו-tools/
- אין שגיאות syntax בקבצים

