from Elements import * 
class Function:
    def __init__(self, computation_name, input_types, output_type, **kwargs):
        self.computation_name = computation_name
        self.input_types = input_types
        self.output_type = output_type
        # Set defaults to False unless specified in kwargs
        self.stochastic = kwargs.get('stochastic', False)
        self.trivial = kwargs.get('trivial', False)
        self.heuristic = kwargs.get('heuristic', False)
        self.implementation = kwargs.get('implementation', None)
        self.output_listability = kwargs.get('output_listability', None)
        self.mapping_type = kwargs.get('mapping_type', False)
        


    def __call__(self, inputs):
        if isinstance(self.output_type, int):
            output_type = inputs[self.output_type].__class__
        else:
            output_type = self.output_type
        input_names = [arg.__class__.__name__ for arg in inputs]
        input_names_str = ", ".join(input_names)
        output_name = f"{output_type.__name__} {self.computation_name}({input_names_str})"
        output = output_type(name=output_name)
        output_trace = f"{self.computation_name}(" + ", ".join([arg.trace for arg in inputs]) + ")"
        output.trace = output_trace
        self.assign_function_specific_attributes(output)
        return output
    
    def assign_function_specific_attributes(self, output):
        pass

    
class Get_trivial_attribute(Function):
    def __init__(self, computation_name, input_types, output_type):
        self.computation_name = computation_name
        self.input_types = input_types
        self.output_type = output_type

        
Map = Function(
    computation_name="Map", 
    input_types=[Element, Element, Element],  #first input is the computation done, or operation, it can be long, second is the individual term, the thrid is the complete term
    output_type=2
)
# function input_types can be a list of type, but sometimes it might require a list of anything, with within certain listability requirement
# for example Iou function can take any two list, so input_types= [Any, Any], but its listability requirement shall be [complete, complete] or [partial, partial]

# NN used functions

