**Overview of Interpretability Methods Formalized Encoding**

This project aims to manifest the characteristics of interpretability methods in deep learning by encoding these methods into formal formulas using Python classes. Each element related to deep learning and the computations required for any interpretability method is represented by a Python class. Every method is represented by a tree structure of operations on these elements within a model or computed elements, where each node is an element (the output of computation is also considered an element).

The motivation behind this project extends beyond systematically providing a uniform and formalized representation of all existing methods. It includes automatically and formally providing explanations and other information about a method, such as its complexity, required input, etc. Here is a list of classifications for these methods that we aim to extract from the formula:
- Global vs. Local
- Model-specific vs. Model-agnostic
- Data-dependent vs. Data-independent
- Intrinsic vs. Post-hoc
- Quantitative vs. Qualitative
- Deterministic vs. Stochastic
- Transparent vs. Opaque
- Analytical vs. Empirical
- Static vs. Interactive
- Explanatory vs. Exploratory
- Singular vs. Comparative
- Causal vs. Correlational
- Deterministic vs. Heuristic
- Manual vs. Automated
- Structural vs. Behavioral
- Sensitivity-based vs. Fidelity-based
- Innate vs. Extraneous

Additional key functions include the ability to perform a random walk on what the system can possibly do with the deep learning model in the post hoc interpretability process, to see whether it can come up with helpful methods given constraints such as complexity and data used. Another feature is using generative sequence models, like Tree-RNNs, to generate new interpretability methods.

We also aim to extract method evaluations, such as the robustness of the method.

**Organization of This Work**

- `elements.py` defines all elements from the model, with a key attribute being their data type and shape. Some elements have different forms, such as weights, which can be represented both as a list and a matrix. However, its list nature can be ignored if the system works fine without it, e.g., if letting a matrix be compatible with all the computations on a list is sufficient.

- `dlc.py` (Deep Learning Component) includes some basic classes in the deep learning process such as model, model_input, model_output, and model_log. Their attributes are often elements defined in `elements.py`, and these basic classes are inherited from elements.

- `computations.py` defines all important functions or computations, each having an output that is an element. For example, `model_run`, one of the most often-used computations in this system, will have the type or output of element model_output and model_log, where the input is model and model_input. To use a particular output of model_log, such as the activation of a neuron, several functions of the type inherited from function, like select, will be used. When creating a computation or functions, the input type needs to be specified, and an output instance of a certain type is automatically created.

- `find_particular_neuron(neuron)` outputs a neuron index or location, and `select_particular_value(model_log, find_particular_neuron(neuron))` completes the task. Here, `find_particular_neuron` has a type (or output type) index (inherited from number, used only for finding things) with an attribute range which is an element such as model_neurons or model_weights, all list type elements, in which the index can be applied as a locator. `select_particular_value` has a type number or activation_number inherited from number.

- `model_run` is a special type of computation since it outputs two high-level elements, which include many other elements.

When defining a formula, the formula is essentially linked by many elements in its tree-shaped data type, but many of these elements are the output of a computation. Thus, when defining a node in a formula, or an operation, the system automatically checks whether the element inputted is valid, whether the output is valid, and whether the computation defined can produce the output from the input, using their type, shape, and working range.

- `number.py`, an inherited class from elements, defines all types of numbers and their ranges and possible associations with other elements, such as probability, constant, activation, etc.

Instead of using `[]`, we utilize different types of select, argmin, max, etc., and other conditional selections. For getting an attribute of an element, we also have a child class `get_attribute` inherited from method, and other

 functions like select also work in the same way to maintain formality while being understandable at the same time.

