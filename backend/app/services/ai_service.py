"""Deterministic, replaceable language and multi-label keyword analysis."""
import re
import time
from langdetect import detect, DetectorFactory, LangDetectException
from app.db.models.needs import PipelineRun
DetectorFactory.seed=0
KEYWORDS={
 "water":["water","pipe","pump","pani","paani","ପାଣି","ଜଳ","पानी","पाइप"],
 "road":["road","pothole","sadak","सड़क","गड्ढ","ରାସ୍ତା","ଗାତ"],
 "health":["health","hospital","clinic","doctor","swasth","अस्पताल","डॉक्टर","ଡାକ୍ତର","ସ୍ୱାସ୍ଥ୍ୟ"],
 "school":["school","teacher","education","vidyalay","शिक्ष","स्कूल","विद्यालय","ବିଦ୍ୟାଳୟ","ଶିକ୍ଷ"],
 "electricity":["electric","power","light","bijli","बिजली","ବିଜୁଳି","ବିଦ୍ୟୁତ"],
 "sanitation":["garbage","waste","drain","toilet","kachra","कचरा","नाली","सफाई","ଆବର୍ଜନା","ନାଳ"],
 "transport":["bus","transport","traffic","बस ","परिवहन","ବସ୍","ଯାତାୟାତ"],
 "housing":["house","housing","shelter","ghar","मकान","आवास","ଘର","ବାସଗୃହ"]}
def redact(text):
    text=re.sub(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b","[redacted]",text)
    return re.sub(r"(?<!\w)\+?\d[\d\s-]{8,}\d(?!\w)","[redacted]",text)

def analyze(text, db=None, need_id=None):
    started=time.perf_counter()
    if re.search(r"[\u0b00-\u0b7f]",text): language="or"
    elif re.search(r"[\u0900-\u097f]",text): language="hi"
    elif any(x in text.lower() for x in ["paani","pani","sadak","bijli","kachra"]): language="hi"
    else:
        try: language=detect(text)
        except LangDetectException: language="und"
    lower=text.casefold()
    signals={category:[k for k in words if k in lower] for category,words in KEYWORDS.items()}
    categories=[key for key,words in signals.items() if words] or ["other"]
    result={"language":language,"category":categories[0],"categories":categories,
            "signals":{key:words for key,words in signals.items() if words},
            "description":redact(text),"model_version":"rules-1 + langdetect-1.0.9"}
    if db is not None:
        elapsed=(time.perf_counter()-started)*1000
        db.add(PipelineRun(need_id=need_id,stage="language_and_category",model_version=result["model_version"],
            latency_ms=elapsed,success=True,language=language,category=result["category"]))
    return result
