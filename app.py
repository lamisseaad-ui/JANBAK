import gradio as gr
import whisper

# Load speech recognition model
model = whisper.load_model("tiny")


def process_report(audio, phone):

    if audio is None:
        return (
            "No voice report received.",
            "",
            "",
            "",
            ""
        )

    # 1. Speech to text
    result = model.transcribe(
        audio,
        language="en",
        fp16=False
    )

    text = result["text"].strip()

    if not text:
        return (
            "No speech detected.",
            "",
            "",
            "",
            ""
        )

    # 2. Incident analysis
    text_lower = text.lower()

    if any(word in text_lower for word in ["fire", "burning", "smoke"]):
        incident = "Fire / Emergency"
        risk = "CRITICAL"
        authority = "Emergency Response Authority"
        action = "Immediate emergency response recommended."

    elif any(word in text_lower for word in ["attack", "weapon", "threat"]):
        incident = "Security Threat"
        risk = "HIGH"
        authority = "Security Authority"
        action = "Immediate verification and security response recommended."

    elif any(word in text_lower for word in ["suspicious", "strange"]):
        incident = "Suspicious Activity"
        risk = "MEDIUM"
        authority = "Security Authority"
        action = "Verify the reported activity."

    else:
        incident = "General Security Report"
        risk = "MEDIUM"
        authority = "Relevant Authority"
        action = "Review and verify the report."

    # 3. Generate authority report
    report_id = "JAN-001"

    authority_report = f"""
JANBAK AI — AUTHORITY REPORT

Report ID:
{report_id}

Reporter:
{phone if phone else "Anonymous"}

Incident:
{incident}

Risk Level:
{risk}

Detected Information:
{text}

Assigned Authority:
{authority}

Recommended Action:
{action}

Status:
REQUIRES REVIEW
"""

    return text, incident, risk, authority, authority_report


# JANBAK interface
with gr.Blocks(title="JANBAK AI") as demo:

    gr.Markdown("""
    # JANBAK AI
    ### AI-Powered Security Reporting System
    """)

    gr.Markdown("""
    **Reporter → JANBAK AI → Analysis → Relevant Authority**
    """)

    gr.Markdown("## 📞 1. Incoming Report")

    phone = gr.Textbox(
        label="Reporter Phone Number",
        placeholder="+966 5X XXX XXXX"
    )

    audio = gr.Audio(
        sources=["microphone"],
        type="filepath",
        label="🎙️ Voice Report"
    )

    analyze_button = gr.Button(
        "🚨 Send & Analyze Report",
        variant="primary"
    )

    gr.Markdown("## 🤖 2. JANBAK AI Analysis")

    transcription = gr.Textbox(
        label="Speech Transcription",
        lines=4
    )

    incident = gr.Textbox(
        label="Incident Type"
    )

    risk = gr.Textbox(
        label="Risk Level"
    )

    authority = gr.Textbox(
        label="Assigned Authority"
    )

    gr.Markdown("## 🏢 3. Authority Dashboard")

    authority_report = gr.Textbox(
        label="📋 Generated Authority Report",
        lines=16
    )

    analyze_button.click(
        fn=process_report,
        inputs=[audio, phone],
        outputs=[
            transcription,
            incident,
            risk,
            authority,
            authority_report
        ]
    )


if __name__ == "__main__":
    demo.launch()
