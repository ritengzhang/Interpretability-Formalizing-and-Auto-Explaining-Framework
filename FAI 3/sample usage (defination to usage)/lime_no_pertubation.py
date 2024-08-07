# Import necessary modules

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
import numpy as np
# Assuming PyTorch Implementation Classes are defined here or imported

# Define the specific functions needed for LIME
class GeneratePerturbations:
    def __call__(self, inputs):
        input_data, num_features = inputs
        # Generate perturbations around the input data
        perturbations = self.perturb_data(input_data, num_features)
        return PerturbedDataSet(name="perturbed_data", data=perturbations)

    def perturb_data(self, data, num_features):
        # Simple perturbation logic: add noise to the data
        perturbations = data + np.random.normal(0, 0.1, size=(100, num_features))
        return perturbations

generate_perturbations = Function(
    computation_name="generate_perturbations",
    input_types=[InputData, FAI_Number],
    output_type=PerturbedDataSet,
    pytorch_impl=GeneratePerturbations
)

select_features = Function(
    computation_name="select_features", 
    input_types=[FeatureSet, FAI_Index], 
    output_type=0  # Output type is the same as the first input type
)

fit_linear_model = Function(
    computation_name="fit_linear_model", 
    input_types=[FeatureSet, Model, InputData], 
    output_type=LinearModel
)

compute_local_importance = Function(
    computation_name="compute_local_importance", 
    input_types=[LinearModel, FeatureSet], 
    output_type=ImportanceScores
)

context_lime = {
    "model": Model(name="main model"),
    "input_data": InputData(name="Input data", listability="individual"),
    "num_features": FAI_Index(name="Index of features for LIME"),  # Changed to FAI_Index
    "select_features": select_features,
    "fit_linear_model": fit_linear_model,
    "compute_local_importance": compute_local_importance
}

# Define the formula for LIME
formula_str_lime = '''compute_local_importance(fit_linear_model(select_features(input_data, num_features), model, input_data), select_features(input_data, num_features))'''

# Compile the formula
compiled_operation_lime = compile_formula_revised(formula_str_lime, context_lime)

# Execute the compiled operation
result_lime = compiled_operation_lime.execute()
print("Result:", result_lime)

# Print the operation tree
compiled_operation_lime.print_tree()

# Collect and print traces
traces_lime = compiled_operation_lime.collect_traces()
print("\nAll traces:")
for trace in traces_lime:
    print(trace)

# Print name trace mapping
compiled_operation_lime.print_name_trace_mapping()

# Print all elements
print("\nAll elements:")
for element in Element.all_elements.values():
    print(element)

# Print attributes and return objects for specific elements
print("xxxxxxxxxxxxxxxxxxxxxxxxx given element print info")
print(compiled_operation_lime.print_attributes_and_return_object("fit_linear_model").trace)
print("xxxxxxxxxxxxxxxxxxxxxxxxx given element print info")
print(compiled_operation_lime.print_attributes_and_return_object("main model").trace)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print(compiled_operation_lime.print_attributes_and_return_object("compute_local_importance").trace)

# Print all existing elements
for i in compiled_operation_lime.all_existing_elements:
    print(i.id)
