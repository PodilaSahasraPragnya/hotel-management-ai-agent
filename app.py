import streamlit as st
from environment import HotelEnvironment
from agent import HotelAgent

st.set_page_config(page_title="Hotel Management Agent", page_icon="🏨", layout="wide")
st.title("🏨 Hotel Management Agent")
st.caption("Simulation only — the agent changes a simulated hotel environment.")

if "env" not in st.session_state:
    st.session_state.env = HotelEnvironment()
if "steps" not in st.session_state:
    st.session_state.steps = []

env = st.session_state.env

with st.sidebar:
    st.header("🎯 Goal")
    guest = st.text_input("Guest", "Rahul")
    nights = st.number_input("Nights", 1, 14, 2)
    late = st.checkbox("Late checkout", True)

    if st.button("▶ Run Agent", type="primary", use_container_width=True):
        st.session_state.steps = HotelAgent(env).run(guest, int(nights), late)
        st.rerun()

    if st.button("↩ Reset", use_container_width=True):
        st.session_state.env = HotelEnvironment()
        st.session_state.steps = []
        st.rerun()

left, right = st.columns([1.2,1])

with left:
    st.subheader("🏨 Live Hotel State")
    st.dataframe(
        [{"Room":r["id"],"Type":r["type"],"Status":r["status"].upper(),"Guest":r["guest"] or "—"}
         for r in env.rooms.values()],
        use_container_width=True, hide_index=True)
    st.subheader("📋 Reservations")
    st.dataframe(env.reservations, use_container_width=True, hide_index=True)

with right:
    st.subheader("🤖 Agent Activity")
    if not st.session_state.steps:
        st.info("Give the agent a goal and press Run Agent.")
    for i,s in enumerate(st.session_state.steps,1):
        if s["type"] == "complete":
            st.success(f"Step {i}: 🎯 GOAL COMPLETED — {s['summary']}")
        elif s["type"] == "stop":
            st.error(f"Step {i}: {s['summary']}")
        else:
            with st.container(border=True):
                st.write(f"**Step {i}: 🔧 {s['tool']}**")
                st.write(s["summary"])
                st.caption(s["result"]["message"])

    r = env.find_reservation(guest)
    if r and r["status"] == "checked_in":
        room = env.get_room(r["room_id"])
        st.subheader("🎉 Visible Result")
        st.success("CHECK-IN COMPLETED")
        st.write(f"**Guest:** {r['guest_name']}")
        st.write(f"**Room:** {room['id']} ({room['type']})")
        st.write(f"**Nights:** {r['nights']}")
        st.write(f"**Late checkout:** {'Yes' if r['late_checkout'] else 'No'}")
