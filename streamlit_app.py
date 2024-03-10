import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

import json

# Authenticate to Firestore with the JSON account key.
# db = firestore.Client.from_service_account_json("streamlit-reddit-d67b6-firebase-adminsdk-jas86-070b8ec8c2.json")

key_dict = json.loads(st.secrets["textkey"])
print(key_dict)
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="streamlit-reddit-d67b6")

# Streamlit widgets to let a user create a new post
title = st.text_input("Post title")
url = st.text_input("Post url")
submit = st.button("Submit new post")

# Once the user has submitted, upload it to the database
if title and url and submit:
	doc_ref = db.collection("posts").document(title)
	doc_ref.set({
		"title": title,
		"url": url
	})

# And then render each post, using some light Markdown
posts_ref = db.collection("posts")
for doc in posts_ref.stream():
	post = doc.to_dict()
	title = post["title"]
	url = post["url"]

	st.subheader(f"Post: {title}")
	st.write(f":link: [{url}]({url})")


# # This time, we're creating a NEW post reference for Apple
# doc_ref = db.collection("posts").document("Apple")

# # And then uploading some data to that reference
# doc_ref.set({
# 	"title": "Apple",
# 	"url": "www.apple.com"
# })

# # Now let's make a reference to ALL of the posts
# posts_ref = db.collection("posts")

# # For a reference to a collection, we use .stream() instead of .get()
# for doc in posts_ref.stream():
# 	st.write("The id is: ", doc.id)
# 	st.write("The contents are: ", doc.to_dict())


# st.header('Hello 🌎!')
# if st.button('Balloons?'):
#     st.balloons()
