import re

# -------------------------
# Essential Elements Section
# -------------------------

class Element:
    all_elements = {}
    element_count = 0  # To keep track of the number of elements

    def __init__(self, **kwargs):
        self.innate_name = self.__class__.__name__.lower()
        self.name = kwargs.get('name', self.innate_name).lower()  # Default to innate_name if name is None
        self.trace = kwargs.get('trace', self.innate_name).lower()  # Initially, the trace is just the innate name
        self.source_operation = kwargs.get('source_operation', None)
        self.listability = kwargs.get('listability', "complete")  # Default value
        self.model_specific = kwargs.get('model_specific', False)
        self.interactive_parameter = kwargs.get('interactive_parameter', None)
        self.contain_non_trivial_value = kwargs.get('contain_non_trivial_value', True)
        self.used_in_operatetion = None
        self.loop_conceptual = False
        self.loop_complete = False
        self.auxillary = False
        # Generate unique ID for the element
        Element.element_count += 1
        self.id = f"{self.innate_name}_{Element.element_count}"
        
        existing_element = Element.all_elements.get((self.name, self.trace))
        if existing_element:
            return existing_element
        Element.all_elements[(self.name, self.trace)] = self

    def __str__(self):
        return self.name if self.name is not None else self.innate_name


    def __str__(self):
        return self.name if self.name is not None else self.innate_name

class model(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"
    
#class model_strcture()
    
#class model_feature()

class Model(Element): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"
    
class Value(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Data(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class Auxillary_model(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"
        self.auxillary = True

class Model_runLog(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"
        
class FAI_Index(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class FAI_Number(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"
        


class Layer(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class Neuron(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class Weight(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class Bias(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class ActivationFunction(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class InputData(Data):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class OutputData(Data):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class SegOutputData(OutputData):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class LossFunction(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class Optimizer(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class Regularizer(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class Dropout(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class BatchNormalization(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class ConvolutionalLayer(Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class PoolingLayer(Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class RecurrentLayer(Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class TransformerBlock(Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class QueryVector(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class KeyValueVector(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class AttentionMechanism(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

# -------------------------
# Output Generation Section
# -------------------------

class OutputLayer(Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class OutputNeuron(Neuron):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class OutputData(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

# -------------------------
# Model Structure Section
# -------------------------

class InputLayer(Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class HiddenLayer(Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class TransformerLayer(Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class Block(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class Branch(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class Circuit(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

# -------------------------
# Training-Related Section
# -------------------------

class GradientFunction(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class InputGradient(GradientFunction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class WeightGradient(GradientFunction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class BiasGradient(GradientFunction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class ActivationRepresentation(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_specific = True
        self.listability = "individual"

class InputActivationRepresentation(ActivationRepresentation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class OutputActivationRepresentation(ActivationRepresentation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"


# -------------------------
# Input Representation Section
# -------------------------

class ImageRepresentation(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class PixelValue(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class PixelToken(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class TextRepresentation(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class WordToken(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class CharacterToken(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class PositionalEncoding(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class GraphRepresentation(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class AudioRepresentation(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class TimeSeriesRepresentation(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

# -------------------------
# Weight and Activation Representation Section
# -------------------------

class WeightRepresentation(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class ActivationRepresentation(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_specific = True
        self.listability = "individual"

class InputWeightRepresentation(WeightRepresentation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class OutputWeightRepresentation(WeightRepresentation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class InputActivationRepresentation(ActivationRepresentation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class OutputActivationRepresentation(ActivationRepresentation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

# -------------------------
# Additional Sections Expanded
# -------------------------

class Attention(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class SelfAttention(Attention):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class CrossAttention(Attention):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class MultiHeadAttention(Attention):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class AttentionMaps(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class Tokenization(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class Embeddings(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class SequenceModeling(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class FeatureMaps(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class ImageEmbeddings(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"

class ConvolutionalBlocks(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listability = "individual"









#Lime
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
