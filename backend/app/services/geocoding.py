import time
from functools import lru_cache
from threading import Lock
import httpx
from app.core.config import settings
_lock=Lock()
_last=0.0

@lru_cache(maxsize=512)
def reverse(latitude,longitude):
    global _last
    # Public Nominatim permits one request per second. Cache repeated locations.
    with _lock:
        delay=1-(time.monotonic()-_last)
        if delay>0: time.sleep(delay)
        try:
            response=httpx.get(settings.NOMINATIM_BASE_URL+"/reverse",params={
                "lat":latitude,"lon":longitude,"format":"jsonv2","addressdetails":1},
                headers={"User-Agent":settings.NOMINATIM_USER_AGENT},timeout=5)
            _last=time.monotonic()
            response.raise_for_status()
            data=response.json(); address=data.get("address",{})
            return {"address":data.get("display_name",""),"state":address.get("state",""),
                "district":address.get("state_district",address.get("county",address.get("city",""))),
                "source":"openstreetmap"}
        except (httpx.HTTPError,ValueError):
            _last=time.monotonic()
            return {"address":"","state":"","district":"","source":"user_provided"}
