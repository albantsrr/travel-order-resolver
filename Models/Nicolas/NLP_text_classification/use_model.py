from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

model = AutoModelForSequenceClassification.from_pretrained(r"model\disitilbert_model_30000")
tokenizer = AutoTokenizer.from_pretrained(r"model\disitilbert_tokenizer_30000")


while(1):
    print("phrase :")
    input_text = str(input())

    inputs = tokenizer(input_text, return_tensors="pt")

    with torch.no_grad():
        model.eval()
        outputs = model(**inputs)

    predictions = torch.argmax(outputs.logits, dim=1)
    if(predictions.item() == 0):
        print("la phrase ne contient pas d'itinéraire")
    elif(predictions.item() == 1):
        print("la phrase contient un itinéraire")
    print()
