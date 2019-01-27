import instantiateDOM from './utils/instantiateDOM';

window.LexBot = class LexBot {
    constructor(IdentityPoolRegion, IdentityPoolId, height, width){
        this.IdentityPoolRegion = IdentityPoolRegion;
        this.IdentityPoolId = IdentityPoolId;
        this.height = height;
        this.width = width;
        this.init();
    }

    async init() {
        await instantiateDOM(this.IdentityPoolRegion, this.IdentityPoolId, this.height, this.width)
    }
}









