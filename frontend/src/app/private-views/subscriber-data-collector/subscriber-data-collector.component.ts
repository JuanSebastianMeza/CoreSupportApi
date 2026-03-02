import { Component, OnInit } from '@angular/core';
import { trigger, transition, style, animate, query, stagger } from '@angular/animations';

// Interfaces
import { Subscriber } from '../../interfaces/subscriber.interfaces';

// Services
import { SubscriberDataService } from '../../services/subscriber-data/subscriber-data.service';

@Component({
    selector: 'app-subscriber-data-collector',
    templateUrl: './subscriber-data-collector.component.html',
    styleUrls: ['./subscriber-data-collector.component.css'],
    animations: [
        trigger('cardListAnimation', [
            transition('* => *', [
                query(':enter', [
                    style({ opacity: 0, transform: 'translateY(30px)' }),
                    stagger(120, [
                        animate('400ms cubic-bezier(0.35, 0, 0.25, 1)',
                            style({ opacity: 1, transform: 'translateY(0)' })
                        )
                    ])
                ], { optional: true })
            ])
        ]),
        trigger('fadeSlideIn', [
            transition(':enter', [
                style({ opacity: 0, transform: 'translateY(-12px)' }),
                animate('300ms ease-out', style({ opacity: 1, transform: 'translateY(0)' }))
            ]),
            transition(':leave', [
                animate('200ms ease-in', style({ opacity: 0, transform: 'translateY(-12px)' }))
            ])
        ])
    ]
})
export class SubscriberDataCollectorComponent implements OnInit {

    // Search input value
    msisdnInput: string = '';

    // State flags
    isLoading: boolean = false;
    hasError: boolean = false;
    errorMessage: string = '';
    hasSearched: boolean = false;

    // Results
    subscribers: Subscriber[] = [];

    // Expanded card tracking
    expandedIndex: number | null = null;

    constructor(private subscriberDataService: SubscriberDataService) { }

    ngOnInit() { }

    /** Validate and execute the search */
    search(): void {
        const raw = this.msisdnInput.trim();
        if (!raw) { return; }

        // Basic MSISDN validation: digits only, 5-15 characters each
        const msisdnList = raw.split(',').map(s => s.trim()).filter(s => s.length > 0);
        const invalid = msisdnList.find(m => !/^\d{5,15}$/.test(m));
        if (invalid) {
            this.hasError = true;
            this.errorMessage = `"${invalid}" no es un MSISDN válido. Solo dígitos, entre 5 y 15 caracteres.`;
            return;
        }

        this.isLoading = true;
        this.hasError = false;
        this.errorMessage = '';
        this.hasSearched = false;
        this.subscribers = [];
        this.expandedIndex = null;

        this.subscriberDataService.getSubscriberData(msisdnList.join(',')).subscribe({
            next: (data: Subscriber[]) => {
                this.subscribers = data;
                this.isLoading = false;
                this.hasSearched = true;
            },
            error: (err) => {
                this.isLoading = false;
                this.hasError = true;
                this.hasSearched = true;
                const msg = err.error?.error || err.message || 'Error desconocido al consultar la API.';
                this.errorMessage = msg;
            }
        });
    }

    /** Clear results and reset the form */
    clearResults(): void {
        this.msisdnInput = '';
        this.subscribers = [];
        this.hasSearched = false;
        this.hasError = false;
        this.errorMessage = '';
        this.expandedIndex = null;
    }

    /** Toggle card expansion */
    toggleCard(index: number): void {
        this.expandedIndex = this.expandedIndex === index ? null : index;
    }

    /** Allow search on Enter key */
    onKeydown(event: KeyboardEvent): void {
        if (event.key === 'Enter') { this.search(); }
    }

    /** Derive a display label for network technology */
    getTechLabel(technology: string): string {
        const map = { 'LTE': '4G LTE', 'UMTS': '3G UMTS', 'GSM': '2G GSM' };
        return map[technology] || technology || '—';
    }

    /** Return a CSS class name based on network technology */
    getTechClass(technology: string): string {
        const map = { 'LTE': 'tech-lte', 'UMTS': 'tech-umts', 'GSM': 'tech-gsm' };
        return map[technology] || 'tech-unknown';
    }
}
