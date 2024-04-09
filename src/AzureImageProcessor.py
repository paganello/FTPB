from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
import utils.dir_and_data_getters as dir_and_data_getters
import time

#overload the class for image processing with Azure
class RemoteImageProcessor:

    # Constructor
    # api_key: Azure API key
    # endpoint: Azure endpoint
    # img_path: path of the image to process
    def __init__(self, api_key, endpoint, img_path):
        self.api_key = api_key
        self.endpoint = endpoint
        self.img_path = img_path
    
    # Using Azure Computer Vision API start the image processing
    def start_image_processing(self):

        self.CV_Client = ComputerVisionClient(self.endpoint, CognitiveServicesCredentials(self.api_key))

        response = self.CV_Client.read_in_stream(open(self.img_path, 'rb'), language='en',  raw=True)
        print(response)
        operationLocation = response.headers["Operation-Location"]
        self.operationId = operationLocation.split("/")[-1]
        print(self.operationId)

    # Return the status of the image processing
    def get_image_processing_status(self):
        self.result = self.CV_Client.get_read_result(self.operationId)
        return self.result.status
    
    # Return the textual result of the image processing
    def get_image_processing_result(self):
        result_text = ""
        readResults = self.result.analyze_result.read_results
        for analyze_result in readResults:
            for line in analyze_result.lines:
                result_text = result_text + line.text + " "

        return result_text
    

async def i_make_request(img_path):
    img_processor = RemoteImageProcessor(dir_and_data_getters.get_credentials('AZURE_API_KEY'), dir_and_data_getters.get_credentials('AZURE_ENDPOINT'), img_path)
    img_processor.start_image_processing()

    while img_processor.get_image_processing_status() == OperationStatusCodes.running:
        print("Processing...")
        time.sleep(2)

    if (img_processor.result.status == OperationStatusCodes.succeeded):

        print(img_processor.get_image_processing_result())
        return img_processor.get_image_processing_result()
    
    else:
        return None
    