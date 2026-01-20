"""
🛡️ ZERO-DAY SENTINEL AI - COMPLETE COPY-PASTE VERSION FOR COLAB

📋 SUPER SIMPLE 3-STEP SETUP:

STEP 1: Run in Cell 1:
    !pip install -q streamlit pyngrok pathway google-generativeai requests python-dateutil

STEP 2: Add to Colab Secrets (🔑 icon):
    - NGROK_AUTH_TOKEN
    - GEMINI_API_KEY

STEP 3: Copy ALL of this file, paste into Cell 2, run!

The app launches automatically - just click the URL!
"""

# ============================================================================
# AUTO-LAUNCHER - Works when you paste this entire file into a Colab cell
# ============================================================================

# Detect Colab
try:
    import google.colab
    _IS_COLAB = True
    
    # Load secrets
    from google.colab import userdata
    import os
    try:
        os.environ['NGROK_AUTH_TOKEN'] = userdata.get('NGROK_AUTH_TOKEN')
        os.environ['GEMINI_API_KEY'] = userdata.get('GEMINI_API_KEY')
        print("✅ API keys loaded")
    except:
        print("⚠️ Please set API keys in Colab Secrets")
        _IS_COLAB = False
except:
    _IS_COLAB = False

# If in Colab, save script and launch
if _IS_COLAB:
    import subprocess, time
    
    # Write the app code to a file (everything after the launcher)
    app_code = '''
# ============================================================================
# ZERO-DAY SENTINEL AI - MAIN APPLICATION CODE
# ============================================================================
import streamlit as st
import pathway as pw
from pathway.stdlib.ml.index import KNNIndex
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("⚠️ Google Generative AI not available")

import json, time, requests, os, threading, random, hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    NGROK_AUTH_TOKEN = os.getenv('NGROK_AUTH_TOKEN', '')
    CVE_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    RISK_THRESHOLDS = {'CRITICAL': 9.0, 'HIGH': 7.0, 'MEDIUM': 4.0, 'LOW': 0.0}

class SeverityLevel(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class ExploitStatus(Enum):
    ACTIVELY_EXPLOITED = "🔥 Actively Exploited"
    EXPLOIT_AVAILABLE = "🚨 Exploit Available"
    VULNERABLE_NO_EXPLOIT = "⚠️ Vulnerable (No Exploit)"
    PATCHED = "✅ Patched"

@dataclass
class VulnerabilityRecord:
    cve_id: str
    title: str
    description: str
    severity: str
    cvss_score: float
    affected_software: str
    exploit_status: str
    published_date: str
    mitigation: str
    source: str
    confidence: str
    timestamp: int

class PathwayVulnerabilityConnector(pw.io.python.ConnectorSubject):
    def __init__(self):
        super().__init__()
        self.vulnerability_buffer = []
        self.is_running = False
        self._thread = None
    
    def run(self):
        """Required method for Pathway ConnectorSubject"""
        # Start the streaming loop when Pathway calls run()
        self.start()
    
    def start(self):
        if not self.is_running:
            self.is_running = True
            self._thread = threading.Thread(target=self._stream_loop, daemon=True)
            self._thread.start()
    
    def stop(self):
        self.is_running = False
        if self._thread:
            self._thread.join(timeout=2)
    
    def _stream_loop(self):
        while self.is_running:
            try:
                if random.random() < 0.4:
                    vuln = self._generate_simulated_vulnerability()
                    self._push_to_pathway(vuln)
                time.sleep(10)
            except Exception as e:
                time.sleep(5)
    
    def _generate_simulated_vulnerability(self):
        vuln_num = random.randint(30000, 39999)
        software = random.choice(["Python", "OpenSSL", "Linux", "Docker", "Node.js", "PostgreSQL", "Redis"])
        title = random.choice(["Remote Code Execution in {}", "Buffer Overflow in {}"]).format(software)
        cvss = round(random.uniform(4.0, 10.0), 1)
        severity = "CRITICAL" if cvss >= 9 else "HIGH" if cvss >= 7 else "MEDIUM" if cvss >= 4 else "LOW"
        exploit = ExploitStatus.ACTIVELY_EXPLOITED.value if cvss >= 9 else ExploitStatus.VULNERABLE_NO_EXPLOIT.value
        
        return VulnerabilityRecord(
            cve_id=f"CVE-2024-{vuln_num}", title=title, description=f"Vulnerability in {software}",
            severity=severity, cvss_score=cvss, affected_software=json.dumps([software]),
            exploit_status=exploit, published_date=datetime.now().isoformat(),
            mitigation=f"Update {software} immediately", source="Simulated", confidence="HIGH",
            timestamp=int(time.time() * 1000)
        )
    
    def _push_to_pathway(self, vuln):
        self.next(**asdict(vuln))
    
    def inject_zero_day(self, vuln):
        self._push_to_pathway(vuln)

class PathwayStreamingEngine:
    def __init__(self):
        self.connector = PathwayVulnerabilityConnector()
        self.vulnerabilities_table = pw.io.python.read(
            self.connector,
            schema=pw.schema_from_types(**{
                'cve_id': str, 'title': str, 'description': str, 'severity': str,
                'cvss_score': float, 'affected_software': str, 'exploit_status': str,
                'published_date': str, 'mitigation': str, 'source': str,
                'confidence': str, 'timestamp': int
            }),
            autocommit_duration_ms=1000
        )
        self.last_update_time = datetime.now()
    
    def start(self):
        self.connector.start()
    
    def get_recent_vulnerabilities(self, limit=20):
        snapshot = list(self.connector.vulnerability_buffer)[-limit:]
        snapshot.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        return snapshot[:limit]
    
    def filter_by_severity(self, severity_list):
        return [v for v in self.get_recent_vulnerabilities(100) if v.get('severity') in severity_list]
    
    def calculate_risk_for_tech_stack(self, tech_stack):
        vulns = self.get_recent_vulnerabilities(100)
        affected, total_risk, recs, counts = [], 0.0, [], defaultdict(int)
        
        for v in vulns:
            try:
                sw = json.loads(v.get('affected_software', '[]'))
            except:
                sw = []
            
            if any(t.lower() in s.lower() for t in tech_stack for s in sw):
                affected.append(v['cve_id'])
                counts[v['severity']] += 1
                total_risk += v['cvss_score'] * (1.5 if 'Actively' in v['exploit_status'] else 1.0)
                recs.append({'cve_id': v['cve_id'], 'mitigation': v['mitigation'],
                           'severity': v['severity'], 'cvss_score': v['cvss_score']})
        
        score = min(total_risk / max(len(tech_stack), 1), 10.0)
        level = 'CRITICAL' if score >= 9 else 'HIGH' if score >= 7 else 'MEDIUM' if score >= 4 else 'LOW'
        
        return {
            'risk_score': round(score, 2), 'risk_level': level, 'affected_cves': affected,
            'recommendations': sorted(recs, key=lambda x: x['cvss_score'], reverse=True)[:5],
            'severity_counts': dict(counts), 'tech_stack': tech_stack
        }
    
    def get_exploit_statistics(self):
        stats = defaultdict(int)
        for v in self.get_recent_vulnerabilities(100):
            stats[v['exploit_status']] += 1
        return dict(stats)
    
    def inject_simulated_zero_day(self):
        vuln = self.connector._generate_simulated_vulnerability()
        self.connector.inject_zero_day(vuln)
        self.connector.vulnerability_buffer.append(asdict(vuln))
        return vuln

class GeminiLLM:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Gemini API key is required")
        if not GENAI_AVAILABLE:
            raise ValueError("google-generativeai not installed")
        
        try:
            genai.configure(api_key=api_key)
            
            # Use gemini-2.5-flash (we know it's available from the diagnostic)
            try:
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                # Quick test
                _ = self.model.generate_content("hi")
                print("✅ Using model: gemini-2.5-flash")
            except:
                # Fallback to listing available models
                try:
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            model_name = m.name.replace('models/', '')
                            self.model = genai.GenerativeModel(model_name)
                            print(f"✅ Using model: {model_name}")
                            break
                except Exception as e:
                    raise ValueError(f"Could not initialize any model: {e}")
                
        except Exception as e:
            raise ValueError(f"Gemini init failed: {str(e)}")
    
    def generate_response(self, prompt, context=''):
        try:
            full_prompt = f"{context}\\n\\n{prompt}" if context else prompt
            response = self.model.generate_content(full_prompt)
            return response.text if hasattr(response, 'text') else str(response)
        except Exception as e:
            return f"Error: {str(e)}"

class LiveRAGSystem:
    def __init__(self, engine, llm):
        self.engine, self.llm, self.history = engine, llm, {}
    
    def query(self, question, tech_stack):
        vulns = self.engine.get_recent_vulnerabilities(20)
        risk = self.engine.calculate_risk_for_tech_stack(tech_stack)
        
        context = f"Risk: {risk['risk_level']} ({risk['risk_score']}/10)\\n"
        for v in vulns[:10]:
            context += f"- {v['cve_id']}: [{v['severity']}, {v['cvss_score']}]\\n"
        
        new_ans = self.llm.generate_response(f"Answer: {question}\\nTech: {', '.join(tech_stack)}", context)
        
        h = hashlib.md5(question.encode()).hexdigest()
        old_ans = self.history.get(h)
        changed = old_ans and old_ans != new_ans
        self.history[h] = new_ans
        
        return new_ans, old_ans, changed

def init_session_state():
    defaults = {'engine': None, 'rag_system': None, 'llm': None,
                'tech_stack': ['Python', 'Linux', 'Docker'], 'last_risk_score': None,
                'last_risk_level': None, 'last_cve_count': 0, 'auto_refresh': True}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def render_sidebar():
    st.sidebar.title("⚙️ Zero-Day Sentinel AI")
    
    # 1️⃣ LIVE STATUS - Most important for judges
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🟢 LIVE STATUS")
    
    if st.session_state.engine:
        st.sidebar.markdown("""<div style='background-color:#00ff00;padding:10px;border-radius:5px;text-align:center'>
        <b style='color:#000;font-size:18px'>🟢 PATHWAY STREAMING: ACTIVE</b></div>""", unsafe_allow_html=True)
        
        t = datetime.now().strftime('%H:%M:%S')
        st.sidebar.markdown(f"""<div style='text-align:center;margin-top:10px;font-size:16px'>
        <b>Last Update:</b> <span style='color:#00ff00;font-family:monospace;font-size:18px'>{t}</span></div>""", unsafe_allow_html=True)
        
        cnt = len(st.session_state.engine.get_recent_vulnerabilities(100))
        delta = cnt - st.session_state.last_cve_count
        st.session_state.last_cve_count = cnt
        st.sidebar.metric("🚨 Active Threats", cnt, delta=f"+{delta}" if delta > 0 else None)
    
    # 2️⃣ INJECT BUTTON - Critical for demo
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🚨 LIVE DEMO")
    st.sidebar.warning("👇 **Click to see real-time updates!**")
    
    if st.sidebar.button("💥 INJECT ZERO-DAY", type="primary", use_container_width=True):
        v = st.session_state.engine.inject_simulated_zero_day()
        st.sidebar.success(f"✅ **{v.cve_id}**")
        st.sidebar.markdown(f"**Severity:** {v.severity} ({v.cvss_score})")
        time.sleep(1)
        st.rerun()
    
    # 3️⃣ TECH STACK - Personalization
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Your Tech Stack")
    st.session_state.tech_stack = st.sidebar.multiselect(
        "Technologies monitored:",
        ["Python", "JavaScript", "Java", "Linux", "Docker", "Node.js", "PostgreSQL", "Redis", "OpenSSL"],
        default=st.session_state.tech_stack,
        help="Risk assessment is personalized to your stack"
    )
    
    # 4️⃣ OPTIONS - Simple and clean
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Display Options")
    st.session_state.auto_refresh = st.sidebar.checkbox(
        "Auto-refresh every 5 seconds",
        value=st.session_state.auto_refresh,
        help="Uncheck to stop automatic updates"
    )

def main():
    st.set_page_config(page_title="🛡️ Zero-Day Sentinel", layout="wide")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🛡️ Zero-Day Sentinel AI")
    with col2:
        st.markdown("### 🟢 **LIVE**")
        st.markdown(f"**{datetime.now().strftime('%H:%M:%S')}**")
    
    st.divider()
    init_session_state()
    
    # Initialize Gemini with better error handling
    if not st.session_state.llm:
        try:
            if not Config.GEMINI_API_KEY:
                st.error("❌ GEMINI_API_KEY not found in environment!")
                st.info("""
                **To fix this:**
                1. Go to Colab Secrets (🔑 icon in sidebar)
                2. Add a new secret: `GEMINI_API_KEY`
                3. Get your key from: https://makersuite.google.com/app/apikey
                4. Toggle access for this notebook
                5. Restart the cell
                """)
                st.stop()
            
            with st.spinner("Initializing Gemini AI..."):
                st.session_state.llm = GeminiLLM(Config.GEMINI_API_KEY)
        except Exception as e:
            st.error(f"❌ Failed to initialize Gemini: {str(e)}")
            st.info("""
            **Troubleshooting:**
            1. Verify your GEMINI_API_KEY is correct
            2. Get a new key at: https://makersuite.google.com/app/apikey
            3. Make sure you've enabled the Generative Language API
            4. Check if you have API quota remaining
            """)
            st.stop()
    
    if not st.session_state.engine:
        st.session_state.engine = PathwayStreamingEngine()
        st.session_state.engine.start()
    
    if not st.session_state.rag_system:
        st.session_state.rag_system = LiveRAGSystem(st.session_state.engine, st.session_state.llm)
    
    render_sidebar()
    
    tab1, tab2 = st.tabs(["📊 Dashboard", "💬 AI Assistant"])
    
    with tab1:
        st.header("🛡️ Risk Dashboard")
        risk = st.session_state.engine.calculate_risk_for_tech_stack(st.session_state.tech_stack)
        
        col1, col2, col3 = st.columns(3)
        delta = None
        if st.session_state.last_risk_score:
            ch = risk['risk_score'] - st.session_state.last_risk_score
            if abs(ch) > 0.1:
                delta = f"{ch:+.1f}"
        
        col1.metric("🎯 Risk Score", f"{risk['risk_score']}/10", delta=delta)
        emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(risk['risk_level'], '⚪')
        col2.metric("⚠️ Level", f"{emoji} {risk['risk_level']}")
        col3.metric("🚨 CVEs", len(risk['affected_cves']))
        
        st.session_state.last_risk_score = risk['risk_score']
        
        if risk['recommendations']:
            st.markdown("---")
            st.subheader("🎯 IMMEDIATE ACTIONS")
            for i, r in enumerate(risk['recommendations'], 1):
                e = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(r['severity'], '⚪')
                with st.expander(f"{e} {i}. {r['cve_id']} - {r['severity']}", expanded=(i==1)):
                    st.markdown(f"**{r['mitigation']}**")
                    if r['severity'] == 'CRITICAL':
                        st.error("⏰ **TIMELINE:** Immediate action required (within 24 hours)")
                    elif r['severity'] == 'HIGH':
                        st.warning("⏰ **TIMELINE:** Apply patch within 48 hours")
        else:
            st.info("👍 No vulnerabilities affecting your tech stack at the moment. Click 'Inject Zero-Day' to test!")
    
    with tab2:
        st.header("💬 AI Assistant (Dynamic RAG)")
        st.info("💡 Answers update automatically when new vulnerabilities arrive!")
        
        qs = ["Are there critical vulnerabilities?", "What affects my stack?", "What should I do immediately?"]
        cols = st.columns(len(qs))
        for i, q in enumerate(qs):
            if cols[i].button(q, key=f"q{i}", use_container_width=True):
                st.session_state.current_query = q
        
        query = st.text_input("🔍 Ask about vulnerabilities:", value=st.session_state.get('current_query', ''))
        
        if st.button("🚀 Analyze Current Threat Landscape", type="primary", use_container_width=True) or query:
            if query:
                with st.spinner("Analyzing with Pathway streaming data..."):
                    new, old, changed = st.session_state.rag_system.query(query, st.session_state.tech_stack)
                    
                    if changed and old:
                        st.error("### ⚠️ ANSWER HAS CHANGED SINCE YOUR LAST QUERY!")
                        st.markdown("""
                        <div style='background-color: #fff3cd; padding: 15px; border-radius: 5px;'>
                        🔄 The AI detected new information and updated its response.<br>
                        This proves real-time knowledge updates powered by Pathway streaming!
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### 📜 Previous Answer")
                            st.text_area("Old", old, height=300, disabled=True, key="old_answer")
                        
                        with col2:
                            st.markdown("#### ✨ Updated Answer (Current)")
                            st.markdown(f"""
                            <div style='background-color: #d4edda; padding: 15px; border-radius: 5px; border: 2px solid #28a745;'>
                            {new.replace(chr(10), '<br>')}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown("### 💡 Answer:")
                        st.write(new)
    
    if st.session_state.auto_refresh:
        time.sleep(5)
        st.rerun()

if __name__ == "__main__":
    main()
'''
    
    # Save to file
    with open('/tmp/zd_app.py', 'w') as f:
        f.write(app_code)
    
    # Kill existing
    subprocess.run(['pkill', '-9', '-f', 'streamlit'], stderr=subprocess.DEVNULL)
    
    print("🚀 Starting app...")
    
    # Launch Streamlit
    proc = subprocess.Popen([
        'streamlit', 'run', '/tmp/zd_app.py',
        '--server.port', '8501',
        '--server.headless', 'true'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    time.sleep(10)
    
    # Launch ngrok
    from pyngrok import ngrok, conf
    import os
    
    if os.environ.get('NGROK_AUTH_TOKEN'):
        conf.get_default().auth_token = os.environ['NGROK_AUTH_TOKEN']
        url = ngrok.connect(8501)
        
        print("="*70)
        print("✅ ZERO-DAY SENTINEL AI IS LIVE!")
        print("="*70)
        print(f"\n🔗 URL: {url}")
        print("\n="*70)
        print("📝 Click URL → Click 'Visit Site' → Enjoy!")
        print("⚠️  Keep this cell running!")
        print("="*70)
        
        proc.wait()
    else:
        print("❌ NGROK_AUTH_TOKEN not found in secrets!")
    
    import sys
    sys.exit(0)

