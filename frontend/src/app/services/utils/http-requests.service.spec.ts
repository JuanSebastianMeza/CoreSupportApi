import { TestBed, inject } from '@angular/core/testing';

import { HttpRequestsService } from './http-requests.service';

describe('HttpRequestsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [HttpRequestsService]
    });
  });

  it('should be created', inject([HttpRequestsService], (service: HttpRequestsService) => {
    expect(service).toBeTruthy();
  }));
});
