def create(client,payload): return client.post('/api/admin/projects',json=payload,headers={'X-Admin-Key':'test-key'})
def test_admin_create_requires_key(client,payload): assert client.post('/api/admin/projects',json=payload).status_code==401
def test_create_list_search_and_filters(client,payload):
 r=create(client,payload); assert r.status_code==201; slug=r.json()['slug']
 assert client.get('/api/projects',params={'q':'Test'}).json()['total']==1
 assert client.get('/api/projects',params={'state':'Gujarat','status':'APPROVED'}).json()['items'][0]['slug']==slug
 assert client.get(f'/api/projects/{slug}').json()['sources'][0]['publisher']=='PIB'
def test_updates_create_history(client,payload):
 slug=create(client,payload).json()['slug']; response=client.patch(f'/api/admin/projects/{slug}',json={'status':'UNDER_CONSTRUCTION','investment_inr':10},headers={'X-Admin-Key':'test-key'})
 assert response.status_code==200; changes=client.get('/api/changes').json(); assert {x[0]['field_name'] for x in changes}=={'status','investment_inr'}
def test_invalid_production_date(client,payload):
 payload['expected_production_date']='2023-01-01'; assert create(client,payload).status_code==422
