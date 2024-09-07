import os

#FOR IMAGE PROCESSING
from PIL import Image

#By importing Streamlit, we can quickly and easily build interactive web applications 
import streamlit as st
import google.generativeai as genai

#TO LOAD THE ENVIRONMENT
from dotenv import load_dotenv

#Load environment variable from .env file if present load_dotenv()
GEMINI_API_KEY=os.environ.get("GOOGLE_API_KEY")

#OR os.getenv

genai.configure(api_key='AIzaSyDLtZosl7zU3N34nfzgMW50SH8I7aaP5BQ')

#Initialize gemini model
def initialize_model(model_name='gemini-1.5-flash'):
    model=genai.GenerativeModel(model_name)
    return model

#Here I am giving the image and it will give me the response
def get_response(model,model_behavior,img,prompt):
    response= model.generate_content([model_behavior,img[0],prompt]) #img[0] -- Will give options to send multiple image
    return response.text

#m=initialize_model()
#print(m.__class__)  ----> To print the model name / class name

#TO STUDY/READ THE IMAGE WE NEED TO CONVERT IT INTO BYTES
def get_image_bytes(uploaded_image):
    if uploaded_image is not None:
        
        #BYTES OF THE IMAGE
        image_bytes=uploaded_image.getvalue()
        
        # MIME type (Multipurpose Internet Mail Extensions type) is a standard way to specify the type of content being transmitted in a network. It's used to indicate the nature of a file or data, such as text, image, video, or audio.
        image_info=[
            {"mime_type":uploaded_image.type,"data":image_bytes}#Dictonary 
        ]
        return image_info
    else:
        #GENERATING EXCEPTION USING THE RAISE KEYWORD [IN JAVA ITS THROW KEYWORD]
        raise FileNotFoundError("Uploading of the image Failed....")#Sending it to its contructor
    
def show_response():
    #Like main() in the project
    #Model is set here
    model=initialize_model()
    
    #Create the streamlit UI
    st.set_page_config('IMAGE EXTRACTOR')
    st.header('INVOICE EXTRACTOR')
    prompt=st.text_input("Enter your prompt")
    
    #UPLOAD THE IMAGE
    upload_image=st.file_uploader('Choose an Invoice',type=["jpg","png","jpeg"])
    
    #Means it has been uploaded
    if upload_image is not None:
        image=Image.open(upload_image)
        #Lets display the image
        st.image(image,caption="YOUR IMAGE",use_column_width=True)
        
        #Lets create submit button
        submit=st.button('Submit')
        model_behavior='''
        You are an expert who understands invoice overall structures and has deep knowledge on it.
        We will upload the invoice image and you have to answer the question based on information present in the invoice image.
        '''
        
        #If user pressed the submit 
        if submit or prompt:
            #NO BLANK PROMPT
            if len(prompt)>0:
                #GET THE BYTES OF THE IMAGE
                image_info=get_image_bytes(upload_image)
                response=get_response(model,model_behavior,image_info,prompt)
                st.success(response)#OR st.write()
                
            else:
                raise ValueError("Please enter valid prompt!!")
            
#Main method i.e the entry point
'''The value of __name__ changes. It is a special keyword in python  
I. __main__ ---> when we run this current module i.e app.py then the name value is __main__.
II. When we import this class/ module to a different class then the __name__ becomes the module name when we are running that another class
'''        
if __name__=='__main__':
    show_response()
        