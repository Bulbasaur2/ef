import json

# Basic mapping from Scratch block opcode to Python code
SCRATCH_TO_PYTHON = {
    "motion_movesteps": lambda args: f"x += {args[0]}",  # Move steps
    "control_repeat": lambda args, substack: f"for _ in range({args[0]}):\n{indent(substack)}",
    "looks_say": lambda args: f"print({repr(args[0])})",  # Say
    "event_whenflagclicked": lambda args: "# when green flag clicked",
    "control_if": lambda args, substack: f"if {args[0]}:\n{indent(substack)}",
    # Add more mappings as needed
}

def indent(code, level=1):
    prefix = "    " * level
    return "\n".join(prefix + line if line else "" for line in code.splitlines())

def convert_block(block, blocks):
    opcode = block["opcode"]
    inputs = block.get("inputs", {})
    fields = block.get("fields", {})
    args = []
    # Extract arguments from inputs/fields (simplified)
    for k, v in fields.items():
        args.append(v[0])
    for k, v in inputs.items():
        # If input is a block, resolve recursively
        if isinstance(v, list) and len(v) > 1 and isinstance(v[1], dict) and "block" in v[1]:
            subblock_id = v[1]["block"]
            subblock = blocks[subblock_id]
            args.append(convert_block(subblock, blocks))
        else:
            args.append(v)
    # For blocks with substack (like repeat, if)
    if "SUBSTACK" in inputs and inputs["SUBSTACK"][1]:
        substack_id = inputs["SUBSTACK"][1]["block"]
        substack_block = blocks[substack_id]
        substack_code = convert_block(substack_block, blocks)
        return SCRATCH_TO_PYTHON.get(opcode, lambda *_: "# Unsupported block")(args, substack_code)
    return SCRATCH_TO_PYTHON.get(opcode, lambda *_: "# Unsupported block")(args)

def convert_scratch_json(scratch_json):
    # Assume 'targets' is a list of sprites, each with 'blocks'
    python_code = ""
    for target in scratch_json.get("targets", []):
        blocks = target.get("blocks", {})
        # Find top-level blocks (e.g. event_whenflagclicked)
        for block_id, block in blocks.items():
            if block.get("topLevel"):
                python_code += convert_block(block, blocks) + "\n"
    return python_code

if __name__ == "__main__":
    # Example usage:
    # Load a Scratch project JSON
    with open("project.json") as f:
        scratch_json = json.load(f)
    python_code = convert_scratch_json(scratch_json)
    print(python_code)