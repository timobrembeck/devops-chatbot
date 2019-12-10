import { Component, OnInit } from '@angular/core';
import { NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { JhiAlertService, JhiEventManager } from 'ng-jhipster';

import { LoginModalService, Principal, Account } from 'app/core';
import { HomeService } from './home.service';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { numberOfBytes } from 'ng-jhipster/src/directive/number-of-bytes';

@Component({
    selector: 'jhi-home',
    templateUrl: './home.component.html',
    styleUrls: ['home.css']
})
export class HomeComponent implements OnInit {
    account: Account;
    modalRef: NgbModalRef;

    constructor(
        private principal: Principal,
        private loginModalService: LoginModalService,
        private alertService: JhiAlertService,
        private eventManager: JhiEventManager,
        private homeService: HomeService
    ) {}

    ngOnInit() {
        this.principal.identity().then(account => {
            this.account = account;
        });
        this.registerAuthenticationSuccess();
    }

    registerAuthenticationSuccess() {
        this.eventManager.subscribe('authenticationSuccess', message => {
            this.principal.identity().then(account => {
                this.account = account;
            });
        });
    }

    isAuthenticated() {
        return this.principal.isAuthenticated();
    }

    login() {
        this.modalRef = this.loginModalService.open();
    }

    fullLoad() {
        this.homeService.mediumLoad().subscribe(
            (res: string) => {
                console.log(res);
                this.alertService.success('Pi is:' + res, '', null);
            },
            (err: HttpErrorResponse) => {
                console.log(err);
            }
        );
    }

    mediumLoad() {
        this.homeService.fullLoad().subscribe(
            (res: string) => {
                console.log(res);
                this.alertService.success('Pi is:' + res, '', null);
            },
            (err: HttpErrorResponse) => {
                console.log(err);
            }
        );
    }

    shutDown() {
        this.homeService.shutDown().subscribe(
            (res: string) => {
                console.log(res);
                this.alertService.success('Successfully shut down the server', null);
            },
            (err: HttpErrorResponse) => {
                console.log(err);
            }
        );
    }
}
