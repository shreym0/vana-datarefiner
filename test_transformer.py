import json
from refiner.transformer.zomato_transformer import ZomatoTransformer

# Test loading and validating the data
with open('input/zomato_sample.json', 'r') as f:
    data = json.load(f)
    
print('Data loaded successfully')
print('Data type:', data.get('type'))

# Test the transformer
transformer = ZomatoTransformer('test.db')
models = transformer.transform(data)
print('Transform successful, created', len(models), 'models')
for model in models:
    print(f'- {type(model).__name__}: {str(model.__dict__)}')
