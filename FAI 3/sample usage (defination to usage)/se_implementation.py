
import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
from Elements import *
from Functions import *
from Operation import *
import torch
from torch import nn
# Assuming PyTorch Implementation Classes are defined here or imported


def ArgminModule(result_mapping):
        min_value = float('inf')
        min_element = None
        for element in result_mapping:
            value = result_mapping[element]

            if value < min_value:
                min_value = value
                min_element = element

        return min_element

def DiffModule(inputs):
        input1, input2 = inputs[0], inputs[1]
        return sum(sum(input1 - input2))

Argmin = Function(
    computation_name="Argmin",
    input_types=[Value, Element, Element],
    output_type=2,
    output_listability="individual",
    implementation=ArgminModule,
    mapping_type = True
)

diff = Function(
    computation_name="diff",
    input_types=[Element, Element],
    output_type=0,
    implementation=DiffModule
)


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
        inp = context[inp.name]
        func = operation.inputs[0]
        for idx,i in enumerate(inp):
            result_mapping = {}
            for key, value in context.items():
                if isinstance(value, str) and value == inpname:
                    loop_conceptual_context = context.copy()
                    loop_conceptual_context[key] = i
            result_mapping[idx] = execute_operation(func, loop_conceptual_context)
        return operation.function.implementation(result_mapping)


    resolved_inputs = []
    for inp in operation.inputs:
        
        if isinstance(inp, Operation):
                    # Recursively resolve the operation input
            input_result = execute_operation(inp, context)
            resolved_inputs.append(input_result)

        elif inp.name in context:
            # Use the direct element from context
            resolved_inputs.append(context[inp.name])

        else:
            raise ValueError(f"Input {inp.name} not found in context.")
    
    # Execute the operation's implementation with resolved inputs
    return operation.function.implementation(resolved_inputs)

# Example usage
if __name__ == "__main__":
    # Define the operations and elements
    query_input = Element(name="query_input")
    some_input = Element(name="some_input", loop_conceptual=True)
    all_input_data = Element(name="all_input_data", loop_complete=True)

    diff_op = Operation("DiffOp", [query_input, some_input], diff)
    argmin_op = Operation("ArgminOp", [diff_op, some_input, all_input_data], Argmin)

    # Context with actual values for elements
    context = {
        'query_input': torch.randn(1, 10),
        'some_input':  'all_input_data',
        'all_input_data': torch.randn(5, 10)
    }

    # Execute the top-level operation
    result = execute_operation(argmin_op, context)
    print("Result:", result)
