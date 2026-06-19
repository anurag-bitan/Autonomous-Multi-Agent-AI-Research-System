import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(page_title="Multi-Agent Researcher", layout="wide")

st.title("🧠 Multi-Agent Research System")
st.markdown("An autonomous workflow leveraging search agents, scraping tools, and LCEL chains to generate peer-reviewed reports.")

topic = st.text_input("What would you like to research today?", placeholder="e.g., The impact of quantum computing on cryptography")

if st.button("Generate Research"):
    if not topic.strip():
        st.warning("Please enter a valid research topic.")
    else:
        with st.status("Initializing AI Pipeline...", expanded=True) as status:
            st.write("🕵️‍♀️ Search Agent gathering live internet data...")
            st.write("📖 Reader Agent parsing and scraping URL sources...")
            st.write("✍️ Writer Chain synthesizing data into a report...")
            st.write("🧐 Critic Chain auditing the draft for quality...")
            
            # Execute the shared-state pipeline
            results = run_research_pipeline(topic)
            status.update(label="Research Complete!", state="complete", expanded=False)
        
        # Render Tabs for clean UI separation
        tab1, tab2, tab3 = st.tabs(["📄 Final Report", "📊 Critic Review", "🛠️ Raw Pipeline State"])
        
        with tab1:
            st.markdown(results["report"])
            
        with tab2:
            st.markdown(results["feedback"])
            
        with tab3:
            st.subheader("Search Output")
            st.write(results["search_results"])
            st.divider()
            st.subheader("Scraped Deep Context")
            st.write(results["scraped_content"])