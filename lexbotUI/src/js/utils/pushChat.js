import showError from './showError';
import showRequest from './showRequest';
import showResponse from './showResponse';
import configAWS from './configAWS';

export default function pushChat(lexUserId, lexruntime) {

    // if there is text to be sent...
    const wisdomText = document.getElementById('wisdom');
    if (wisdomText && wisdomText.value && wisdomText.value.trim().length > 0) {
        // disable input to show we're sending it
        const wisdom = wisdomText.value.trim();
        wisdomText.value = '...';
        wisdomText.locked = true;

        let sessionAttributes = {};
         // send it to the Lex runtime
        const params = {
            botAlias: '$LATEST',
            botName: 'DevOpsChatBot',
            inputText: wisdom,
            userId: lexUserId,
            sessionAttributes: sessionAttributes
        };

        showRequest(wisdom);
        lexruntime.postText(params, (err, data) => {
            if (err) {
                console.log(err, err.stack);
                showError('Error:  ' + err.message + ' (see console for details)')
            }
            if (data) {
                console.log(data);
                // capture the sessionAttributes for the next cycle
                sessionAttributes = data.sessionAttributes;
                // show response and/or error/dialog status
                showResponse(data);
            }
            // re-enable input
            wisdomText.value = '';
            wisdomText.locked = false;
        });
    }

}