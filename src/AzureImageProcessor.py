from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from src.utils import dir_and_data_getters
import time

class RemoteImageProcessor:
    """
    A class to handle image processing using Azure Computer Vision API.
    """

    def __init__(self, api_key, endpoint, img_path):
        """
        Initializes the RemoteImageProcessor with Azure API key, endpoint, and image path.

        Args:
        - api_key (str): Azure API key.
        - endpoint (str): Azure endpoint.
        - img_path (str): Path of the image to process.
        """
        self.api_key = api_key
        self.endpoint = endpoint
        self.img_path = img_path

    def start_image_processing(self):
        """
        Starts the image processing using Azure Computer Vision API.
        """
        self.CV_Client = ComputerVisionClient(self.endpoint, CognitiveServicesCredentials(self.api_key))

        response = self.CV_Client.read_in_stream(open(self.img_path, 'rb'), language='en',  raw=True)
        operationLocation = response.headers["Operation-Location"]
        self.operationId = operationLocation.split("/")[-1]

    def get_image_processing_status(self):
        """
        Returns the status of the image processing.

        Returns:
        - str: Status of the image processing.
        """
        self.result = self.CV_Client.get_read_result(self.operationId)
        return self.result.status

    def get_image_processing_result(self):
        """
        Returns the textual result of the image processing.

        Returns:
        - str: Textual result of the image processing.
        """
        result_text = ""
        readResults = self.result.analyze_result.read_results
        for analyze_result in readResults:
            for line in analyze_result.lines:
                result_text = result_text + line.text + " "

        return result_text
    

async def i_make_request(img_path):
    """
    Asynchronous function to make a request for image processing.

    Args:
    - img_path (str): Path of the image to process.

    Returns:
    - str or None: Textual result of the image processing or None if the operation fails.
    """
    img_processor = RemoteImageProcessor(dir_and_data_getters.get_credentials('AZURE_API_KEY'), dir_and_data_getters.get_credentials('AZURE_ENDPOINT'), img_path)
    img_processor.start_image_processing()

    while img_processor.get_image_processing_status() == OperationStatusCodes.running:
        time.sleep(2)

    if (img_processor.result.status == OperationStatusCodes.succeeded):
        return img_processor.get_image_processing_result()
    
    else:
        return BaseException("operation failed")
