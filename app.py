import gradio as gr
import whisper
import uuid
from datetime import datetime


# =========================================================
# JANBAK AI — Speech Recognition Model
# =========================================================

model = whisper.load_model("tiny")


# =========================================================
# Incident Analysis
# =========================================================

def analyze_incident(text):
    text_lower = text.lower()

    if any(word in text_lower for word in [
        "fire", "burning", "smoke", "flames", "explosion"
    ]):
        return (
            "FIRE / EMERGENCY",
            "CRITICAL",
            "Emergency Response Authority",
            "Immediate emergency response recommended."
        )

    elif any(word in text_lower for word in [
        "attack", "weapon", "gun", "shooting",
        "threat", "bomb", "terror"
    ]):
        return (
            "SECURITY THREAT",
            "HIGH",
            "Security Authority",
            "Immediate verification and security response recommended."
        )

    elif any(word in text_lower for word in [
        "fight", "violence", "assault", "injured",
        "injury", "accident", "crash"
    ]):
        return (
            "VIOLENCE / ACCIDENT",
            "HIGH",
            "Emergency & Security Authority",
            "Immediate assessment and response recommended."
        )

    elif any(word in text_lower for word in [
        "suspicious", "strange", "intruder",
        "intrusion", "stolen", "theft", "robbery"
    ]):
        return (
            "SUSPICIOUS ACTIVITY",
            "MEDIUM",
            "Security Authority",
            "Verify the reported activity and assess the situation."
        )

    elif any(word in text_lower for word in [
        "crowd", "crowded", "people", "gathering"
    ]):
        return (
            "CROWD / PUBLIC SAFETY",
            "MEDIUM",
            "Public Safety Authority",
            "Monitor the situation and assess escalation risk."
        )

    else:
        return (
            "GENERAL SECURITY REPORT",
            "MEDIUM",
            "Relevant Authority",
            "Review and verify the submitted report."
        )


# =========================================================
# Generate Authority Report
# =========================================================

def create_report(phone, text, incident, risk, authority, action):

    report_id = "JAN-" + str(uuid.uuid4())[:6].upper()

    current_time = datetime.now().strftime("%Y-%m-%d  |  %H:%M")

    reporter = phone.strip() if phone and phone.strip() else "ANONYMOUS"

    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              JANBAK AI
        AUTHORITY INCIDENT REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REPORT ID
{report_id}

DATE / TIME
{current_time}

REPORTER
{reporter}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INCIDENT CLASSIFICATION
{incident}

RISK LEVEL
{risk}

