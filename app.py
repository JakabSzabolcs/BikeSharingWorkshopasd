"""A workshop dashboardjának futtatható váza."""

import streamlit as st

from data_preparation import load_bike_data

st.set_page_config(page_title="Szöuli kerékpárkölcsönzés", layout="wide")

st.html("""
<style>
[class*="st-key-workshop-panel-"] {
    min-height: 13rem;
}
</style>
""")

st.title("Szöuli kerékpárkölcsönzés")

try:
    data = load_bike_data()
except (OSError, ValueError) as error:
    st.error(f"Az adatok betöltése sikertelen. {error}")
    st.stop()

with st.sidebar:
    st.header("Szűrők")
    # TODO: Hozd létre a szűrőket. A kiválasztott megfigyeléseket add át a paneleknek.
    st.empty()
    st.divider()
    total = f"{len(data):,}".replace(",", "\u202f")
    st.caption(f"Betöltve · {total} órás megfigyelés")
    st.caption("[Adatforrás · UCI Machine Learning Repository](https://doi.org/10.24432/C5F62R)")

left, right = st.columns(2, gap="medium")
with left:
    with st.container(border=True, key="workshop-panel-time"):
        st.subheader("Időbeli változás")
        # TODO: Készíts vizualizációt a kölcsönzésszám időbeli változásáról.
        st.empty()

    with st.container(border=True, key="workshop-panel-distribution"):
        st.subheader("Eloszlások")
        # TODO: Hasonlítsd össze a kölcsönzésszám eloszlását általad választott csoportokban.
        st.empty()

with right:
    with st.container(border=True, key="workshop-panel-week"):
        st.subheader("Heti és napi mintázatok")
        # TODO: Vizsgáld meg a hét napja és az óra kapcsolatát a kölcsönzésszámmal.
        st.empty()

    with st.container(border=True, key="workshop-panel-weather"):
        st.subheader("Időjárás és kölcsönzés")
        # TODO: Vizsgáld meg a kölcsönzésszám és egy időjárási változó kapcsolatát.
        st.empty()
