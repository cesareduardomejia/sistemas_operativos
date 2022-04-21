
import firebase_admin 
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("sistemas-operativos-4532d-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://sistemas-operativos-4532d-default-rtdb.firebaseio.com/'
})

ref = db.reference('/')
'''ref.set({
   'Employes':
        {
            'empl': {
                'name':'cesar',
                'last_name' : 'mejia',
                'age' : '23'

            },

            'empl2' : {
                'name':'julio',
                'last_name':'mejia',
                'age':'43'
            }
        }
})'''

ref = db.reference('Employes')
emp_ref= ref.child('empl')

emp_ref.update({
    'name':'Python'
})