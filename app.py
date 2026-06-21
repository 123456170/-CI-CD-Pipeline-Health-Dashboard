import streamlit as st
import json
import re
from datetime import datetime

st.set_page_config(page_title="CI/CD Pipeline Health Dashboard", layout="wide")

st.title("🚀 CI/CD Pipeline Health Dashboard")
st.caption("Unified monitoring for Jenkins, GitHub Actions, GitLab CI, and CircleCI")

# --- Input Section ---
st.header("📥 Input Pipeline Data")

pipeline_logs = st.text_area("Paste Pipeline Logs", height=250)
pipeline_config = st.text_area("Paste Pipeline Config", height=200)

# --- Simple heuristic "AI analysis" engine ---
def analyze_logs(logs: str, config: str):
    logs_lower = logs.lower()

    failures = []
    warnings = []
    flaky_tests = []

    # Detect failures
    if "failed" in logs_lower or "error" in logs_lower:
        failures.append("Detected failure keywords in logs.")

    # Detect test instability (simple heuristic)
    flaky_patterns = ["retry", "flaky", "unstable", "rerun"]
    for p in flaky_patterns:
        if p in logs_lower:
            flaky_tests.append(f"Possible flaky behavior detected due to keyword: '{p}'")

    # Pipeline duration estimation (mock)
    duration = len(logs.split()) * 0.05  # fake heuristic

    # Risk scoring
    risk = 20
    if failures:
        risk += 40
    if flaky_tests:
        risk += 20
    if "deploy" in logs_lower and "error" in logs_lower:
        risk += 20

    risk = min(risk, 100)

    # Bottlenecks (mock logic)
    bottlenecks = []
    if "build" in logs_lower:
        bottlenecks.append("Build step may be slow or repeated frequently.")
    if "test" in logs_lower:
        bottlenecks.append("Test suite execution contributing to pipeline latency.")

    # Optimization suggestions
    recommendations = [
        "Enable caching for dependencies to reduce build time.",
        "Parallelize test execution across runners.",
        "Add retry limits to stabilize flaky tests.",
        "Split monolithic pipeline into smaller stages."
    ]

    return {
        "pipeline_status": "FAILED" if failures else "SUCCESS",
        "estimated_duration_minutes": round(duration, 2),
        "failures_detected": failures,
        "flaky_tests": flaky_tests,
        "bottlenecks": bottlenecks,
        "optimization_recommendations": recommendations,
        "deployment_risk_score": risk,
        "timestamp": datetime.now().isoformat()
    }


# --- Output Section ---
if st.button("🔍 Analyze Pipeline"):
    if not pipeline_logs:
        st.warning("Please paste pipeline logs.")
    else:
        result = analyze_logs(pipeline_logs, pipeline_config)

        st.subheader("📊 Pipeline Health Report")

        st.json(result)

        st.subheader("🚨 Summary")
        st.write(f"**Status:** {result['pipeline_status']}")
        st.write(f"**Risk Score:** {result['deployment_risk_score']} / 100")
        st.write(f"**Estimated Duration:** {result['estimated_duration_minutes']} minutes")

        if result["flaky_tests"]:
            st.warning("⚠ Flaky test signals detected")
        if result["failures_detected"]:
            st.error("❌ Failures detected in pipeline")


# --- Sidebar Info ---
st.sidebar.title("🔗 Supported CI/CD Systems")
st.sidebar.write("• Jenkins")
st.sidebar.write("• GitHub Actions")
st.sidebar.write("• GitLab CI")
st.sidebar.write("• CircleCI")

st.sidebar.info("This is a lightweight simulation dashboard (no external APIs required).")