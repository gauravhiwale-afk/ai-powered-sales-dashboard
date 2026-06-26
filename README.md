📊 AI‑Powered Sales Dashboard

🔗 Live App:
https://ai-sales-intelligence-dashboard.streamlit.app/

🚀 Overview
This project is an AI-powered sales analytics dashboard that transforms raw sales data into structured KPIs and executive-level business insights.

Unlike traditional dashboards that only display charts, this system dynamically computes key performance indicators and generates AI-driven summaries that highlight strengths, risks, and recommended actions.

The objective was to bridge the gap between visualization and actionable decision-making.

🧠 Key Features

✅ Dynamic KPI computation (Revenue, Profit, Margin, Orders)

✅ Interactive filtering by Region and Category

✅ AI-generated executive insights (via Cerebras LLM)

✅ Revenue analysis by region and state

✅ Geographic visualization (US choropleth map)

✅ Smart number formatting (K / M scaling)

✅ Cloud deployment via Streamlit


🏗 System Architecture
User Filters

→ Dynamic SQL Queries (SQLite)
→ KPI Computation (Python)
→ Structured KPI Dictionary
→ Cerebras LLM
→ Executive Insight Generation
→ Interactive Dashboard (Streamlit)

Important:
All numerical calculations are deterministic and handled by SQL and Python.
The AI layer only interprets pre-calculated metrics.

🛠 Tech Stack
Python

SQL (SQLite)

Streamlit

Plotly

Cerebras API (LLM Integration)

dotenv (Secure API handling)


📈 Business Value
Traditional dashboards require manual interpretation of charts and metrics.

This system:

Automatically highlights strengths
Identifies potential risks
Suggests actionable business improvements
Reduces analysis time
Enhances decision readiness


🔒 Production Considerations
API keys managed securely via environment variables
Button-controlled AI execution to prevent rate-limit issues
Modular architecture allowing migration to scalable databases (e.g., PostgreSQL)
Stable deployment via Streamlit Cloud


👨‍💻 Author
Built as a portfolio project demonstrating:

Data analytics engineering

System architecture design

AI integration

Interactive dashboard development

Cloud deployment workflow



<img width="1920" height="1080" alt="Screenshot (137)" src="https://github.com/user-attachments/assets/c6dd26a0-5be9-4c39-939f-d360d5e58fff" />



<img width="1920" height="1080" alt="Screenshot (135)" src="https://github.com/user-attachments/assets/c3118da7-305b-4141-802f-c13c63489446" />




<img width="1920" height="1080" alt="Screenshot (136)" src="https://github.com/user-attachments/assets/bdf54be9-0bb9-4311-9f3d-4099e16d6bc1" />







