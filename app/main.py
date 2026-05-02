from agent.loop import run_agent

if __name__ == "__main__":
    state = None

    while True:
        prompt = "🎤 Say something: " if state is None else "> "
        user_input = input(prompt)
        state, result = run_agent(user_input, state)

        print("\n🤖 Response:")
        print(result)

        if state is None or state.status == "completed" or not state.awaiting_confirmation:
            break