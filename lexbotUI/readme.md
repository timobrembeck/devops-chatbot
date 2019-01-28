Generic widget UI to integrate lex bot in any web app.

In order to make it work : 
  - Insert bundle.css and bundle.js from the dist folder into your main html file
  - Insert the official AWS sdk 
  - Create a div with id="lexbotapp"
  - Instantiate the chatbot with  new LexBot(IdentityPoolRegion, IdentityPoolId, WidgetHeight, WidgetWidht);
  

In order to further develop: 
  - Source code exist in src folder
  - Webpack configuration compiles and minifies js and css in single files inside the dist folder
  - Type webpack on the root folder to compile and minify the code


You can see an example of how the widget is used in the index.html file inside the dist folder.

