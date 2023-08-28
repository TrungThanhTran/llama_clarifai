import streamlit as st
from streamlit_chat import message
import json
import llama
from PIL import Image

st.set_page_config(page_title="HOME", layout='wide')

def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": "Say something to get started!"}]
    
def make_prompt(data):
    try:
        
        instruction_1 = ". First you will receive a description of this user such as: "
        instruction_2 = ". You will output a detailed fashion guide that matches user and his/her purposes:"
        query = f" INSTRUCTION:  I want you to act as a fashionita {instruction_1}  \
            the personal information is {data['input']['physic_metric']} \
            and their personal favorite information is {data['input']['personal_choice']} \
            and their history use is {data['input']['browser_history']} \
            {instruction_2} \
            including this temple: \
            1. Suggestion outfit \
            2. Suggest event for the outfit \
            3. Reason why choose the outfit  \
            4. Illustration for the outfit in image, url link, etc \
            "
    except:
        return user_prompt
    return query

def main():
    c1, c2 = st.columns(2)
    with c1:
        original_title = '<center><p style="font-size: 80px;">FLAIR</p> \n <p>A Conent recommedation system for fashionista </p></center>'
        st.markdown(original_title, unsafe_allow_html=True)
    
    with c2:
        image = Image.open('images/icon.png')
        st.image(image, width=300)
    
    st.subheader('Select a fashionista')
    select_fashionistas = st.selectbox(
        'Select a reviewr?',
        ('', 'Bruce', 'Anastasia', 'Reese'))
    
    st.write("\n\n\n\n")
    
    if len(select_fashionistas) > 1 and select_fashionistas != None:
        with open(f'example/{select_fashionistas}.json') as f:
            data = json.load(f)
        
        if data is not None:
            input_col, output_col = st.columns(2)
            with input_col:
                # Display input data
                st.header("USER INPUT:")
                st.subheader("1. Personal information of the fashionista:")
                st.markdown(f'''**Physic metric**: {data['input']['physic_metric']}''')
                st.markdown(f'''**Personal favorite**: {data['input']['personal_choice']}''')
                st.markdown(f'''**History data**: {data['input']['browser_history']}''')
                
                st.write("\n\n\n\n")

                
                st.subheader("2. Product for the fashionista:")
                st.markdown(f'''**Description**: {data['input']['product_image_description']}''')

                image = Image.open(data['input']['product_image_path'])
                st.image(image, width=200)
            
            with st.spinner("asking LLAMA2"):
                prompt = make_prompt(data)
                response = llama.get_response(prompt)
                
                with output_col:
                    st.header("OUTPUT RECOMMENDATION:")
                    st.write(response)
                    # st.subheader("1. Suggest outfit for the fa:")
                    # for outfit in data['output']['suggest_outfit']:
                    #     st.markdown(f'''{outfit}''')
                    
                    # st.write("\n\n\n\n")

                    # st.subheader("2. Suggest event for the fashionista:")
                    # st.markdown(f'''{data['output']['suggest_event']}''')
                    
                    # st.write("\n\n\n\n")
                    
                    # st.subheader("3. Explain reasons for the fashionista:")
                    # for reason in data['output']['reason']:
                    #     st.markdown(f'''{reason}''')
                    
                    # st.write("\n\n\n\n")

                    # if data['output']['illustration'] is not None:
                    #     st.subheader("4. Illustration for the revi")
                    #     image = Image.open(data['output']['illustration'])
                    #     st.image(image, width=200)
             
if __name__ == '__main__':
    main()