import streamlit as st
import pieces_os_client as client  
import requests

# AI Client Configuration
configuration = client.Configuration(host="http://localhost:1000")
api_client = client.ApiClient(configuration)
api_instance = client.ModelsApi(api_client)

# Get models from Client
api_response = api_instance.models_snapshot()
models = {model.name: model.id for model in api_response.iterable if model.cloud or model.downloading}

# Set default model from Client
default_model_name = "GPT-4 Chat Model"
model_id = models[default_model_name]
models_name = list(models.keys())
default_model_index = models_name.index(default_model_name)

new = ''

# Web App UI 
st.title("ReadMe Generator app")

st.sidebar.title("Choose a model")
model_name = st.sidebar.selectbox("Choose a model", models_name, index=default_model_index)

user = st.text_area("Describe your project")

# prompt = "Using Git README best practices, generate ONLY the README.md file on: " + user 

prompt = f"""Act as a programmer and generate a README text for a project. 
before generating you should try to answer these questions 
1. which programing langauge does this project use
2. What is the aim of the project
3. How to achieve the best results to get the readme text
Here is a outline of what the text should be like:
1. Project Title: A brief title for the project.
2. Description: A detailed description of the project and its purpose.
3. Installation: Instructions on how to install the project and run it you can check out which programing langauge and frameworks used and how to install them.
4. Usage: Instructions on how to use the project after installation.
5. Contributing: Guidelines for how to contribute to the project.
6. Credits: Acknowledge the authors and contributors of the project.
7. License: Information about the license.
The files provided to you please use them to generate the most relevant text for the README file.
Here is a quick breif about the project also:{user}"""

files = st.file_uploader("Upload a file",accept_multiple_files=True)

# Create a button for the user to generate a README file
if st.button('Generate'):
  question = client.QGPTQuestionInput(
    query = prompt,  
    relevant = {"iterable": []}, 
    model = model_id
  )

  question_json = question.json()


   # Send a Prompt request to the /qgpt/question endpoint
  response = requests.post('http://localhost:1000/qgpt/question', data=question_json)

  # Create an Instance of Question Output 
  question_output = client.QGPTQuestionOutput(**response.json())

  # Getting the answer
  answers = question_output.answers.iterable[0].text 
  st.write(answers)
  # edited_readme = st.text_area("Edit Your README: ", value=answers)


  # if st.sidebar.button('Save Your Edited README'):
  # # When the user clicks the save button, the edited response will be saved in the session state
  #   st.session_state['answer'] = edited_readme
  #   new = edited_readme 
  #   print(new)
  #   st.success("Response saved successfully!")

  #   # Let User download the response 
  #   st.sidebar.download_button(
  #         label="Download as a markdown file",
  #         data=new,
  #         file_name="README.md",
  #         mime="text/markdown",
  #     )
  
  st.sidebar.download_button(
    label="Download as a markdown file",
    data=answers,
    file_name="README.md",
    mime="text/markdown",
  )

  # if 'answers' not in st.session_state:
  #     st.session_state['answers'] = answers

  # # Function to update the session state with the new answer
  # def update_answers(new_answer):
  #     st.session_state['answers'] = new_answer

  # # Text area to edit the answer
  # new_answer = st.text_area("Edit Answer", value=st.session_state.answers, on_change=update_answers)


    


  # st.sidebar.download_button(
  #   label="Download Edited file",
  #   data=new_answer,
  #   file_name="README.md",
  #   mime="text/markdown",
  # )







