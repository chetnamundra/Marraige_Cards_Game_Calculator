# streamlit_app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Marraige Cards Game Calculator", layout="wide")


def init():
    if "players" not in st.session_state:
        st.session_state.players = (
            []
        )  # list of dicts: {"name": str, "rounds": [[m,p,round_pts,cum_pts], ...]}
    if "round_index" not in st.session_state:
        st.session_state.round_index = 0
    if "started" not in st.session_state:
        st.session_state.started = False


init()

st.title("Maal-Points Game (no saving)")

with st.sidebar:
    st.header("Setup")
    if not st.session_state.started:
        n = st.number_input(
            "Number of players", min_value=2, max_value=20, value=3, step=1
        )
        names = []
        for i in range(int(n)):
            names.append(st.text_input(f"Player {i+1} name", value=f"Player{i+1}"))
        if st.button("Start game"):
            # initialize players
            st.session_state.players = [
                {"name": names[i].strip() or f"Player{i+1}", "rounds": []}
                for i in range(int(n))
            ]
            st.session_state.round_index = 0
            st.session_state.started = True
            st.rerun()
    else:
        st.write("Game started")
        if st.button("Reset game"):
            for k in list(st.session_state.keys()):
                if k not in ["page_config"]:
                    del st.session_state[k]
            st.rerun()

st.markdown("---")

if not st.session_state.started:
    st.info("Configure players in the sidebar and press **Start game**.")
    st.stop()

players = st.session_state.players
n = len(players)
r = st.session_state.round_index

st.subheader(f"Round {r+1} — Enter inputs")

cols = st.columns(n)
round_inputs = []
for idx, p in enumerate(players):
    with cols[idx]:
        st.markdown(f"**{p['name']}**")
        m = st.number_input(
            f"Maal ({p['name']})", min_value=0, value=0, key=f"m_{r}_{idx}"
        )
        pts = st.number_input(
            f"Points ({p['name']})", min_value=0, value=0, key=f"p_{r}_{idx}"
        )
        round_inputs.append((m, pts))

closer_name = st.selectbox(
    "Player who closed the game", options=[p["name"] for p in players], index=0
)
if st.button("Submit round"):
    # Prepare data structures
    tm = sum(m for m, _ in round_inputs)
    # append provisional round entries
    for idx, (m, pts) in enumerate(round_inputs):
        players[idx]["rounds"].append([m, pts, 0, 0])  # fill round_pts and cum later

    # find index of closer
    cp = next(i for i, p in enumerate(players) if p["name"] == closer_name)

    # calculate round points
    tp = 0
    for i in range(n):
        if i == cp:
            continue
        m_i = players[i]["rounds"][r][0]
        p_i = players[i]["rounds"][r][1]
        round_pt = (m_i * n) - (tm + p_i)
        players[i]["rounds"][r][2] = round_pt
        tp += round_pt

    players[cp]["rounds"][r][2] = -tp

    # calculate cumulative
    for i in range(n):
        if r == 0:
            players[i]["rounds"][r][3] = players[i]["rounds"][r][2]
        else:
            players[i]["rounds"][r][3] = (
                players[i]["rounds"][r - 1][3] + players[i]["rounds"][r][2]
            )

    st.session_state.round_index += 1
    st.success("Round submitted")
    st.rerun()

# Display scoreboard
st.header("Scoreboard")
# Build dataframe: latest cumulative for each player
df = pd.DataFrame(
    {
        "Player": [p["name"] for p in players],
        "Current Total": [p["rounds"][-1][3] if p["rounds"] else 0 for p in players],
    }
)
st.dataframe(df.style.format({"Current Total": "{:.0f}"}), use_container_width=True)

# Expanders for round-by-round history per player
st.markdown("### Player histories")
hist_cols = st.columns(n)
for idx, p in enumerate(players):
    with hist_cols[idx]:
        st.subheader(p["name"])
        if not p["rounds"]:
            st.write("No rounds yet")
            continue
        hist_df = pd.DataFrame(
            p["rounds"], columns=["Maal", "Points", "Round Points", "Cumulative"]
        )
        hist_df.index = [f"R{ix+1}" for ix in range(len(hist_df))]
        st.table(hist_df)

st.markdown("---")
st.write(
    "Tip: open this app on any device. This session persists while the page is open, but is not saved permanently."
)
