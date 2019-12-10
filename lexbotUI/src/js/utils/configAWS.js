
export default function configAWS(IdentityPoolRegion, IdentityPoolId){
    // Initialize the Amazon Cognito credentials provider
    AWS.config.region = IdentityPoolRegion; // Region
    AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    // Provide your Pool Id here
        IdentityPoolId: IdentityPoolId,
    });

    const lexruntime = new AWS.LexRuntime();
    const lexUserId = 'chatbot-demo' + Date.now();

    return {
        'lexruntime':lexruntime, 
        'lexUserId': lexUserId
    }
}