ASSIGNED AUTHORITY
{authority}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DETECTED INFORMATION
{text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDED ACTION
{action}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATUS
REQUIRES HUMAN REVIEW

JANBAK AI provides decision-support analysis.
Final response decisions remain with authorized personnel.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return report


# =========================================================
# Main Processing Function
# =========================================================

def process_report(audio, phone):

    if audio is None:
        return (
            "NO VOICE REPORT RECEIVED",
            "—",
            "—",
            "—",
            "Waiting for an incoming voice report."
        )

    try:

        # Speech-to-text
        result = model.transcribe(
            audio,
            language="en",
            fp16=False
        )

        text = result["text"].strip()

        if not text:
            return (
                "NO SPEECH DETECTED",
                "—",
                "—",
                "—",
                "No understandable speech was detected."
            )

        # Incident analysis
        incident, risk, authority, action = analyze_incident(text)

        # Authority report
        report = create_report(
            phone,
            text,
            incident,
            risk,
            authority,
            action
        )

        return (
            text,
            incident,
            risk,
            authority,
            report
        )

    except Exception as e:

        return (
            "PROCESSING ERROR",
            "—",
            "—",
            "—",
            f"JANBAK system error:\n{str(e)}"
        )


# =========================================================
# JANBAK UI
# =========================================================

custom_css = """

/* ================================
   GLOBAL
================================ */

body {
    background: #080b10 !important;
}

.gradio-container {
    max-width: 1250px !important;
    background: #080b10 !important;
    color: #e8edf3 !important;
}


/* ================================
   HEADER
================================ */

.janbak-header {
    background: linear-gradient(
        135deg,
        #101722,
        #0b1018
    );

    border: 1px solid #263342;
    border-radius: 18px;

    padding: 28px 32px;
    margin-bottom: 20px;

    box-shadow:
        0 0 30px rgba(0,0,0,0.35);
}

.janbak-logo {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 3px;
    color: #ffffff;
}

.janbak-subtitle {
    font-size: 15px;
    color: #8f9baa;
    margin-top: 5px;
}

.system-status {
    display: inline-block;

    margin-top: 18px;
    padding: 7px 13px;

    border-radius: 20px;

    background: #10251b;
    border: 1px solid #1d5c3b;

    color: #65d99a;

    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}


/* ================================
   SECTION TITLES
================================ */

.section-title {
    font-size: 19px;
    font-weight: 700;

    color: #f3f6f9;

    margin-top: 8px;
    margin-bottom: 10px;
}


/* ================================
   CARDS
================================ */

.panel {
    background: #0e141d;

    border: 1px solid #222d3a;

    border-radius: 16px;

    padding: 20px;

    margin-bottom: 15px;
}


/* ================================
   LABELS
================================ */

label span {
    color: #9ba8b7 !important;
    font-weight: 600 !important;
}


/* ================================
   INPUTS
================================ */

textarea,
input {
    background: #090e15 !important;

    border: 1px solid #263342 !important;

    color: #edf2f7 !important;

    border-radius: 10px !important;
}


/* ================================
   BUTTON
================================ */

.analyze-button {
    width: 100% !important;

    min-height: 58px !important;

    border-radius: 12px !important;

    font-size: 16px !important;

    font-weight: 800 !important;

    letter-spacing: 0.5px !important;
}


/* ================================
   OUTPUT BOXES
================================ */

.output-box textarea {
    background: #090e15 !important;
}


/* ================================
   REPORT
================================ */

.report-box textarea {
    font-family: monospace !important;

    line-height: 1.55 !important;

    font-size: 13px !important;
}


/* ================================
   FOOTER
================================ */

.footer {
    text-align: center;

    color: #647181;

    font-size: 11px;

    margin-top: 25px;

    padding-bottom: 10px;
}

"""


# =========================================================
# Interface
# =========================================================

with gr.Blocks(
    title="JANBAK AI — Security Intelligence",
    css=custom_css
) as demo:

    # HEADER
    gr.HTML("""
    <div class="janbak-header">

        <div class="janbak-logo">
            JANBAK AI
        </div>

        <div class="janbak-subtitle">
            AI-POWERED SECURITY INTELLIGENCE PLATFORM
        </div>

        <div class="system-status">
            ● SYSTEM READY
        </div>

    </div>
    """)


    # -----------------------------------------------------
    # INCOMING REPORT
    # -----------------------------------------------------

    gr.HTML("""
    <div class="section-title">
        01 — INCOMING INCIDENT REPORT
    </div>
    """)

    with gr.Group(elem_classes="panel"):

        phone = gr.Textbox(
            label="Reporter Contact",
            placeholder="+966 5X XXX XXXX",
            info="Optional"
        )

        audio = gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="Voice Incident Report"
        )

        analyze_button = gr.Button(
            "🚨  SEND REPORT & RUN AI ANALYSIS",
            variant="primary",
            elem_classes="analyze-button"
        )


    # -----------------------------------------------------
    # AI ANALYSIS
    # -----------------------------------------------------

    gr.HTML("""
    <div class="section-title">
        02 — JANBAK AI ANALYSIS
    </div>
    """)

    with gr.Group(elem_classes="panel"):

        with gr.Row():

            with gr.Column(scale=2):

                transcription = gr.Textbox(
                    label="Speech Transcription",
                    lines=5,
                    placeholder="AI-generated transcription..."
                )

            with gr.Column(scale=1):

                incident = gr.Textbox(
                    label="Incident Classification",
                    placeholder="—"
                )

                risk = gr.Textbox(
                    label="Risk Level",
                    placeholder="—"
                )

                authority = gr.Textbox(
                    label="Assigned Authority",
                    placeholder="—"
                )


    # -----------------------------------------------------
    # AUTHORITY DASHBOARD
    # -----------------------------------------------------

    gr.HTML("""
    <div class="section-title">
        03 — AUTHORITY RESPONSE INTELLIGENCE
    </div>
    """)

    with gr.Group(elem_classes="panel"):

        authority_report = gr.Textbox(
            label="Generated Authority Report",
            lines=22,
            placeholder="The structured authority report will appear here...",
            elem_classes="report-box"
        )


    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    gr.HTML("""
    <div class="footer">
        JANBAK AI • Security Intelligence Prototype<br>
        AI-assisted decision support — final decisions remain with authorized personnel.
    </div>
    """)


    # -----------------------------------------------------
    # BUTTON ACTION
    # -----------------------------------------------------

    analyze_button.click(
        fn=process_report,

        inputs=[
            audio,
            phone
        ],

        outputs=[
            transcription,
            incident,
            risk,
            authority,
            authority_report
        ]
    )


# =========================================================
# Launch
# =========================================================

if __name__ == "__main__":
    demo.launch()
