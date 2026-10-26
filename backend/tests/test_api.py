from datetime import datetime, timezone
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from app.models import Preferences, Day, Trip
from app.main import app, identity

client = TestClient(app)
def prefs(**changes):
    return dict(destination='Kyoto, Japan',start_date='2026-11-13',end_date='2026-11-15',budget=900,currency='USD',group_size=2,style='Relaxed',interests=['Food'],**changes)

def test_reversed_dates():
    p=prefs();p['end_date']='2026-11-12'
    with pytest.raises(ValidationError): Preferences(**p)

def test_long_trip():
    p=prefs();p['end_date']='2026-12-15'
    with pytest.raises(ValidationError): Preferences(**p)

def test_invalid_budget():
    p=prefs();p['budget']=-1
    with pytest.raises(ValidationError): Preferences(**p)

def test_overlapping_schedule():
    a=dict(time='09:00',title='Breakfast',category='Dining',description='Cafe',duration=90,cost=10,location='Kyoto')
    with pytest.raises(ValidationError):
        Day(day=1,title='City',activities=[a,a],accommodation={'name':'Hotel','cost':50},transport={'description':'Walk','cost':0})

def test_health():
    assert client.get('/health').json()['status']=='ok'

def test_trip_requires_auth():
    from app.main import settings
    old=(settings.supabase_url,settings.supabase_anon_key)
    settings.supabase_url='https://example.supabase.co';settings.supabase_anon_key='test'
    try: assert client.get('/trips').status_code==401
    finally: settings.supabase_url,settings.supabase_anon_key=old

def test_trip_date_consistency():
    with pytest.raises(ValidationError):
        Trip(id=uuid4(),title='Trip',summary='Summary',source='ai',days=[],preferences=prefs(),created_at=datetime.now(timezone.utc))

def test_storage_scoped_to_authenticated_owner(monkeypatch):
    import app.main as main
    seen=[]
    async def mock_db(method,user,trip_id=None,body=None):
        seen.append(user['id']);return []
    app.dependency_overrides[identity]=lambda:{'id':'owner-id','headers':{}}
    monkeypatch.setattr(main,'database',mock_db)
    try:
        assert client.get('/trips').json()==[]
        assert seen==['owner-id']
    finally: app.dependency_overrides.clear()
