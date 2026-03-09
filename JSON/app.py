import streamlit as st
import json
import os

# Safe file loading (professional way)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
schema_path = os.path.join(BASE_DIR, "form_schema.json")

with open(schema_path) as f:
    schema = json.load(f)

st.title(schema["title"])

# Use session state (important in Streamlit)
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

if "errors" not in st.session_state:
    st.session_state.errors = {}

form_data = st.session_state.form_data
errors = st.session_state.errors

# Render fields dynamically
for field in schema["fields"]:
    field_type = field["type"]
    name = field["name"]
    label = field["label"]

    if field_type == "text":
        value = st.text_input(
            label,
            value=form_data.get(name, ""),
            key=name
        )
        form_data[name] = value

    elif field_type == "select":
        options = [""] + field["options"]
        value = st.selectbox(
            label,
            options,
            index=options.index(form_data.get(name, "")) if form_data.get(name, "") in options else 0,
            key=name
        )
        form_data[name] = value

# Submit logic
if st.button("Submit"):

    errors.clear()

    for field in schema["fields"]:
        if field.get("required") and not form_data.get(field["name"]):
            errors[field["name"]] = f"{field['label']} is required"

    if errors:
        for err in errors.values():
            st.error(err)
    else:
        st.success("Form Submitted Successfully!")
        st.write("Submitted Data:", form_data)