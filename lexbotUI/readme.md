
# Generic widget which can integrate easily AWS Lex bot in any website/webapp.

## Installation : 
  - Import bundle.css and bundle.js bundles from the dist folder into your main html file.
  - Import the official AWS JS sdk.
  - Create a div with id="lexbotapp" in your main html file.
  - Using the Widget API, instantiate the lex-chatbot using the following code and passing the appropriate data : ``` const lexbot = new LexBot(IdentityPoolRegion, IdentityPoolId, WidgetHeight, WidgetWidht); ```
  

## In order to contribute to the project: 
  - Source code exist in src folder
  - Webpack configuration compiles and minifies js and css in single bundles inside the dist folder.
  - Type ```webpack``` on the root folder of the project to compile and minify the code/


The project is hosted in a S3 bucket on AWS and can be used following the URL :  
## ```http://lexbotwebapp.s3-website-eu-west-1.amazonaws.com/```

You can see an example of how the widget is used in the index.html.
