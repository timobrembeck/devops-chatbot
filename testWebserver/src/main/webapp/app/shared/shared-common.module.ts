import { NgModule } from '@angular/core';

import { TestWebserverSharedLibsModule, JhiAlertComponent, JhiAlertErrorComponent } from './';

@NgModule({
    imports: [TestWebserverSharedLibsModule],
    declarations: [JhiAlertComponent, JhiAlertErrorComponent],
    exports: [TestWebserverSharedLibsModule, JhiAlertComponent, JhiAlertErrorComponent]
})
export class TestWebserverSharedCommonModule {}
