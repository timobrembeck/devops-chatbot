import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { SERVER_API_URL } from 'app/app.constants';

@Injectable({ providedIn: 'root' })
export class HomeService {
    constructor(private http: HttpClient) {}

    mediumLoad(): Observable<Object> {
        return this.http.get<String>(SERVER_API_URL + 'api/load/medium');
    }

    fullLoad(): Observable<Object> {
        return this.http.get<String>(SERVER_API_URL + 'api/load/full');
    }
}
