import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# ✅ Prevent duplicate initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-service-account.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ✅ Helper Functions (used in main.py)
def get_session(session_id: str):
    """Fetch session data from Firestore"""
    try:
        doc = db.collection("chat_sessions").document(session_id).get()
        return doc.to_dict() if doc.exists else None
    except Exception as e:
        print(f"[Memory] Error in get_session: {e}")
        return None

def update_session(session_id: str, updates: dict):
    """Update existing session"""
    try:
        db.collection("chat_sessions").document(session_id).update(updates)
    except Exception as e:
        print(f"[Memory] Error in update_session: {e}")

def create_new_session(session_id: str, initial_data: dict):
    """Create new session"""
    try:
        db.collection("chat_sessions").document(session_id).set(initial_data)
    except Exception as e:
        print(f"[Memory] Error in create_new_session: {e}")

# ✅ OOP-based session memory (Optional but used in other parts of your app)
class ConversationMemory:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = self._get_session()

    def _get_session(self):
        """Fetch session from Firestore or create a new one"""
        try:
            doc_ref = db.collection('chat_sessions').document(self.user_id)
            doc = doc_ref.get()

            if doc.exists:
                session = doc.to_dict()
                if datetime.now() - session.get('last_updated', datetime.now()) > timedelta(minutes=30):
                    return self._create_new_session()
                return session
            else:
                return self._create_new_session()
        except Exception as e:
            print(f"[Memory] Error getting session: {e}")
            return self._create_new_session()

    def _create_new_session(self):
        """New session structure"""
        return {
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a helpful flight booking assistant. Keep responses concise and friendly. Always confirm details before proceeding with bookings.'
                }
            ],
            'context': {
                'origin': None,
                'destination': None,
                'departure_date': None,
                'return_date': None,
                'passengers': None,
                'booking_step': 'initial'
            },
            'last_updated': datetime.now()
        }

    def add_message(self, role, content):
        self.session['messages'].append({
            'role': role,
            'content': content
        })

    def get_messages(self):
        return self.session['messages']

    def get_context(self):
        return self.session.get('context', {})

    def update_context(self, new_context):
        self.session['context'].update(new_context)

    def save(self):
        """Save the current session to Firestore"""
        try:
            self.session['last_updated'] = datetime.now()
            db.collection('chat_sessions').document(self.user_id).set(self.session)
        except Exception as e:
            print(f"[Memory] Error saving session: {e}")
