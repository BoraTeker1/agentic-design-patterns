from dotenv import load_dotenv
from openai import OpenAI
import json
import os
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

client = OpenAI()
MODEL = "text-embedding-3-small"



def embedding(text: str) -> list[float]:
    #converting a sentence into a numerical vectors. 
    response = client.embeddings.create(
        model=MODEL,
        input= text,
        encoding_format="float"
    )

    return response.data[0].embedding

references = {
    "coding": [
        "Help me debug a Python function that produces incorrect results.",
        "Write a JavaScript function that sorts an array of objects.",
        "Explain why my application crashes when executing this code.",
        "Optimize a SQL query that takes too long to execute.",
        "Review my program and suggest improvements to its implementation."
    ],
    "research": [
        "Research current trends in artificial intelligence and summarize the findings.",
        "Compare different cloud computing providers using reliable sources.",
        "Find academic studies investigating the effects of remote work.",
        "Analyze market trends and prepare a report using publicly available data.",
        "Investigate the advantages and disadvantages of different database technologies."
    ],
    "support": [
        "I need assistance recovering access to my customer account.",
        "Help me resolve an unexpected charge on my subscription.",
        "I want to contact customer support about my recent purchase.",
        "My order hasn't arrived and I need help tracking the delivery.",
        "I am having trouble updating my billing information."
    ]
}




cache_file = "eval_data/reference_embeddings.json"
if os.path.exists(cache_file):
    with open(cache_file, "r") as file:
        reference_embeddings = json.load(file)
else:
    reference_embeddings = {
    "coding": [],
    "research": [],
    "support": []
}




for category, sentences in references.items():
    for sentence in sentences:
        vector = embedding(sentence)
        reference_embeddings[category].append(vector)
    

with open(cache_file, "w") as file:
    json.dump(reference_embeddings, file)

MIN_SIMILARITY = 0.20
MIN_MARGIN = 0.08

def embedding_route(request: str) -> str:
    category_stores = {
    }
    request_vector = embedding(request)
    for category, vectors in reference_embeddings.items():
        similarity = cosine_similarity([request_vector], vectors)
        category_stores[category] = float(similarity.mean())


    #i am sorting categories by similarity
    sorted_scores = sorted(
        category_stores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    best_category, best_score = sorted_scores[0]
    second_score = sorted_scores[1][1]
    margin = best_score - second_score


    print(f"\nRequest: {request}")
    print(f"Category scores: {category_stores}")
    print(f"Best score: {best_score:.3f}")
    print(f"Margin: {margin:.3f}")

    print(f"Below similarity threshold: {best_score < MIN_SIMILARITY}")
    print(f"Below margin threshold: {margin < MIN_MARGIN}")

    if best_score < MIN_SIMILARITY or margin < MIN_MARGIN:
        predicted_category = "unclear"
    else:
        predicted_category = best_category

    return predicted_category



if __name__ == "__main__":
    requests = [
        "Fix my Python IndexError",
        "Compare AWS and Azure pricing",
        "I need help recovering my account",
        "My application isn't working. Can you help?"
    ]

    for request in requests:
        print("Prediction:", embedding_route(request))
