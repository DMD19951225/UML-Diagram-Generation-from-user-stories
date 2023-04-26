from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from plantuml import PlantUML
from django.http import FileResponse

# Create your views here.
import spacy
from spacy import displacy
import pandas as pd
from spacy.lang.en.stop_words import STOP_WORDS
from . import use_case_diagram

def create_erd():
    # Get the file with the models.

    # Call the plantuml library to take the plantuml file and generate the png file.
    plantuml = PlantUML('http://www.plantuml.com/plantuml/img/')
    done = plantuml.processes_file(filename = './media/UML.puml', outfile = './media/schema.png')    

    # Notify the user if the process was successful.

def index(request):
    if request.method == "POST":
        input_text = json.loads(request.body)['sentence']
        use_case_diagram.result(input_text)
        create_erd()

        return JsonResponse({"url": "/media/schema.png"})
        
        # img = open('./schema.png', 'rb')
        # response = FileResponse(img)
        # return response
