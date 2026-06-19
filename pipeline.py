from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:
    state = {}
    
    # 1. Search Execution
    print("\n[Step 1] Search Agent is working...")
    search_agent = build_search_agent()
    # Notice the new 'messages' list invocation format
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, detailed information about: {topic}")]
    })
    # We extract the text from the very last message the AI generated
    state["search_results"] = search_result["messages"][-1].content
    
    # 2. Reader Execution
    print("\n[Step 2] Reader Agent is extracting deep URL content...")
    reader_agent = build_reader_agent()
    reader_input = f"Based on this web research, pick the relevant URLs and scrape them for deeper context:\n{state['search_results']}"
    reader_result = reader_agent.invoke({
        "messages": [("user", reader_input)]
    })
    state["scraped_content"] = reader_result["messages"][-1].content
    
    # 3. Writer Execution
    print("\n[Step 3] Writer Chain is drafting the report...")
    combined_research = f"Raw Search Data:\n{state['search_results']}\n\nDeeper Scraped Context:\n{state['scraped_content']}"
    report = writer_chain.invoke({
        "topic": topic, 
        "research": combined_research
    })
    state["report"] = report
    
    # 4. Critic Execution
    print("\n[Step 4] Critic Chain is reviewing the final draft...")
    feedback = critic_chain.invoke({"report": report})
    state["feedback"] = feedback
    
    print("\nPipeline Complete!")
    return state