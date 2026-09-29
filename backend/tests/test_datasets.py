import json
from app.db.import_datasets import DATA_PATH,import_dataset
from app.db.models.projects import Project
from app.services.decision_service import dashboard

def test_transcription_and_deduplication():
    data=json.loads(DATA_PATH.read_text(encoding="utf8"))
    assets={a["id"]:a for a in data["assets"]}
    assert len(assets)==len(data["assets"])==16
    assert len(assets["BBSR-rajmahal"]["claims"])==1
    assert set(assets["BBSR-rajmahal"]["claims"][0]["sources"])=={"image-1","image-2","image-3"}
    janpath=assets["BBSR-janpath"]
    assert "reported_cost" in janpath["conflicts"]
    assert {c["values"]["reported_duration"] for c in janpath["claims"] if "reported_duration" in c["values"]}=={"~30 Months","~36 months"}
    for asset in assets.values():
        for claim in asset["claims"]:
            assert set(claim["sources"])<=data["sources"].keys()
    assert assets["BBSR-jaydev-expressway"]["shared_budget_group"]==assets["BBSR-jaydev-flyover"]["shared_budget_group"]

def test_import_preserves_unknowns_and_existing_records(db,client,account):
    import_dataset(db);db.commit()
    assert import_dataset(db)==0
    p=db.get(Project,"BBSR-janpath")
    assert p.location is None and p.progress is None
    assert p.sanctioned_cost is None and p.actual_cost is None
    assert not p.is_sample
    payload=client.get('/api/v1/projects/BBSR-janpath').json()
    assert payload['fields']['name']['source_badge']=='User supplied — unverified'
    assert payload['fields']['actual_completion']['value'] is None
    assert payload['dataset_record']['claims'][-1]['as_of']=='2023-03-03'
    found=client.get('/api/v1/projects/search?q=Janpath').json()
    assert any(p['id']=='BBSR-janpath' and p['progress'] is None for p in found)
    nearby=client.get('/api/v1/projects/search?lat=20.3&lng=85.8').json()
    assert not any(p['id'].startswith('BBSR-') for p in nearby)
    user,_=account('national_planner')
    result=dashboard(db,user,{})
    assert all(p['latitude'] is not None for p in result['projects'])

def test_official_reference_is_field_specific(client,db):
    import_dataset(db);db.commit()
    record=client.get('/api/v1/projects/BBSR-ring-road').json()
    assert record['status']=='unverified' and record['progress'] is None
    assert record['fields']['sanctioned_cost']['value'] is None
    official=record['dataset_record']['claims'][-1]
    assert official['numeric_cost']=={'amount':8307.74,'unit':'INR crore','kind':'approved_capital_cost'}
    assert official['source_badge']=='Government Dataset'
    assert 'reported_completion' not in official['values']

