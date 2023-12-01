import torch
from transformers import pipeline, TapasTokenizer, TapasForQuestionAnswering

model_name = "google/tapas-large-finetuned-wtq"

# load the tokenizer and the model from huggingface model hub
tokenizer = TapasTokenizer.from_pretrained(model_name)
model = TapasForQuestionAnswering.from_pretrained(model_name, local_files_only=False)

# load the model and tokenizer into a question-answering pipeline
pipe = pipeline("table-question-answering", model=model, tokenizer=tokenizer)

def get_answer(table, query):
    answers = pipe(table=table, query=query)
    print(answers['coordinates']) # FOR DEBUGGING PURPOSES
    return answers

def convert_answer(answer):
    if answer['aggregator'] == 'SUM':
      print(answer['answer']) # FOR DEBUGGING
      cells = answer['cells']
      converted = sum(float(value.replace(',', '')) for value in cells)
      return converted

    if answer['aggregator'] == 'AVERAGE':
      print(answer['answer']) # FOR DEBUGGING
      cells = answer['cells']
      values = [float(value.replace(',', '')) for value in cells]
      converted = sum(values) / len(values)
      return converted

    if answer['aggregator'] == 'COUNT':
      print(answer['answer']) # FOR DEBUGGING
      cells = answer['cells']
      converted = sum(int(value.replace(',', '')) for value in cells)
      return converted

    else:
      return answer

def get_converted_answer(table, query):
    converted_answer = convert_answer(get_answer(table, query))
    return converted_answer