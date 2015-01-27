from lib import keybase, gpg, gmail
from pprint import pprint
import triplesec


# Log in and get session idea
user = raw_input("Username: ")
salt = keybase.get_salt(user)
salt_csrf = salt["csrf"]

pw = raw_input("Password: ")
ts = triplesec.TripleSec(key=pw)
login_reply = keybase.login(user, pw, salt["salt"], salt["session"], salt_csrf)
me = login_reply['me']
session = login_reply['session']
csrf = login_reply['csrf_token']

# keys, csrf = keybase.key_fetch(me['private_keys']['primary']['kid'], ['sign'], session)
# pub_key = me['public_keys']['primary']['bundle']

# Test code for obtaining a user's public key
# pub_key = keybase.user_pub_key('christopherburg')
# import_result = gpg.import_keys(pub_key)
# pprint(import_result.results)

# print priv_key

# priv_key = keybase.decode_priv_key(me['private_keys']['primary']['bundle'], ts)
# import_result = gpg.import_keys(priv_key)
# pprint(import_result.results)
# to = import_result.fingerprints[0]


# print gpg.list_keys(True)

# test = gpg.export_keys(to)
# print test

# enc = gpg.encrypt_msg('A simple test of encryption with downloaded keys!', to)
# print enc
#
# dec = gpg.decrypt_msg(enc, pw)
# print dec

# results, csrf = keybase.user_autocomplete('thor')
# for u in results:
#     print u['components']['username']['val']

# print "Sending encrypted email...."
# gmail.send_email('mtanous22@gmail.com', ['mtanous22@gmail.com', '<redacted>'], enc)
# print "Email away!"

# Test code for use with user lookup
lookup = 'temp'
users = []
fields = 'basics'
while lookup != '':
    lookup = raw_input("User to look up: ")
    if lookup != '':
        users.append(lookup)

status = keybase.user_lookup('domain', users, fields)
print status['status']
lookup_csrf = status['csrf_token']

# if lookup_csrf != csrf:
#     print "SALT: " + salt_csrf
#     print "LOGIN: " + csrf
#     print "LOOKUP: " + lookup_csrf
#     raise Exception("CSRF tokens are not the same!")

print "SALT: " + salt_csrf
print "LOGIN: " + csrf
print "LOOKUP: " + lookup_csrf

edit_csrf = keybase.edit_profile(session, lookup_csrf, name="Matt Tanous",
                                 bio="Anarchist working to develop a digital end-run around the state.",
                                 loc='United States')

keys, key_csrf = keybase.key_fetch(me['public_keys']['primary']['kid'], ['encrypt'])
# pub_key = me['public_keys']['primary']['bundle']


print "KEY: " + key_csrf
print "EDIT: " + edit_csrf
# keybase.kill_sessions(session, lookup_csrf)


