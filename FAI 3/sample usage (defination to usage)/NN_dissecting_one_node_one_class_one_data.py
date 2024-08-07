import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Now you can import the module from the parent directory
from Elements import *
from Functions  import*
from Operation import *



get_activation = Function(
    computation_name="get_activation", 
    input_types=[Model, InputData], 
    output_type=ActivationRepresentation
)

select = Function(
    computation_name="select", 
    input_types=[ActivationRepresentation, FAI_Index], 
    output_type=ActivationRepresentation
)

iou_function = Function(
    computation_name="Iou", 
    input_types=[ActivationRepresentation, ActivationRepresentation], 
    output_type=FAI_Number
)

get_output = Function(
    computation_name="get_output", 
    input_types=[Model, InputData], 
    output_type=Element
)


context_adjusted = {
    "model": Model(name="main model"),
    "seg_model": Auxillary_model(name="seg model"),
    "One_input_data": InputData(name="my data"),
    "get_activation": get_activation,
    "select": select,
    "Iou": iou_function,
    "neuron_index": FAI_Index(name="Index of neuron focused"),
    "get_output":get_output 
    
}

formula_str_revised = "Iou(get_output(seg_model, One_input_data), select(get_activation(model, One_input_data), neuron_index))"


compiled_operation_revised = compile_formula_revised(formula_str_revised, context_adjusted)
print(compiled_operation_revised)
result = compiled_operation_revised.execute()
print("Result:", result)

compiled_operation_revised.print_tree()

traces = compiled_operation_revised.collect_traces()
print("\nAll traces:")
for trace in traces:
    print(trace)

print(2143142141231)

compiled_operation_revised.print_name_trace_mapping()


print("\nAll elements:")
for element in Element.all_elements.values():
    print(element)


print("xxxxxxxxxxxxxxxxxxxxxxxxx given element print info")
print(compiled_operation_revised.print_attributes_and_return_object("Iou").trace)
print("xxxxxxxxxxxxxxxxxxxxxxxxx given element print info")
print(compiled_operation_revised.print_attributes_and_return_object("main model").trace)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print(compiled_operation_revised.print_attributes_and_return_object("fai_number iou(element, activationrepresentation)").trace)

#下一步可以再写一个什么方法出来，熟悉一下这个操作流程然后写context init过程
#再下一步又可以系统地扩建所有function和element了， 根据不同可解释性方法遍历，function element同时建，建一个function想他的input output type，然后写入context和element里