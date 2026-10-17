# Hotel Management Agent

Simulation-only AI agent for a KTS demonstration.

Goal example:
"Check in Rahul for 2 nights, give him a clean room, and add late checkout."

Architecture:
Goal -> Agent -> Tools -> Hotel Environment -> Observation -> Agent -> Goal Complete

The default controller is deterministic so the demo works offline and is reliable during a live
session. The hotel tools/environment are deliberately separated so an LLM decision-maker can be
added later without rewriting the simulated hotel.

Run:
    pip install -r requirements.txt
    streamlit run app.py

Or use run.bat on Windows.

This project does not connect to real hotels, reservations, guests, or payments.
