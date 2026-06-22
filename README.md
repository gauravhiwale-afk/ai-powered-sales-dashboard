📊 AI‑Powered Sales Dashboard

🔗 Live App:
https://ai-sales-intelligence-dashboard.streamlit.app/

🚀 Project Overview
This project is an AI-powered sales analytics dashboard that transforms raw sales data into structured KPIs and executive-level business insights.

Unlike traditional dashboards that only display charts, this system dynamically calculates key performance indicators and generates AI-driven summaries that highlight strengths, risks, and recommended actions.

The goal was to bridge the gap between data visualization and actionable business intelligence.

🧠 Key Features

✅ Dynamic KPI computation (Revenue, Profit, Margin, Orders)

✅ Interactive filtering by Region and Category

✅ AI-generated executive insights

✅ Geographic revenue visualization (US map)

✅ Automatic number formatting (K / M scaling)

✅ Error-handled AI integration

✅ Cloud deployment via Streamlit

🏗 Architecture
User Filters
→ Dynamic SQL Queries (SQLite)
→ KPI Computation (Python)
→ Structured KPI Dictionary
→ Gemini LLM
→ Executive Insight Generation
→ Interactive Dashboard (Streamlit)

Important:
All calculations are deterministic and handled by SQL and Python.
The AI layer only interprets pre-calculated metrics.

🛠 Tech Stack

Python

SQL (SQLite)

Streamlit

Plotly

Gemini API (LLM Integration)

dotenv (Secure API handling)

📈 Business Value
Traditional dashboards require manual interpretation.

This system:
Automatically identifies strengths

Flags potential risks

Suggests business actions

Reduces analysis time

Improves decision readiness

🔒 Production Considerations
API keys handled securely using environment variables
Error handling prevents AI failures from crashing the app
Modular structure allows migration to scalable databases (e.g., PostgreSQL)


🎯 Author
Built as a portfolio project demonstrating:

Data analytics

System architecture

AI integration

Dashboard development

Deployment workflow
