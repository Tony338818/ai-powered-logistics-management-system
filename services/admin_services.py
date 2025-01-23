import json
import os
import shipping as sh
import shared_services as ss
import tracking as t

# Users
users = ss.load_users()
    
def update_users_details(user_id, updates):
    ss.update_user_details(user_id, updates)

def remove_user(user_id):
    ss.remove_user(user_id)




update_users_details('a553b1ac-c3cb-11ef-af06-ccd9ac1c0538')

