def generate_response(state):
    if state.intent and "error" in state.intent:
        return f"❌ Fatal error: {state.intent['error']}"

    if state.status == "failed":
        return "❌ Something went wrong during execution."

    # Summarize the results
    if state.tool_results:
        summary = "Task completed. Results:\n"
        for i, result in enumerate(state.tool_results):
            summary += f"Step {i+1}: {result}\n"
        return summary.strip()
    else:
        return "No actions were taken."