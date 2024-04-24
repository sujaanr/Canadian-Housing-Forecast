import math
from tensorflow import keras

# Load the pre-trained model
loaded_model = keras.models.load_model('model')

# Dictionaries for encoding categorical variables
type_encode = {
    "Condo Apartment": 0, "Co-op / Co-Ownership Apartment": 1, 
    "Condo Townhouse": 2, "Townhouse": 3, "Detached": 4, "Semi-Detached": 5
}
style_encode = {
    "Apartment": 6, "2-Storey": 7, "Bachelor/Studio": 8, 
    "Stacked Townhouse": 9, "3-Storey": 10, "Loft": 11, "Bungalow": 12
}
district_encode = {
    "W05": "district_bin_12"
}
district_int_encode = {
    "district_bin_12": 17
}
community_encode = {
    "Black Creek": "community_bin_23"
}
community_int_encode = {
    "community_bin_23": 32
}

# Normalization and addition arrays for post-processing
normalize = [1.0] * 57 
addition = [0.0] * 57 

# Example input
example_input = [
    "900-999", "Condo Apartment", "Apartment", "Black Creek", "W05", 
    2, 0, 1, 1
]

def process_input(input_data):
    try:
        output_array = [0] * 57
        output_array[type_encode[input_data[1]]] = 1
        output_array[style_encode[input_data[2]]] = 1
        output_array[13] = input_data[5]  # Bedrooms
        output_array[14] = input_data[6]  # Dens
        output_array[15] = input_data[7]  # Bathrooms
        output_array[16] = input_data[8]  # Parking Total
        output_array[community_int_encode[community_encode[input_data[3]]]] = 1
        output_array[district_int_encode[district_encode[input_data[4]]]] = 1
        square_footage = sum(map(int, input_data[0].split('-'))) / 2
        output_array[56] = math.log(square_footage)
        output_array = [num * scale + add for num, scale, add in zip(output_array, normalize, addition)]
        return [output_array]
    except Exception as e:
        print(f"Error processing input: {e}")
        return None

# Get processed array for model prediction
processed_input = process_input(example_input)
print(processed_input)

# Make prediction
if processed_input:
    prediction = loaded_model.predict(processed_input)
    predicted_price = prediction[0][0]
    print(f"Predicted Price: ${predicted_price:.2f}")
