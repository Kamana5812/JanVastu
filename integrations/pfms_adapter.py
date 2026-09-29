"""Explicit placeholder. No PFMS data connection has been configured."""
def status():
    return {"name":"pfms","status":"planned","records_imported":0}
if __name__=="__main__":
    print(status())
