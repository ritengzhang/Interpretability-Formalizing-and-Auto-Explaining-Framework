from Elements import *
from Functions import *
from Operation import *

def execute_operation(operation, context):
    """
    Directly execute an operation using the provided context.
    Recursively processes any operation inputs and uses the implementation to compute the result.
    """
    # Check if the operation has an implementation
    if not hasattr(operation.function, 'implementation'):
        raise ValueError(f"No implementation provided for the operation {operation.name}")
    
    # Prepare inputs for this operation
    if operation.function.mapping_type:
        inp = operation.inputs[2]
        inpname = inp.name
        inp = context[inpname]
        func = operation.inputs[0]
        result_mapping = {}
        for idx, i in enumerate(inp):
            loop_conceptual_context = context.copy()
            loop_conceptual_context[inpname] = i
            result_mapping[idx] = execute_operation(func, loop_conceptual_context)
        return operation.function.implementation(result_mapping)

    resolved_inputs = []
    for inp in operation.inputs:
        if isinstance(inp, Operation):
            # Recursively resolve the operation input
            input_result = execute_operation(inp, context)
            resolved_inputs.append(input_result)
        else:
            resolved_inputs.append(context[inp.name])

    # Execute the operation's implementation with resolved inputs
    return operation.function.implementation(resolved_inputs)