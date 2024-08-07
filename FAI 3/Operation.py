from Elements import *
from Functions  import *
class Operation:
    all_operations = []
    operation_count = 0  # To keep track of the number of operations

    def __init__(self, name, inputs, function):
        self.name = name
        self.inputs = self.process_inputs(inputs)
        self.function = function
        self.trace = self.construct_trace()
        self.generated_elements = []
        self.all_existing_elements = []
       
       
        self.input_trace = [input.trace for input in self.inputs]  # Track input keys
        
        self.global_finished= False
        self.model_count = 0

        self.classification = {
        "Global_vs_Local": "Global",  # use input data's listaility, or whether input data used, default global
        "Model_specific_vs_Model_agnostic": "Model_agnostic",  # whether generated model specific feature 
        "Data_dependent_vs_Data_independent": "Data_independent",  # whether data used
        "Quantitative_vs_Qualitative": None,  # output type
        "Deterministic_vs_Stochastic": "Deterministic",  # whether random select or random num used
        "Static_vs_Interactive": "Static",  # whether changable or a parameter with range of value but is random is given in direct input
        "Explanatory_vs_Exploratory": None,  # is the answer open ended or not
        "Singular_vs_Comparative": "Singular",  # number of models but not auxiliary models
        "Deterministic_vs_Heuristic": "Deterministic",  # whether things like shapely used, mark these methods as heuristic , shall I mark formula for shapely with a name like feature importance to show heuristicity?
        "Structural_vs_Behavioral": "Behavioral",  # whether model has been run, or whether all computations are done on model elements like weights
        "Sensitivity_based_vs_Fidelity_based": "Fidelity_based",  # whether thing like variance and etc thing is calculated and how they are used.
        }


        self.default_classification = {
        "Global_vs_Local": "Global",  # use input data's listaility, or whether input data used, default global
        "Model_specific_vs_Model_agnostic": "Model_agnostic",  # whether generated model specific feature 
        "Data_dependent_vs_Data_independent": "Data_independent",  # whether data used
        "Quantitative_vs_Qualitative": None,  # output type
        "Deterministic_vs_Stochastic": "Deterministic",  # whether random select or random num used
        "Static_vs_Interactive": "Static",  # whether changable or a parameter with range of value but is random is given in direct input
        "Explanatory_vs_Exploratory": None,  # is the answer open ended or not
        "Singular_vs_Comparative": "Singular",  # number of models but not auxiliary models
        "Deterministic_vs_Heuristic": "Deterministic",  # whether things like shapely used, mark these methods as heuristic , shall I mark formula for shapely with a name like feature importance to show heuristicity?
        "Structural_vs_Behavioral": "Behavioral",  # whether model has been run, or whether all computations are done on model elements like weights
        "Sensitivity_based_vs_Fidelity_based": "Fidelity_based",  # whether thing like variance and etc thing is calculated and how they are used.
        }

        # another types of function is called get_non_value_attri, which get attribute like shape or size rather than more meanful info contained in an element


        
        # Generate unique ID for the operation
        Operation.operation_count += 1
        self.id = f"{self.name}_{Operation.operation_count}"
        
        Operation.all_operations.append(self)

        
    

    def process_inputs(self, inputs):
        processed_inputs = []
        for input_item in inputs:
            if isinstance(input_item, Operation):
                processed_inputs.append(input_item)
            elif isinstance(input_item, Element):
                processed_inputs.append(input_item)
            elif isinstance(input_item, dict):
                func = input_item['function']
                input_args = input_item.get('inputs', [])
                op = Operation(func.computation_name, input_args, func)
                processed_inputs.append(op)
            else:
                raise ValueError(f"Unsupported input type: {type(input_item)}")
        return processed_inputs

    def construct_trace(self):
        input_traces = [str(arg.trace) for arg in self.inputs]
        return f"{self.name}({', '.join(input_traces)})"

    def inherit_classification(self, inputs_results):
        # Initialize the result classification as a copy of the operation's current classification
        result_classification = self.classification.copy()

        function_is_trivial = isinstance(self.function, Get_trivial_attribute)

        # If function is not trivial, check additional conditions
        if function_is_trivial:
            result_classification = self.classification
        else:
            for input_result in inputs_results:
                if input_result.source_operation:
                    source_classification = input_result.source_operation.classification
                    if input_result.source_operation.global_finished:
                        self.global_finished = True
                        result_classification["Global_vs_Local"] = "Global"
                    else:
                        if source_classification["Global_vs_Local"] == "Local":
                            result_classification["Global_vs_Local"] = "Local"

                    if  source_classification["Model_specific_vs_Model_agnostic"] == "Model_specific":
                        result_classification["Model_specific_vs_Model_agnostic"] = "Model_specific"

                    if  source_classification["Data_dependent_vs_Data_independent"] == "Data_dependent":
                        result_classification["Data_dependent_vs_Data_independent"] = "Data_dependent"
                    
                    if  source_classification["Quantitative_vs_Qualitative"] == "Qualitative":
                        result_classification["Quantitative_vs_Qualitative"] = "Qualitative"

                    if  source_classification["Deterministic_vs_Stochastic"] == "Stochastic":
                        result_classification["Deterministic_vs_Stochastic"] = "Stochastic"

                    if  source_classification["Static_vs_Interactive"] == "Interactive":
                        result_classification["Static_vs_Interactive"] = "Interactive"
                    
                    if  source_classification["Singular_vs_Comparative"] == "Qualitative":
                        result_classification["Singular_vs_Comparative"] = "Qualitative"

                    if  source_classification["Deterministic_vs_Heuristic"] == "Heuristic":
                        result_classification["Deterministic_vs_Heuristic"] = "Heuristic"

                    if  source_classification["Structural_vs_Behavioral"] == "Structural":
                        result_classification["Structural_vs_Behavioral"] = "Structural"

                    if  source_classification["Sensitivity_based_vs_Fidelity_based"] == "Sensitivity_based":
                        result_classification["Sensitivity_based_vs_Fidelity_based"] = "Sensitivity_based"

        return result_classification

    
    def update_classification(self, classification, inputs_results):
        new_classification = classification.copy()
        #Data_dependent_vs_Data_independent        
        function_is_trivial = self.function.trivial

        if function_is_trivial:
            new_classification = self.default_classification.copy()
            self.global_finished = False
            self.model_count = 0
            return new_classification


        # Example condition: Check if operation is data-based and update classification
        if any(isinstance(i, Data) for i in inputs_results):
            new_classification["Data_dependent_vs_Data_independent"] = "Data_dependent"
        # Add other conditions as needed
        #need to check whether all functions after data dependent is non trival (or at least one circuit of them is non trivials) same for the rest of the c;assificarions

        #function_is_trivial = isinstance(self.function, Get_trivial_attribute)
        
        
        #Global_vs_Local if ever we see for all data... then global
        #or if we have never see data in this operation's trace, then global
        # so original default is global, if data dependent, change to local, then check wether 
        if not self.global_finished: #if it's finished, and function not trivial, means we have used map like functions which calls on all data, thus global
            
                
                    if any((isinstance(i, Data) and i.listability == "individual" ) for i in inputs_results):
                        new_classification["Global_vs_Local"] = "Local"
                    # Example condition: Check if operation is data-based and update classification

                    if any((isinstance(i, Data) and i.listability == "complete" and self.function.computation_name == "Map") for i in inputs_results):

                        new_classification["Global_vs_Local"] = "Global"
                        self.global_finished = True

        # Model_specific_vs_Model_agnostic
        if any(i.model_specific for i in inputs_results if isinstance(i, Element) ):
            new_classification["Model_specific_vs_Model_agnostic"] = "Model_specific"

        #"Quantitative_vs_Qualitative": None,  # output type
        if any(i.contain_non_trivial_value for i in inputs_results if isinstance(i, FAI_Number)):
            new_classification["Quantitative_vs_Qualitative"] = "Qualitative"

        #"Deterministic_vs_Stochastic": None,  # whether random select or random num used
        if self.function.stochastic:
            new_classification["Deterministic_vs_Stochastic"] = "Stochastic"
       
        #"Static_vs_Interactive": None,  # whether changable or a parameter with range of value but is random is given in direct input
        if any(i.interactive_parameter for i in inputs_results if isinstance(i, Element)):
            new_classification["Static_vs_Interactive"] = "Interactive"

            
        #"Singular_vs_Comparative": None,  # number of models but not auxiliary models
        #!!!!!!!!!!! in the end counted # of models that are not auxillary
        if any(not i.auxillary for i in inputs_results if isinstance(i, Model) ):
            new_classification["Singular_vs_Comparative"] = "Comparative"

        if any((isinstance(i, Model) and i.listability != "individual" )  for i in inputs_results):
            new_classification["Singular_vs_Comparative"] = "Comparative"

        #"Deterministic_vs_Heuristic": None,  # whether things like shapely used, mark these methods as heuristic , shall I mark formula for shapely with a name like feature importance to show heuristicity?
        #!!!!! mark chunk of formula as heuristic or with simulation nature
        if self.check_heurstic():
            new_classification["Deterministic_vs_Heuristic"] = "Heuristic"
        #"Structural_vs_Behavioral": None,  # whether model has been run, or whether all computations are done on model elements like weights
        # !!!! using the instruction above
        if any((isinstance(i, Model) and i.listability != "individual" )  for i in inputs_results):
            new_classification["Structural_vs_Behavioral"] = "Structural"
        #"Sensitivity_based_vs_Fidelity_based": check if any variance based or diff taken on final steps
        # !!!
        if self.check_sensitivity():
            new_classification["Sensitivity_based"] = "True"
        return new_classification
    def check_sensitivity(self):
        return False
    def check_heurstic(self):
        return False
    def get_output_classification(self, inputs_results):
        # Step 1: Inherit classification from inputs
        inherited_classification = self.inherit_classification(inputs_results)


        # Step 2: Update classification based on operation's properties
        updated_classification = self.update_classification(inherited_classification, inputs_results)

        return updated_classification


    def execute(self):
        inputs = [inp.execute() if isinstance(inp, Operation) else inp for inp in self.inputs]
        result = self.function(inputs)
        
        # Update source_operation for elements
        for inp in self.inputs:
            if isinstance(inp, Element):
                inp.used_in_operatetion = self
        
        # Inherit existing elements from input operations and include direct input elements
        
        for inp in inputs:
            if not inp.source_operation: 
                if inp not in self.all_existing_elements:
                    self.all_existing_elements.append(inp)
            else:
                existed_elements = inp.source_operation.all_existing_elements
                for e in existed_elements:
                    if e not in self.all_existing_elements:
                        self.all_existing_elements.append(e)
                    

        # update result
        result.source_operation = self
        
        self.classification = self.get_output_classification(inputs)
        self.generated_elements.append(result)
        self.all_existing_elements.append(result)
        
        return result


    def __str__(self):
        return self.trace

    # Other methods...


    def collect_traces(self, traces=None):
        if traces is None:
            traces = []
        traces.append(self.trace)
        for input_op in self.inputs:
            if isinstance(input_op, Operation):
                input_op.collect_traces(traces)
        return traces

    @classmethod
    def get_operation_by_name(cls, name):
        for operation in cls.all_operations:
            if operation.name == name:
                return operation
        return None

    @classmethod
    def print_all_operations(cls):
        for operation in cls.all_operations:
            print(f"Name: {operation.name}")
            print(f"Trace: {operation.trace}")
            print(f"Function: {operation.function.computation_name}")
            print("\nInputs:")
            for i, input_op in enumerate(operation.inputs):
                print(f"Input {i + 1}: {input_op.name}")
            print("\n---")

    def print_tree(self, level=0, prefix=""):
        connector = "├── " if level > 0 else ""
        last_connector = "└── "
        line_prefix = "│   " * (level > 0) + prefix
        print(f"{line_prefix}{connector}{self.name}: from function -> {self.function.computation_name}")
        print(f"{line_prefix}    Function: {self.function.computation_name}")
        for i, input_op in enumerate(self.inputs):
            new_prefix = "" if (i == len(self.inputs) - 1) else "│   "
            if isinstance(input_op, Operation):
                if i == len(self.inputs) - 1:
                    input_op.print_tree(level + 1, prefix + new_prefix)
                else:
                    input_op.print_tree(level + 1, prefix + new_prefix)
            else:
                print(f"{line_prefix}{last_connector}    Direct Input: {input_op.name}")

    def collect_all_objects(self):
        all_objects = []

        def collect_objects_recursive(op):
            all_objects.append(op)
            for input_op in op.inputs:
                if isinstance(input_op, Operation):
                    collect_objects_recursive(input_op)
                else:
                    all_objects.append(input_op)

        collect_objects_recursive(self)
        return all_objects
    
    def print_name_trace_mapping(self):
        print("Name - Trace Mapping:")
        # Print all elements
        for element in Element.all_elements.values():
            print(f"Id: {element.id} | Innate Name: {element.innate_name} | Name: {element.name} | Trace: {element.trace} | Class: {element.__class__.__name__}")
        # Print all operations
        for operation in self.all_operations:
            print(f"Id: {operation.id} | Name: {operation.name} | Trace: {operation.trace} | Class: {operation.__class__.__name__}")

    def print_attributes_and_return_object(self, name):
        target_object = None

        def search_target_object(obj):
            nonlocal target_object
            if isinstance(obj, Operation) or isinstance(obj, Element):
                if obj.name == name:
                    target_object = obj
                    return
            if hasattr(obj, 'inputs'):
                for input_obj in obj.inputs:
                    search_target_object(input_obj)
            if hasattr(obj, 'generated_elements'):
                for generated_element in obj.generated_elements:
                    search_target_object(generated_element)

        search_target_object(self)

        if target_object:
            if isinstance(target_object, Operation):
                print(f"Function: {target_object.function.computation_name}")
                print("Inputs:")
                for input_op in target_object.inputs:
                    print(f"  - Name: {input_op.name}, Trace: {input_op.trace}")
            for attr_name, attr_value in target_object.__dict__.items():
                print(f"{attr_name}: {attr_value}")
            return target_object
        else:
            print(f"No object found with the name '{name}'.")
            return None
        


