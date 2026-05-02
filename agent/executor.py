from tools.registry import TOOLS

def execute_step(step: dict, state):
    tool_name = step["tool"]
    tool_fn = TOOLS.get(tool_name)

    if not tool_fn:
        return {"error": f"Tool {tool_name} not found"}

    try:
        params = resolve_references(step["input"], state)
        result = tool_fn(params)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
    
def resolve_references(input_data, state):
    if isinstance(input_data, dict):
        return {
            k: resolve_references(v, state)
            for k, v in input_data.items()
        }

    if isinstance(input_data, str) and input_data.startswith("$step_"):
        step_num = int(input_data.split("_")[1].split(".")[0])
        key = input_data.split(".")[1]

        return state.tool_results[step_num - 1]["result"].get(key)

    return input_data