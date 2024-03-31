import streamlit as st
import requests
from application import client,connect_api,api_client
from io import StringIO

extensions = [e.value for e in client.ClassificationSpecificEnum]
opensource_application = connect_api()
models_api = client.ModelsApi(api_client)
# Get models from Client
api_response = models_api.models_snapshot()
models = {model.name: model.id for model in api_response.iterable if model.cloud or model.downloaded}

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

user = st.text_area("Describe your project.",placeholder="""
Remeber to generate the best result we highly recommend:
1. Add your github repo link
2. A brief description about the project""") # Try to generate many md files and share your experience

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
  iterable = []
  for file in files:
    if file.name.split(".")[-1] not in extensions:
      st.warning(f"File type {file.name.split('.')[-1]} not supported.")
      files.remove(file) # Remove the file from the list of the files because it is not vaild
      continue
    try:
      raw = StringIO(file.getvalue().decode("utf-8"))
    except:
      st.warning(f"Error in decoding file {file.name}")
      files.remove(file) # Remove the file from the list of the files because it is not vaild
      continue
    # TODO use the file instead of the string and if the file not in the extensions use the string instead
    iterable.append(client.RelevantQGPTSeed(
        seed = client.Seed(
            type="SEEDED_ASSET",
            asset=client.SeededAsset(
                application=opensource_application,
                format=client.SeededFormat(
                  fragment = client.SeededFragment(
                    string = client.TransferableString(
                           raw = raw.read()
                    ),
                    # file = client.SeededFile(
                    #     string = client.TransferableString(
                    #       raw = raw.read()
                    #     ),
                    #     metadata=client.FileMetadata(
                    #         name = file.name,
                    #         ext=file.name.split(".")[-1],
                    #         size=file.size
                    #     )
                    ),
                ),
            ), 
        ),
    ))
  question = client.QGPTQuestionInput(
    query = prompt,  
    relevant = client.RelevantQGPTSeeds(iterable = iterable) if iterable else {"iterable": []},
    model = model_id
  )

  question_json = question.to_json()

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







