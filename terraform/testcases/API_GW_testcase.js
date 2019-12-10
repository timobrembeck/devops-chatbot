In order to use the API Gateway provided from the FCP DevOps_Chatbot team please follow the instructions below.

URL = 'https://49i1s1hky0.execute-api.eu-west-1.amazonaws.com/alert_manager_notification_api_stage_name';

Send a POST request to the above URL and specify:
    1) The request headers = Authorization:Bearer xyz
    2) The request body to the following data structure as JSON(application/json) : 
        {
            "status": "firing",
            "description": "example description",
            "priority": "high"
        }