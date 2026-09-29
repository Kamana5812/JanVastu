import pytest
from app.services.ai_service import analyze,redact
CASES={
 "water":["water supply failed","the pipe is broken","the pump is not working","हमारे गाँव में पानी नहीं है","ଆମ ଗାଁରେ ପାଣି ନାହିଁ"],
 "road":["the road is damaged","there is a pothole","sadak kharab hai","हमारी सड़क टूट गई","ଆମ ରାସ୍ତା ଖରାପ"],
 "health":["the hospital needs staff","the clinic is closed","there is no doctor here","अस्पताल बंद है","ଡାକ୍ତର ନାହାନ୍ତି"],
 "school":["the school is closed","we need a teacher","education facilities needed","विद्यालय की मरम्मत चाहिए","ବିଦ୍ୟାଳୟ ମରାମତି ଦରକାର"],
 "electricity":["electric supply failed","there is a power outage","street light is broken","बिजली नहीं आती","ବିଜୁଳି ନାହିଁ"],
 "sanitation":["garbage is piled up","waste collection stopped","the drain is blocked","कचरा उठाएँ","ଆବର୍ଜନା ଉଠାନ୍ତୁ"],
 "transport":["we need a bus service","public transport is missing","traffic is congested","परिवहन सुविधा चाहिए","ଯାତାୟାତ ସୁବିଧା ଦରକାର"],
 "housing":["house repair needed","housing assistance needed","shelter is needed","आवास चाहिए","ଘର ଦରକାର"]}
@pytest.mark.parametrize("category,text",[(category,text) for category,examples in CASES.items() for text in examples])
def test_category_samples(category,text):
    assert category in analyze(text)["categories"]
def test_multilabel_and_redaction():
    result=analyze("The water pipe and road both need repair.")
    assert {"water","road"}<=set(result["categories"])
    assert "person@example.org" not in redact("Contact person@example.org or +91 98765 43210.")
    assert "98765" not in redact("Call +91 98765 43210.")
