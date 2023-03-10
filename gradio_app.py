import openai
import gradio as gr

message_history = []

def init(key_file_path):
    openai.api_key = open(key_file_path, "r").read().strip("\n")

def predict_answer(input):

    message_history.append({"role": "user", "content": f"{input}"})

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=message_history
    )

    reply_content = completion.choices[0].message.content
    
    message_history.append({"role": "assistant", "content": f"{reply_content}"}) 
    
    response = [(message_history[i]["content"], message_history[i+1]["content"]) for i in range(0, len(message_history)-1, 2)]  # convert to tuples of list
    return response

def main():

    with gr.Blocks() as demo: 

        chatbot = gr.Chatbot() 

        with gr.Row(): 
            txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)

        txt.submit(predict_answer, txt, chatbot)
        txt.submit(lambda :"", None, txt)
            
    demo.launch()


if __name__ == "__main__":
    key_file_path = "key.txt"
    init(key_file_path)
    main()