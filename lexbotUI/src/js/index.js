import instantiateDOM from './utils/instantiateDOM';
import configAWS from './utils/configAWS';

window.LexBot = class LexBot {
    constructor(IdentityPoolRegion, IdentityPoolId, height, width){
        this.IdentityPoolRegion = IdentityPoolRegion;
        this.IdentityPoolId = IdentityPoolId;
        this.height = height;
        this.width = width;
        this.init();
    }

    async init() {
        const config = configAWS(this.IdentityPoolRegion, this.IdentityPoolId);
        const lexUserId = config.lexUserId;
        const lexruntime = config.lexruntime;
        await instantiateDOM(lexUserId, lexruntime, this.height, this.width)
    }
}









