from io import BytesIO
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from fastapi import HTTPException
from minio import Minio
from minio.error import S3Error
from urllib3 import PoolManager,Timeout
from urllib3.exceptions import HTTPError
from PIL import Image, UnidentifiedImageError
from app.core.config import settings

def get_minio_client():
    if not settings.MINIO_ACCESS_KEY or not settings.MINIO_SECRET_KEY:
        raise HTTPException(503,"storage_unavailable")
    return Minio(settings.MINIO_ENDPOINT,access_key=settings.MINIO_ACCESS_KEY,
                 secret_key=settings.MINIO_SECRET_KEY,secure=settings.MINIO_SECURE,
                 region=settings.MINIO_REGION or None,
                 http_client=PoolManager(timeout=Timeout(connect=3,read=10),retries=1))

def validate_media(raw,content_type):
    if not raw or len(raw)>settings.MAX_UPLOAD_BYTES:
        raise HTTPException(413,"media_too_large")
    if content_type in ("image/jpeg","image/png","image/webp"):
        try:
            image=Image.open(BytesIO(raw));image.verify()
            image=Image.open(BytesIO(raw));image.thumbnail((2400,2400))
            output=BytesIO();image.convert("RGB").save(output,format="JPEG",quality=85)
            return output.getvalue(),"image/jpeg",".jpg"
        except (UnidentifiedImageError,ValueError,OSError,Image.DecompressionBombError):
            raise HTTPException(400,"invalid_media")
    if content_type in ("video/mp4","video/webm","audio/webm","audio/ogg","audio/wav","audio/mpeg"):
        probe=shutil.which("ffprobe")
        if not probe: raise HTTPException(503,"media_validation_unavailable")
        suffix=".webm" if "webm" in content_type else ".mp4" if "mp4" in content_type else ".bin"
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/("evidence"+suffix);path.write_bytes(raw)
            try:
                result=subprocess.run([probe,"-v","error","-show_format","-show_streams","-of","json",str(path)],capture_output=True,timeout=10,check=True)
                info=json.loads(result.stdout)
                duration=info.get("format",{}).get("duration")
                if duration is None:
                    packets=subprocess.run([probe,"-v","error","-show_entries","packet=pts_time,duration_time","-of","json",str(path)],capture_output=True,timeout=10,check=True)
                    rows=json.loads(packets.stdout).get("packets",[])
                    duration=max((float(p.get("pts_time",0))+float(p.get("duration_time",0)) for p in rows),default=0)
                duration=float(duration)
                if duration<=0 or duration>60: raise HTTPException(400,"media_duration_limit")
                streams=info.get("streams",[])
                expected="video" if content_type.startswith("video") else "audio"
                if not any(s.get("codec_type")==expected for s in streams): raise HTTPException(400,"invalid_media")
            except (subprocess.SubprocessError,KeyError,ValueError):
                raise HTTPException(400,"invalid_media")
        return raw,content_type,suffix
    raise HTTPException(400,"unsupported_media")

def put_media(key,raw,content_type):
    try:
        client=get_minio_client()
        if not client.bucket_exists(settings.MINIO_BUCKET): client.make_bucket(settings.MINIO_BUCKET)
        client.put_object(settings.MINIO_BUCKET,key,BytesIO(raw),len(raw),content_type=content_type)
    except (S3Error,HTTPError,OSError):
        raise HTTPException(503,"storage_unavailable")

def read_media(key):
    try: return get_minio_client().get_object(settings.MINIO_BUCKET,key)
    except (S3Error,HTTPError,OSError): raise HTTPException(404,"media_unavailable")
