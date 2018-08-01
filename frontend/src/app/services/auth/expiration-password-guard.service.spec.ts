import { TestBed, inject } from '@angular/core/testing';

import { ExpirationPasswordGuardService } from './expiration-password-guard.service';

describe('ExpirationPasswordGuardService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ExpirationPasswordGuardService]
    });
  });

  it('should be created', inject([ExpirationPasswordGuardService], (service: ExpirationPasswordGuardService) => {
    expect(service).toBeTruthy();
  }));
});
