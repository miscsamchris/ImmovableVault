from ImmovableVault.Models import UserProfile, Document, DocumentAccess
from datetime import date
for i in DocumentAccess.query.all():
    for j in UserProfile.query.all():
        print(i.access_to_id," ",j.user_unique_id, i.access_to_id==j.user_unique_id)
    print(date.fromisoformat(i.access_deadline))
