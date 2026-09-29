"""Explicit placeholder. No IIG data connection has been configured."""
def status():
    return {"name":"iig","status":"planned","records_imported":0}
if __name__=="__main__":
    print(status())
