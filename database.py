import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage

# Use a service account
cred = credentials.Certificate('parking-vision-1-ae16cad5a5ad.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

client = storage.Client()
bucket = client.get_bucket('gs://parking-vision-1.appspot.com/')
blob = bucket.blob('2020-09-23 16:50:51.814074.png')
blob.upload_from_string('this is test content!')

# for i in range(113):
#     doc_ref = db.collection(u'couch_parking_spots').document(u'spot'+str(i))
#     doc_ref.set({
#         u'status': u'open'
#     })

users_ref = db.collection(u'couch_parking_spots')
docs = users_ref.stream()

spots_ref = {}
for doc in docs:
    dic = doc.to_dict()
    spots_ref[doc.id] = dic['status']

def set_spot_status(status, spotId):
    spots_ref[spotId] = status
    doc_ref = db.collection(u'couch_parking_spots').document(spotId)
    doc_ref.set({
        u'status': status
    })

