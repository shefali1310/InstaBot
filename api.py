from clarifai.rest import ClarifaiApp

app = ClarifaiApp(api_key = 'f5904f1940154c2caadfe8bd7c48b20b')

model= app.models.get('food-items-v1.0')

response = model.predict_by_url(
    url = 'https://www.macheesmo.com/wp-content/uploads/2011/04/periperi1_550.jpg')
print response

