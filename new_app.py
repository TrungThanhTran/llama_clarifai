import streamlit as st
from streamlit_chat import message
import llama

def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": "Say something to get started!"}]

def make_prompt(user_prompt, metadata, brand='normal brands'):
    try:
        context_data = user_prompt
        
        instruction_1 = ". First you will receive a description of this user such as: "
        instruction_2 = ". You will output a detailed fashion guide that matches user and his/her purposes:"
        query = f" INSTRUCTION:  I want you to act as a fashionita {instruction_1}  \
            the height is {metadata['height']} \
            and the size is {metadata['body_size']} \
            and gender is {metadata['gender']} \
            and skin color is {metadata['skin_color']} \
            and hair color is {metadata['hair_color']} \
            PURPOSES: \
            {context_data} \
            WITH: \
            {brand} \
            {instruction_2}"
    except:
        return user_prompt
    return query
    
st.title("Llama2 Fashitionita")
def main():
    metadata = {}
    h, s, g = st.columns(3)
    with h:
        number = st.number_input('Insert height info (cm):', min_value=100, max_value=200, value=180)
        metadata['height'] = number
    
    with s:
        number = st.number_input('Insert weight info (kg):', min_value=40, max_value=300, value=80)
        metadata['body_size'] = number 
        
    with g:
        gender = st.selectbox(
            'Your gender?',
            ('Male', 'Female', 'Not rather to say'))
        metadata['gender'] = gender
    
    skin_color = st.selectbox("Your skin color",
                ("Fair — belongs to the lightest shade of skin tones and burns easily",
                 "Light — appears light-colored but has warmer undertones and likely tans in summer",
                 "Medium — tone is not too fair and not too dark, and usually tans when in the sun",
                 "Deep/dark — appears deep or dark-colored and tans fast when in the sun"))
    metadata['skin_color'] = skin_color
    
    hair_color  = st.selectbox("Your hair color",
                ("Black", 
                 "Darkest Brown", 
                 "Dark Brown",
                 "Brown", 
                 "Light Brown", 
                 "Dark Blonde",
                 "Blonde", 
                 "Light Blonde", 
                 "Very Light Blonde", "Lightest Blonde"))
    metadata['hair_color'] = hair_color

    with st.form("Input your demand", clear_on_submit=True):
        a, b = st.columns([4, 1])
        user_prompt = a.text_input(
            label="Your message:",
            placeholder="Type something...",
            label_visibility="collapsed",
        )

        b.form_submit_button("Send", use_container_width=True)

    if user_prompt:
        clear_chat()
        user_prompt = make_prompt(user_prompt,  metadata, brand='normal brands')

        st.write('user_prompt: ', user_prompt)
        
        response = llama.get_response(user_prompt)  # get response from llama2 API (in our case from Workflow we created before)
        st.write("\n")
        st.title("The suggestion from FLAIR: ")
        st.write(response)

if __name__ == '__main__':
    main()
