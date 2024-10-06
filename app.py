from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
from pydantic import BaseModel

# Load all models from pickle files
model_files = {
    "soybeans": "./models/model_Soyabeans.pkl",
    "apple": "./models/model_apple.pkl",
    "banana": "./models/model_banana.pkl",
    "beans": "./models/model_beans.pkl",
    "coffee": "./models/model_coffee.pkl",
    "cotton": "./models/model_cotton.pkl",
    "cowpeas": "./models/model_cowpeas.pkl",
    "grapes": "./models/model_grapes.pkl",
    "groundnuts": "./models/model_groundnuts.pkl",
    "maize": "./models/model_maize.pkl",
    "mango": "./models/model_mango.pkl",
    "orange": "./models/model_orange.pkl",
    "peas": "./models/model_peas.pkl",
    "rice": "./models/model_rice.pkl",
    "watermelon": "./models/model_watermelon.pkl"
}

# Create a dictionary with descriptions
crop_descriptions = {
    "coffee": "Coffee is a tropical plant requiring a warm climate and rich soil. Sensitive to frost, it grows best at high altitudes with adequate rainfall.",
    "cotton": "Cotton thrives in warm climates with long frost-free periods. It requires well-drained, fertile soil and moderate rainfall.",
    "orange": "Oranges grow well in tropical and subtropical climates. They need well-drained soil and consistent watering during dry periods.",
    "rice": "Rice thrives in flooded conditions, particularly in tropical regions. Efficient water management and disease-resistant varieties improve productivity.",
    "maize": "Maize prefers warm temperatures and well-drained soil. Balanced fertilization and proper irrigation are important for high yields.",
    "soybeans": "Soybeans require moderate climates and fertile soil. Adequate nitrogen, phosphorus, and potassium are critical for healthy growth.",
    "beans": "Beans prefer fertile, well-drained soil and need consistent moisture and moderate temperatures for optimal growth.",
    "peas": "Peas grow best in cool, moist climates with well-drained soil rich in organic matter. Regular watering and disease management are key.",
    "groundnuts": "Groundnuts thrive in warm climates with sandy, well-drained soil. Crop rotation and proper watering during flowering are essential.",
    "cowpeas": "Cowpeas are drought-tolerant and can grow in a range of soil types. They help improve soil fertility by fixing nitrogen.",
    "banana": "Bananas require tropical climates with rich, well-drained soil and high rainfall. Regular irrigation and pest management are crucial.",
    "mango": "Mangoes grow in tropical and subtropical climates. They need deep, well-drained soil, moderate watering, and pruning for airflow.",
    "grapes": "Grapes prefer temperate climates and fertile soil. Careful pruning and pest control are crucial for healthy vines and high-quality fruit.",
    "watermelon": "Watermelons need warm temperatures and well-drained, sandy soil. Consistent watering during fruit development ensures a good yield.",
    "apple": "Apples thrive in temperate climates with well-drained, loamy soil. Proper irrigation, pruning, and pest management ensure good quality fruit."
}

# Initialize models dictionary
models = {}
for crop, file in model_files.items():
    with open(file, 'rb') as f:
        models[crop] = pickle.load(f)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://farmz-gx1n.onrender.com"],  # React's port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

@app.post("/predict")
def predict(input_data: CropInput):
    input_list = [[
        input_data.N, input_data.P, input_data.K,
        input_data.temperature, input_data.humidity,
        input_data.ph, input_data.rainfall
    ]]
    
    predicted_crops = []

    # Check each model for prediction
    for crop, model in models.items():
        prediction = model.predict(input_list)
        if prediction[0] == 1:  
            predicted_crops.append(crop)

    final_text = ""

    # Append descriptions of predicted crops
    for crop in predicted_crops:
        final_text += f"{crop.capitalize()} can be cultivated in this area.\n {crop_descriptions[crop]}\n\n"
    
    if final_text == '':
        final_text = 'Unfortunately,\n\nThere are two possibilities:\n\n 1. Your data is incorrect (negative factual)\n\n 2. Your area is unstable for most of the crops'
    print(final_text) #
    return {"predicted_crops": final_text}























# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import pickle
# from pydantic import BaseModel

# # Load the model from the pickle file
# with open("./models/model_apple.pkl", "rb") as file:
#     model = pickle.load(file)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # React's port
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class CropInput(BaseModel):
#     N: float
#     P: float
#     K: float
#     temperature: float
#     humidity: float
#     ph: float
#     rainfall: float

# @app.post("/predict")
# def predict(input_data: CropInput):
#     input_list = [[
#         input_data.N, input_data.P, input_data.K,
#         input_data.temperature, input_data.humidity,
#         input_data.ph, input_data.rainfall
#     ]]
    
#     print(f"Input data: {input_list}")
    
#     # Make prediction using the loaded model
#     prediction = model.predict(input_list)
    
#     print(f"Model prediction: {prediction}")
    
#     # Map prediction to 'apple' or 'not apple'
#     predicted_crop = "apple" if prediction[0] == 1 else "not apple"
    
#     return {"predicted_crop": predicted_crop}