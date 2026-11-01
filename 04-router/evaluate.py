
import json
from router import route
from embedding_router import embedding_route
import time

with open('eval_data/requests.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


test_data = data

res = []

for i, v in enumerate(test_data):
    input = v['input']
    expected_category = v['expected_category']
    test_number = i + 1

    
    before = time.perf_counter()
    prediction = route(input)
    after = time.perf_counter()

    latency = after - before

    
    before = time.perf_counter()
    embedding_prediction = embedding_route(input)
    after = time.perf_counter()

    embedding_latency = after - before

    res.append(
        {
            "input": input,
            "expected_category": expected_category,
            "test_number": test_number,
            "correct": prediction.category == expected_category,
            "latency": latency,
            "predicted_category": prediction.category,
            "confidence": prediction.confidence,
            "embedding_correct": embedding_prediction == expected_category,
            "embedding_latency": embedding_latency,
            "embedding_prediction": embedding_prediction
        }
    )



calc_true = 0
calc_false = 0

for i in range(len(res)):
    correct = res[i]['correct']

    if correct == True:
        calc_true += 1
    else:
        calc_false += 1

accuracy = (calc_true / len(res)) * 100


count = 0

for i in range(len(res)):
    latency = res[i]['latency']
    count += latency

average_latency = count / len(res)



embedding_true = 0
embedding_false = 0

for i in range(len(res)):
    correct = res[i]['embedding_correct']

    if correct == True:
        embedding_true += 1
    else:
        embedding_false += 1

embedding_accuracy = (embedding_true / len(res)) * 100


# Embedding average latency
embedding_count = 0

for i in range(len(res)):
    latency = res[i]['embedding_latency']
    embedding_count += latency

embedding_average_latency = embedding_count / len(res)


print(f"Total requests: {len(res)}")

print("\n--- LLM Router ---")
print(f"Correct predictions: {calc_true}")
print(f"Incorrect predictions: {calc_false}")
print(f"Accuracy: {accuracy:.2f}%")
print(f"Average latency: {average_latency:.3f} seconds")

print("\n--- Embedding Router ---")
print(f"Correct predictions: {embedding_true}")
print(f"Incorrect predictions: {embedding_false}")
print(f"Accuracy: {embedding_accuracy:.2f}%")
print(f"Average latency: {embedding_average_latency:.3f} seconds")



print("\n--- Incorrect Predictions ---")

for i in range(len(res)):
    if res[i]['correct'] == False or res[i]['embedding_correct'] == False:
        print(f"\nTest {res[i]['test_number']}")
        print(f"Expected: {res[i]['expected_category']}")
        print(f"LLM predicted: {res[i]['predicted_category']}")
        print(f"Embedding predicted: {res[i]['embedding_prediction']}")



#in conclusion, i can use llm router when accurracy matters. 
#its better to use embedding router when latency and cost is important and requests follow 
#predictable categories.