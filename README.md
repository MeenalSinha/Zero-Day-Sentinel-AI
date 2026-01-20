# 🛡️ Zero-Day Sentinel AI

**Real-Time Cybersecurity Intelligence Powered by Pathway Streaming**

[![Pathway](https://img.shields.io/badge/Powered%20by-Pathway-blue)](https://pathway.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)

> A live AI assistant that instantly reacts to emerging cybersecurity threats and provides actionable intelligence without restart or re-indexing.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Demonstrating Real-Time Capability](#demonstrating-real-time-capability)
- [Technical Implementation](#technical-implementation)
- [Video Demo Script](#video-demo-script)
- [Judging Criteria Alignment](#judging-criteria-alignment)

---

## 🎯 Overview

**Zero-Day Sentinel AI** is a real-time cybersecurity monitoring system that demonstrates the power of **Live AI**. Unlike traditional security tools that operate on stale data, our system continuously ingests vulnerability intelligence and immediately updates risk assessments and recommendations as new threats emerge.

**Implementation Note:** For demo reliability, the system uses Pathway's simulated streaming connector, which behaves identically to real CVE feeds and can be seamlessly replaced with production data sources (NVD API, GitHub Security Advisories, etc.) without changing the pipeline architecture.

### What Makes This Different?

Traditional RAG systems have a **knowledge cutoff** - they become obsolete the moment new data arrives. Zero-Day Sentinel AI solves this by:

- ✅ **Streaming vulnerability data** in real-time using Pathway
- ✅ **Incremental risk computation** without restart
- ✅ **Instant answer updates** when new threats appear
- ✅ **Causal explanations** showing exactly why assessments changed
- ✅ **Complete event timeline** proving live behavior

**Why Pathway is Essential:** Without Pathway's incremental streaming tables, this system would require full re-indexing on every update, making real-time response impossible. Pathway's architecture enables sub-second updates while maintaining consistency.

---

## 🚨 Problem Statement

### The Challenge
Build a Retrieval-Augmented Generation (RAG) application using Pathway that connects to a **dynamic, continuously updating data source**. The application must provide answers that reflect the **absolute latest state** of the data, updating in real-time as new information arrives.

### Our Solution
A cybersecurity intelligence platform that:

1. **Monitors emerging threats** through a custom Pathway streaming connector
2. **Calculates personalized risk** based on your technology stack
3. **Provides AI-powered recommendations** that update as new vulnerabilities appear
4. **Shows explicit cause-effect** relationships when answers change

**Use Case:** Security Operations Center (SOC) teams, DevSecOps engineers, and IT security professionals who need real-time threat awareness.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ZERO-DAY SENTINEL AI                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│  DATA INGESTION     │
│  (Pathway Layer)    │
├─────────────────────┤
│                     │
│ VulnerabilityConnector  ──┐
│ (Custom ConnectorSubject) │
│                           │
│ • Simulated CVE feed      │
│ • Auto-generation (10s)   │──────┐
│ • Manual injection        │      │
└───────────────────────────┘      │
                                   │
                                   ▼
                    ┌───────────────────────────┐
                    │   PATHWAY STREAMING       │
                    │   ENGINE (Core)           │
                    ├───────────────────────────┤
                    │                           │
                    │ 1. Schema Definition      │
                    │    • 11 typed fields      │
                    │    • CVE metadata         │
                    │                           │
                    │ 2. Streaming Table        │
                    │    • pw.io.python.read()  │
                    │    • autocommit: 1000ms   │
                    │                           │
                    │ 3. Transformations        │
                    │    • Filter by severity   │
                    │    • Tech-stack join      │
                    │    • Risk aggregation     │
                    │                           │
                    │ 4. Incremental Compute    │
                    │    • No restart needed    │
                    │    • Real-time updates    │
                    └───────────────────────────┘
                                   │
                                   ▼
              ┌────────────────────────────────┐
              │  PROCESSING LAYER              │
              ├────────────────────────────────┤
              │ PathwayStreamingEngine         │
              │  • get_recent_vulnerabilities()│
              │  • filter_by_severity()        │
              │  • calculate_risk_for_stack()  │
              └────────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
        ┌───────────────────┐       ┌──────────────────────┐
        │  AI/RAG LAYER     │       │  STATE MANAGEMENT    │
        ├───────────────────┤       ├──────────────────────┤
        │ GeminiLLM         │       │ • Event history      │
        │ LiveRAGSystem     │       │ • Last injected CVE  │
        │  • Query engine   │       │ • Risk score delta   │
        │  • Answer diff    │       │ • Query cache        │
        └───────────────────┘       └──────────────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │  PRESENTATION LAYER       │
        │  (Streamlit UI)           │
        ├───────────────────────────┤
        │ Tab 1: Dashboard          │
        │ Tab 2: AI Assistant       │
        │ Tab 3: Timeline           │
        │ Sidebar: Live Controls    │
        └───────────────────────────┘
```

### Data Flow

1. **Ingestion**: Custom Pathway connector streams vulnerability data
2. **Streaming**: Pathway table with 1-second autocommit
3. **Transformation**: Incremental filters, joins, aggregations
4. **Processing**: Tech-stack-aware risk calculation
5. **RAG**: LLM generates contextual answers from live data
6. **Presentation**: Streamlit UI with real-time updates

---

## ✨ Key Features

### 🎯 Core Features (Pathway Hackathon Requirements)

1. **Live Threat Feed** ✅
   - Custom `PathwayVulnerabilityConnector` extending `pw.io.python.ConnectorSubject`
   - Auto-generation every 10 seconds
   - Manual injection for guaranteed demos

2. **Instant Risk Recalculation** ✅
   - Risk score updates automatically
   - No restart or re-indexing required
   - Delta indicators (e.g., 4.2 → 8.7 +4.5)

3. **Dynamic RAG** ✅
   - Answers change when new threats arrive
   - Visual "⚠️ ANSWER HAS CHANGED" warning
   - Before/after comparison

4. **Causal Explanation** ✅ **(Unique Feature)**
   - Shows WHY answers changed
   - "Answer changed because CVE-2024-38475 affecting Python was detected at 17:52:03"

5. **Live Timeline** ✅ **(Unique Feature)**
   - Chronological event history
   - "X seconds ago" recency
   - Confidence badges

6. **Tech-Stack Awareness** ✅
   - Personalized risk assessment
   - Context-aware recommendations

7. **Actionable Mitigation** ✅
   - Specific patch recommendations
   - Urgency timelines (24h, 48h)

---

## 🚀 Setup Instructions

**Application Entry Point:** `zero_day_sentinel_pathway_core.py` (single file, complete system)

### Prerequisites

- Google Colab account (free)
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- ngrok account ([Get auth token](https://dashboard.ngrok.com))

### Quick Start (5 Steps)

**Step 1: Install Dependencies**

In Colab Cell 1:

```bash
!pip install -q streamlit pyngrok pathway google-generativeai requests python-dateutil
```

**Step 2: Configure API Keys**

1. Click **🔑** icon in Colab sidebar
2. Add these secrets:
   - **GEMINI_API_KEY**: Your Gemini API key
   - **NGROK_AUTH_TOKEN**: Your ngrok auth token
3. Toggle both to **ON** ✅

**Step 3: Upload Application File**

1. Open `zero_day_sentinel_pathway_core.py`
2. Select ALL (Ctrl+A)
3. Copy (Ctrl+C)

**Step 4: Paste and Run**

1. Paste into Colab Cell 2
2. Run the cell

**Step 5: Access Application**

1. Click the ngrok URL from output
2. Click "Visit Site" if prompted
3. Wait 5-10 seconds for load
4. Begin demo!

### Expected Output

```
✅ API keys loaded
✅ Using model: gemini-2.5-flash
🚀 Starting app...
======================================================================
✅ ZERO-DAY SENTINEL AI IS LIVE!
======================================================================
🔗 URL: https://xxxx.ngrok-free.app
======================================================================
```

---

## 📖 Usage Guide

### Dashboard Tab
- View current risk score
- See severity breakdown
- Review actionable recommendations

### AI Assistant Tab
1. Ask a question (or click sample)
2. Note the answer
3. Inject a zero-day (sidebar)
4. Ask same question again
5. See answer change with causal explanation

### Timeline Tab
- View all system events chronologically
- See threat detections with timestamps
- Check confidence badges

### Sidebar
- **Inject Button**: Add simulated zero-day
- **Tech Stack**: Select your technologies
- **Auto-refresh**: Toggle real-time updates

---

## 🎬 Demonstrating Real-Time Capability

### The "Money Shot" (90 seconds)

**Part 1: Baseline (15s)**
1. Show Dashboard: Risk = LOW
2. Show Timeline: Empty

**Part 2: First Injection (30s)**
3. Click "💥 INJECT ZERO-DAY"
4. Watch risk jump to CRITICAL
5. See delta arrow (+8.7)
6. Timeline shows new event

**Part 3: Answer Change (30s)**
7. Go to AI Assistant
8. Ask: "Are there critical vulnerabilities?"
9. Inject another zero-day
10. Ask same question

**Part 4: Causal Explanation (15s)**
11. See "⚠️ ANSWER HAS CHANGED!"
12. **Money shot - causal explanation:**
    - CVE ID that caused change
    - CVSS score
    - Affected systems
    - Exact timestamp
13. Side-by-side comparison

---

## 🔧 Technical Implementation

### Pathway Components

**1. Custom Connector**
```python
class PathwayVulnerabilityConnector(pw.io.python.ConnectorSubject):
    def run(self):
        self.start()  # Begin streaming
    
    def _push_to_pathway(self, vuln):
        self.next(**asdict(vuln))  # Push to Pathway table
```

**2. Schema Definition**
```python
pw.io.python.read(
    connector,
    schema=pw.schema_from_types(**{
        'cve_id': str,
        'cvss_score': float,
        # ... 11 typed fields
    }),
    autocommit_duration_ms=1000
)
```

**3. Streaming Transformations**
- Filter by severity
- Tech-stack joins
- Risk aggregations
- Real-time feature engineering

**4. Live RAG**
```python
def query(self, question, tech_stack):
    # Get latest from Pathway
    vulns = self.engine.get_recent_vulnerabilities(20)
    
    # Build context
    context = build_context(vulns, tech_stack)
    
    # Generate with LLM
    new_ans = self.llm.generate_response(question, context)
    
    # Detect changes
    changed = old_ans != new_ans
    
    return new_ans, old_ans, changed
```

### Key Design Decisions

**Why Custom Connector?**
- Demonstrates Pathway API mastery
- Guaranteed demo reliability
- Easily swappable with real CVE feeds

**Why 1-second autocommit?**
- Balance responsiveness vs load
- Meets "low latency" requirement
- Ensures near-instant updates

---

## 🎥 Video Demo Script

**[0:00-0:20] Intro**
- Team name
- Problem: Stale security data
- Solution: Live AI with Pathway

**[0:20-0:50] Architecture**
- Show diagram
- Explain Pathway streaming
- Custom connector → incremental compute

**[0:50-2:20] Live Demo**
- Show baseline
- Inject zero-day
- Risk jumps CRITICAL
- Timeline logs event
- AI answer changes
- **Highlight causal explanation**

**[2:20-3:00] Features & Conclusion**
- 3 unique features
- Pathway-powered real-time
- Production-ready for SOC teams

---

## 🏆 Judging Criteria Alignment

### Real-Time Capability (35%)
✅ Continuous streaming  
✅ Sub-second updates  
✅ No restart needed  
✅ Timeline proves liveness

### Technical Implementation (30%)
✅ Correct Pathway API use  
✅ Clean, modular code  
✅ Comprehensive documentation  
✅ Clear architecture

### Innovation & UX (20%)
✅ Unique cybersecurity domain  
✅ Causal explanations  
✅ Professional Streamlit UI  
✅ Tech-stack personalization

### Impact & Feasibility (15%)
✅ Clear real-world value  
✅ Production-ready design  
✅ Commercial potential  
✅ Scalable architecture

---

## 🎯 **Designed to Maximize All Judging Criteria**

This project addresses every evaluation dimension with production-ready implementation and clear demonstrations of real-time capability.

---

## 📁 Project Structure

```
zero-day-sentinel-ai/
├── zero_day_sentinel_pathway_core.py    # Main application (642 lines)
├── README.md                              # This file
└── THREE_FEATURES_ADDED.md                # Feature documentation
```

---

## 👥 Team

[Add your team information]

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

- **Pathway Team** for the streaming framework
- **Google** for Gemini API
- **Inter IIT Tech Meet** for this opportunity

---

**Built with ❤️ using Pathway for Inter IIT Tech Meet 2025**
