import pandas as pd
import streamlit as st

# Set up page config
st.set_page_config(
    page_title="Distributed Systems Study Hub", page_icon="📺", layout="wide"
)

st.title("📚 Distributed Systems Study Dashboard")
st.markdown(
    "All your scraped textbook topic videos embedded and ready to watch"
    " offline/instantly."
)


# Load data safely from the CSV file
@st.cache_data
def load_data():
  try:
    return pd.read_csv("distributed_systems_videos.csv")
  except FileNotFoundError:
    return None


df = load_data()

if df is not None and not df.empty:
  # Sidebar filter for convenience
  st.sidebar.header("Navigation")
  selected_topic = st.sidebar.selectbox(
      "Filter by Topic", ["All Topics"] + list(df["Topic"].unique())
  )

  # Filter dataframe based on selection
  if selected_topic != "All Topics":
    filtered_df = df[df["Topic"] == selected_topic]
  else:
    filtered_df = df

  st.markdown(f"### Showing {len(filtered_df)} Resources")
  st.divider()

  # Loop through and display each video entry
  for index, row in filtered_df.iterrows():
    with st.container():
      col1, col2 = st.columns([1, 1.5])

      with col1:
        st.markdown(f"### 📌 {row['Topic']}")
        st.markdown(f"**Title:** {row['Video Title']}")
        st.markdown(f"**Channel:** {row['Channel']}")
        st.markdown(f"[🔗 Open Directly on YouTube]({row['Direct Link']})")

      with col2:
        # Use native Streamlit video component for clean embedding
        direct_link = row["Direct Link"]
        if pd.notna(direct_link):
          st.video(direct_link)
        else:
          st.warning("Video link not available.")

      st.markdown("---")
else:
  st.error(
      "⚠️ `distributed_systems_videos.csv` not found! Please run your scraping"
      " script first to generate the CSV file."
  )
  