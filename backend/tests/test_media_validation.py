import shutil,subprocess
import pytest
from fastapi import HTTPException
from app.core.storage import validate_media
pytestmark=pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"),reason="FFmpeg is supplied in the API container")
def make_audio(path,duration):
    subprocess.run(["ffmpeg","-v","error","-f","lavfi","-i","sine=frequency=440:sample_rate=8000","-t",str(duration),str(path)],check=True,timeout=20)
def test_audio_duration_and_signature(tmp_path):
    path=tmp_path/"sample.wav";make_audio(path,1)
    raw,ctype,_=validate_media(path.read_bytes(),"audio/wav")
    assert raw and ctype=="audio/wav"
    long=tmp_path/"long.wav";make_audio(long,61)
    with pytest.raises(HTTPException) as error:validate_media(long.read_bytes(),"audio/wav")
    assert error.value.detail=="media_duration_limit"
    with pytest.raises(HTTPException):validate_media(b"invalid","audio/wav")
def test_video_and_stream_type(tmp_path):
    path=tmp_path/"sample.mp4"
    subprocess.run(["ffmpeg","-v","error","-f","lavfi","-i","color=c=blue:s=32x32:r=5","-t","1",str(path)],check=True,timeout=20)
    assert validate_media(path.read_bytes(),"video/mp4")[1]=="video/mp4"
    with pytest.raises(HTTPException):validate_media(path.read_bytes(),"audio/mpeg")
