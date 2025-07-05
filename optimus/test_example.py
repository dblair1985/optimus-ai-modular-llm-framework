def calculate_sum(a, b):
    """Calculate the sum of two numbers"""
    result = a + b
    return result

def process_data(data_list):
    """Process a list of data"""
    processed = []
    for item in data_list:
        if item > 0:
            processed.append(item * 2)
    return processed

# Example usage
numbers = [1, 2, 3, -1, 4]
result = process_data(numbers)
print(f"Processed result: {result}")