def compile_formula_revised(formula_str, context):
    def find_matching_parenthesis(argument_str):
        stack = []
        for i, char in enumerate(argument_str):
            if char == "(":
                stack.append(i)
            elif char == ")" and stack:
                stack.pop()
                if not stack:
                    return i
        return -1

    def process_part(part, parent_inputs):
        if part in context:
            return context[part]
        
        func_match = re.match(r"(\w+)\((.*)\)$", part)
        if func_match:
            func_name, args_str = func_match.groups()
            if func_name not in context:
                raise ValueError(f"Function {func_name} not found in context.")
            
            func = context[func_name]
            args = []

            while args_str:
                comma_index = args_str.find(',')
                parenthesis_index = args_str.find('(')

                if parenthesis_index == -1 or (comma_index < parenthesis_index and comma_index != -1):
                    next_comma = args_str.find(',')
                    if next_comma == -1:
                        next_part = args_str
                        args_str = ""
                    else:
                        next_part = args_str[:next_comma]
                        args_str = args_str[next_comma + 1:].strip()
                else:
                    end_parenthesis = find_matching_parenthesis(args_str[parenthesis_index:]) + parenthesis_index
                    next_part = args_str[:end_parenthesis + 1]
                    args_str = args_str[end_parenthesis + 2:].strip()
                
                args.append(process_part(next_part.strip(), parent_inputs))

            operation = Operation(func.computation_name, args, func)
            for arg in args:
                if isinstance(arg, Element):
                    arg.source_input = parent_inputs
            return operation
        else:
            raise ValueError(f"Unrecognized part: {part}")
    
    return process_part(formula_str.strip(), None)


class Saved_Operation:
    def __init__(self, name, operation):
        self.name = name
        self.operation = operation

