import pickle
import os
import csv

# Ensure the directory exists
os.makedirs('./method/saved_methods', exist_ok=True)

def save_object(obj, filename, function_name, description, *additional_info):
    """
    Saves an object to a file using pickle in the './method/saved_methods' directory and records metadata in 'saved_methods.txt'.

    Parameters:
    obj (any): The object to save.
    filename (str): The name of the file to save the object to.
    function_name (str): The name of the function.
    description (str): A description of the function.
    additional_info (tuple): Additional information to be recorded.
    """
    filepath = os.path.join('./method/saved_methods', filename)
    with open(filepath, 'wb') as file:
        pickle.dump(obj, file)

    # Write metadata to 'saved_methods.txt'
    metadata_filepath = os.path.join('./method/saved_methods', 'saved_methods.txt')
    file_exists = os.path.isfile(metadata_filepath)
    with open(metadata_filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            # Write header if the file does not exist
            writer.writerow(['Function Name', 'Description', 'Filename', 'Classfications', 'formula'])
        writer.writerow([function_name, description, filename] + list(additional_info))

def load_object(filename):
    """
    Loads an object from a file using pickle from the './method/saved_methods' directory.

    Parameters:
    filename (str): The name of the file to load the object from.

    Returns:
    any: The loaded object.
    """
    filepath = os.path.join('./method/saved_methods', filename)
    with open(filepath, 'rb') as file:
        obj = pickle.load(file)
    return obj

# Example usage:
# my_object = SomeClass()
# save_object(my_object, 'my_object.pkl', 'my_function', 'This is a description', 'Additional info 1', 'Additional info 2')
# loaded_object = load_object('my_object.pkl')
