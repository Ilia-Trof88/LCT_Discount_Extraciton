from flask import Flask, render_template, request, render_template, jsonify, redirect
from transformers import pipeline, BertTokenizerFast, BertForTokenClassification
import torch
model_name = r"C:\Users\Ilia\Desktop\Проект Питон\app\Final_Model_Director_10.06.24" #Заменить на директорию, де лежит модель
tokenizer = BertTokenizerFast.from_pretrained(model_name)
model = BertForTokenClassification.from_pretrained(model_name)


device = torch.device("cpu") #Если пилим веб-сервис, лучше поставить cpu, вероятно
model.to(device)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple", device=0 if torch.cuda.is_available() else -1) #арг -1 можно убр.

def entity_extraction(text, tokenizer, ner_pipeline, max_length=512):
    tokens = tokenizer(text, truncation=True, max_length=max_length, return_tensors="pt")
    truncated_text = tokenizer.decode(tokens["input_ids"][0], skip_special_tokens=True)
    predictions = ner_pipeline(truncated_text)
    return predictions

app = Flask(__name__)


# перенаправление на страницу ввода
@app.route("/")
def main_page():
    return redirect("/input")


@app.route("/input", methods=["GET"])
def input_page():
    return render_template("index.html")


@app.route("/input", methods=["POST"])
def get_input():
    example_text = request.get_json()["phrase"]

    # example = 'прекрасный пример полного отсутствия мозга'
    predictions = entity_extraction(example_text, tokenizer,
                                    ner_pipeline)  # вот тут как раз фигурирует example_text кот нужно заменять
    s=''
    for prediction in predictions:
        s=s+f"Слово: {prediction['word']}, Метка: {prediction['entity_group']}, Score: {prediction['score']:.4f} \n"

    return jsonify({"message": s})  # тут фразу заменить на результат


# запуск приложения
if __name__ == "__main__":
    app.run(debug=True)

'''


model_name = "/home/work5/reviews/Second_Model/Fourth_Model_Early_Stopping_Applied" #Заменить на директорию, де лежит модель
tokenizer = BertTokenizerFast.from_pretrained(model_name)
model = BertForTokenClassification.from_pretrained(model_name)


device = torch.device("cuda") #Если пилим веб-сервис, лучше поставить cpu, вероятно
model.to(device)


ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple", device=0 if torch.cuda.is_available() else -1) #арг -1 можно убр.


example_text = df['processed_text'][10] #Здесь example_text - это именно пользовательский ввод, так что наверное как-то заменять необходимо

# Функция для предсказаний с учетом максимальной длины == 512
def entity_extraction(text, tokenizer, ner_pipeline, max_length=512):

    tokens = tokenizer(text, truncation=True, max_length=max_length, return_tensors="pt")
    truncated_text = tokenizer.decode(tokens["input_ids"][0], skip_special_tokens=True)


    predictions = ner_pipeline(truncated_text)

    return predictions


predictions = entity_extraction(example_text, tokenizer, ner_pipeline) #вот тут как раз фигурирует example_text кот нужно заменять


for prediction in predictions:
    print(f"Слово: {prediction['word']}, Метка: {prediction['entity_group']}, Score: {prediction['score']:.4f}")
'''