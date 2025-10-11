# Jenquin.io

Personal Ops Dashboard

## Access URLs

- **Live Site**: https://jenquin813.github.io/jenquin.github.io/
- **Demo Mode**: https://jenquin813.github.io/jenquin.github.io/?demo=1

## Features

- Top 3 Today task management
- 7-Day Crash Plan
- Daily Agenda view
- Mini calendar with month navigation
- Digital clock
- Quick Add functionality
- Demo mode (via URL parameter)

| Layer | Description |
|------|-------------|
| **Backend (Private Repo)** | Handles the “thinking”: logic, scheduling, data processing, and decision-making. |
| **Frontend (`jenquin-site`)** | Handles the “feeling”: what users see, click, and experience visually. |

This separation allows for clean modular growth — keeping the system secure, adaptable, and easy to evolve over time.

## 🧭 Concept Diagram (Aligned & Consistent)
A high-level view of how **Jenquin Site** fits into the broader system with consistent, parallel labels:

```
                     ┌──────────────────────────┐
                     │        Jenquin UI        │
                     │  (jenquin-site frontend) │
                     └─────────────┬────────────┘
                                   │
                         [User Interaction Layer]
                                   │
                     ┌─────────────┴────────────┐
                     │       Voice Gateway      │
                     │    (Siri / Mic Input)    │
                     └─────────────┬────────────┘
                                   │
                           [Input Interpretation]
                                   │
                     ┌─────────────┴────────────┐
                     │       AI Assistant       │
                     │  (Nova — Router/Agent)   │
                     └─────────────┬────────────┘
                                   │
                         [Intent Routing & Orchestration]
                                   │
                     ┌─────────────┴────────────┐
                     │     Language Model(s)    │
                     │ (LLM Engine — Reasoning) │
                     └─────────────┬────────────┘
                                   │
                          [Structured Commands]
                                   │
                     ┌─────────────┴────────────┐
                     │      Jenquin Backend     │
                     │ (Data & Automation Core) │
                     └─────────────┬────────────┘
                                   │
                         [Memory & Long-Term Data]
                                   │
                     ┌─────────────┴────────────┐
                     │    FlowOS / SelfOS Stack │
                     │   (Personal System Memory)│
                     └──────────────────────────┘
```

**Alignment notes:**
- **Voice Gateway** parallels **AI Assistant** in label style (top role + subtitle in parentheses).
- **AI Assistant** is the title; **Nova** is specified as the implementation (Router/Agent).
- **Language Model(s)** mirrors this pattern (title + role in parentheses).
- **Backend** and **FlowOS** use consistent “title + role” phrasing.

## 🎯 Goals
- Present a **functional and visually clear** concept site.
- Prototype UI elements such as dashboards, top tasks, and flow navigation.
- Serve as the **public face** of the Jenquin project while backend logic develops privately.
- Evolve into a unified web or app experience that integrates voice, reminders, and adaptive interfaces.

## 🔄 Future Vision
Jenquin isn’t just a site — it’s the start of a connected ecosystem. Over time, this front-end layer will become a **gateway** into a broader platform that blends:
- **automation**
- **data awareness**
- **voice input**
- **flow-based productivity**

The goal is to make technology feel *invisible but intelligent* — helping people stay organized and in flow without needing to manage every detail manually.

## 🧰 Built With
- **HTML5 / CSS3**
- **JavaScript (Vanilla)**
- *(Optional future frameworks: React, Vue, or Svelte)*

## 🚀 Getting Started
To preview locally:
```bash
git clone https://github.com/<yourusername>/jenquin-site.git
cd jenquin-site
open index.html
```
Or view live on GitHub Pages (after enabling it in repo settings).

## 🖼️ Showcase / Screenshots (placeholder)
- `docs/screenshots/` folder for UI previews and GIFs (add when ready).
- Example sections to show later: **Reveal Crash Plan**, **Top 3 / Top 7**, **Flow Navigation**.

## 🪶 License
This project is currently under personal development and not licensed for redistribution.
Future licensing will be added once the full system architecture is ready for collaboration.
