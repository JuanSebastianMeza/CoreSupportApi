import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

// Own services imports
import { ConstService } from '../utils/const.service';

// Interfaces
import { Subscriber } from '../../interfaces/subscriber.interfaces';

@Injectable({
    providedIn: 'root'
})
export class SubscriberDataService {

    // Base API URL from environment
    private apiUrl: string = this.constService.apiUrl;

    constructor(
        private http: HttpClient,
        private constService: ConstService,
    ) { }

    /**
     * Fetches subscriber data from the backend API.
     *
     * @param msisdn - A single MSISDN or a comma-separated list of MSISDNs.
     *                 e.g. '584141963786' or '584141963786,584141963787'
     * @returns Observable<Subscriber[]> — array with one entry per MSISDN queried.
     *
     * Endpoint: GET /api/get-subscribers-data/?msisdn=<msisdn>
     */
    getSubscriberData(msisdn: string): Observable<Subscriber[]> {
        const params = new HttpParams().set('msisdn', msisdn);
        return this.http.get<Subscriber[]>(
            `${this.apiUrl}api/get-subscribers-data/`,
            { params }
        );
    }
}
