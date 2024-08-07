import sys
import os
import numpy as np
from sklearn.linear_model import LinearRegression
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
from Elements import *
from Functions import *
from Operation import *
from automation import *

# Define Elements
class LinearModel(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class FeatureSet(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "complete"

class ImportanceScores(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class PerturbedDataSet(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "complete"

# Define Function Implementations
class GeneratePerturbations:
    def __call__(self, inputs):
        input_data, num_perturbations, variance, model = inputs
        perturbations, y_perturbed = self.perturb_data(input_data, num_perturbations, variance, model)
        return perturbations, y_perturbed

    def perturb_data(self, data, num_perturbations, variance, model):
        perturbations = data + np.random.normal(0, variance, size=(num_perturbations, data.shape[1]))
        outputs = model(torch.tensor(perturbations, dtype=torch.float32)).detach().numpy()
        y_perturbed = np.argmax(outputs, axis=1)  # Convert probabilities to class labels using argmax
        return perturbations, y_perturbed


class FitLinearModel:
    def __call__(self, inputs):
        print(inputs[0])
        X,y=inputs[0]
        linear_model = LinearRegression().fit(X,y)
        return linear_model


class ComputeLocalImportance:
    def __call__(self, inputs):
        linear_model, features = inputs
        importances = np.abs(linear_model.coef_)
        return importances

# Define the specific functions needed for LIME
generate_perturbations = Function(
    computation_name="generate_perturbations",
    input_types=[InputData, FAI_Number, FAI_Number, Model],
    output_type=PerturbedDataSet,
    implementation=GeneratePerturbations()
)

fit_linear_model = Function(
    computation_name="fit_linear_model",
    input_types=[PerturbedDataSet, FeatureSet],
    output_type=LinearModel,
    implementation=FitLinearModel()
)

compute_local_importance = Function(
    computation_name="compute_local_importance",
    input_types=[LinearModel, FeatureSet],
    output_type=ImportanceScores,
    implementation=ComputeLocalImportance()
)

# Define the PyTorch model and dataset
class SimpleNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(x)
        return out

# Generate a toy dataset
X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to PyTorch tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.long)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.long)

# Create the model
input_dim = X_train.shape[1]
hidden_dim = 20  # Make hidden_dim equal to input_dim to avoid shape mismatch
output_dim = 2
model = SimpleNN(input_dim, hidden_dim, output_dim)

# Define loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train the model
num_epochs = 5
for epoch in range(num_epochs):
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Define the contexts for LIME
context_lime_conceptual = {
    "model": Model(name="model"),
    "input_data": InputData(name="input_data", listability="individual"),
    "num_perturbations": FAI_Number(name="num_perturbations"),
    "variance": FAI_Number(name="variance"),
    "features": FeatureSet(name="features"),
    "fit_linear_model": fit_linear_model,
    "compute_local_importance": compute_local_importance,
    "generate_perturbations": generate_perturbations,
}

context_lime_actual = {
    "model": model,
    "input_data": X_test[0].unsqueeze(0),  # Select the first data point for explanation
    "num_perturbations": 100,
    "variance": 1,
    "features": X_test,  # Assuming the entire test set represents the feature set
    "fit_linear_model": fit_linear_model,
    "compute_local_importance": compute_local_importance,
    "generate_perturbations": generate_perturbations,
}

# Define the formula for LIME with perturbation
formula_str_lime = '''compute_local_importance(fit_linear_model(generate_perturbations(input_data, num_perturbations, variance, model)), features)'''

# Compile the formula
compiled_operation_lime = compile_formula_revised(formula_str_lime, context_lime_conceptual)

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
print(compiled_operation_lime.print_attributes_and_return_object("model").trace)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print(compiled_operation_lime.print_attributes_and_return_object("compute_local_importance").trace)

# Print all existing elements
for i in compiled_operation_lime.all_existing_elements:
    print(i.id)

# Execute the operation for the actual context
result_lime_actual = execute_operation(compiled_operation_lime, context_lime_actual)
print("Actual Result:", result_lime_actual)
