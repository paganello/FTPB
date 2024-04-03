from openai import OpenAI
import time
import other_functions
import json

#overload the class for text processing with OpenAI
class OpenaiTextProcessor:
    assistant_id = None
    thread_id = None

    # Constructor
    # api_key: OpenAI API key
    # text: text to elaborate
    # conf_mex: configuration message
    def __init__(self, api):

        self.client = OpenAI(api_key = api)
        self.file = None
        self.assistant = None
        self.thread = None
        self.run = None
        self.response = None

        if OpenaiTextProcessor.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id=OpenaiTextProcessor.assistant_id
                )
            
        if OpenaiTextProcessor.thread_id:
            self.thread = self.client.beta.threads.retrieve(
                thread_id=OpenaiTextProcessor.thread_id
                )
            

    # Upload the file
    def upload_file(self, file_dir): 
        
        file = self.client.files.create(
            file= open(file_dir, "rb"),
            purpose= "fine-tune"
        )
        self.file = file



    # Create the assistant
    def create_assistant(self, name, instructions):
        
        if not self.assistant:
            
            assistant = self.client.beta.assistants.create(
                name= name,
                instructions= instructions,
                tools= [{"type": "retrieval"}],
                model= "gpt-3.5-turbo-0125",
                #file_ids= [self.file.id]
            )
            OpenaiTextProcessor.assistant_id = assistant.id
            self.assistant = assistant
            print(f"AssID:::: {self.assistant.id}")



    # Create the thread
    def create_thread(self):
        
        if not self.thread:
            
            thread = self.client.beta.threads.create()
            OpenaiTextProcessor.thread_id = thread.id
            self.thread = thread
            print(f"ThreadID:::: {self.thread.id}")



    # Add a message to the thread
    def add_thread_message(self, role, content):
        
        if self.thread:
            
            self.message = self.client.beta.threads.messages.create(
                thread_id= self.thread.id,
                role= role,
                content= content
            )



    # Run the assistant
    def run_assistant(self):

        if self.thread and self.assistant:
            
            self.run = self.client.beta.threads.runs.create(
                thread_id= self.thread.id,
                assistant_id= self.assistant.id,
                temperature= 0.1,
            )



    # Process the messages
    def process_messages(self):

        if self.thread:
            
            messages = self.client.beta.threads.messages.list(
                thread_id= self.thread.id
            )
            response = []

            last_message = messages.data[0]
            role = last_message.role
            response = last_message.content[0].text.value
            
            self.response = response

            print(f"SUMMARY: {role.capitalize()} => {response}")

            #for msg in messages:
            #    role = msg.role
            #    content = msg.content[0].text.value
            #    print(f"{role.capitalize()} => {content}")



    # Wait for the completion
    def wait_for_completion(self):

        if self.thread and self.run:

            while self.run.status != "completed":
                time.sleep(5)
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id= self.thread.id,
                    run_id= self.run.id
                )
                print(f"RUN STATUS:: {run_status.model_dump_json(indent=4)}")

                if run_status.status == "completed":
                    self.process_messages()
                    break
                elif run_status.status == "requires_action":
                    print("Run failed")
                    break


    # Execute fast completion using fine-tuned gpt model
    def make_completion(self, custom_model, instructions, text):

        completion = self.client.chat.completions.create(
            model= custom_model,
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": text}
            ]
        )
        print(completion)

        self.response = completion.choices[0].message.content
    


    # Return the elaborated text
    def get_response(self):
        return self.response

#async def t_make_request(text):
#    text_processor = RemoteImageTextProcessor(other_functions.get_credentials('OPENAI_API_KEY'), text, other_functions.get_settings('CONF_GPT_REQ_MESSAGE_text'))
#    # Elaborate the text
#    text_processor.elaborate_text()
#    # Return the elaborated text
#    output = text_processor.get_elaborated_text()
#    print(output)
#    return output

def t_make_request_using_custom_model(text):

    instructions = other_functions.get_settings("CUSTOM_MODEL_SYS_INSTRUCTIONS")

    custom_model = other_functions.get_settings("CUSTOM_MODEL_NAME")

    text_processor = OpenaiTextProcessor(other_functions.get_credentials('OPENAI_API_KEY'))

    completion = text_processor.make_completion(
        custom_model= custom_model,
        instructions= instructions,
        text= text
    )

    return text_processor.get_response()


#def t_make_request_using_assistant(text):
    
    #text_processor = RemoteTextProcessor(other_functions.get_credentials('OPENAI_API_KEY'))

    #if text_processor.is_ready():
                #... do something

    # Create the assistant
    #text_processor.create_assistant(name= "receipt-ocr", instructions= "sei un assistente di elaborazione di testo. e' importente che il testo sia formattato come scritto nelle istruzioni: la formattzione deve essere come la seguente: {\"date\": \"...\",\"total\": ...};[{\"amount\": ..., \"tax\": ..., \"description\": \"...\"}, {\"amount\": ..., \"tax\": ..., \"description\": \"...\"}] al posto dei punti ('...') devono esserci i valori relativi al singolo caso estratti dal messaggio. ")
    # Create the thread
    #text_processor.create_thread()
    # Add the message
    #text_processor.add_thread_message(role= "user", content= text)
    # Run the assistant
    #text_processor.run_assistant()
    # Wait for the completion
    #text_processor.wait_for_completion()
    # Get the elaborated text
    #text_processor.get_threadMessage()
