from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Chargez le tokenizer et le modèle fine-tuné
# Chargement du tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained('model.bin')
# Phrase que vous souhaitez prédire
phrase_a_predire = "Paris est une belle ville."

# Encodage de la phrase avec le tokenizer
input_ids = tokenizer.encode(phrase_a_predire, add_special_tokens=True, max_length=128, truncation=True, padding=True, return_tensors="pt")

# Inférence
model.eval()
with torch.no_grad():
    outputs = model(input_ids)
    predicted_label = torch.argmax(outputs.logits, dim=1).item()

# Le label prédit correspond à votre classe (1 pour ville, 0 pour pas de ville)
if predicted_label == 1:
    print("La phrase contient un nom de ville.")
else:
    print("La phrase ne contient pas de nom de ville.")