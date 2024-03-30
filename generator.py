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

prompt = "Generate a professional and informative README.md file following Git best practices, for project: " + user

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







