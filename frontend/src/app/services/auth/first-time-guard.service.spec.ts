import { TestBed, inject } from '@angular/core/testing';

import { FirstTimeGuardService } from './first-time-guard.service';

describe('FirstTimeGuardService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [FirstTimeGuardService]
    });
  });

  it('should be created', inject([FirstTimeGuardService], (service: FirstTimeGuardService) => {
    expect(service).toBeTruthy();
  }));
});
