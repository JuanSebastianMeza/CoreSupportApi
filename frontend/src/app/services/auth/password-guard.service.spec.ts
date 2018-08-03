import { TestBed, inject } from '@angular/core/testing';

import { PasswordGuardService } from './password-guard.service';

describe('PasswordGuardService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [PasswordGuardService]
    });
  });

  it('should be created', inject([PasswordGuardService], (service: PasswordGuardService) => {
    expect(service).toBeTruthy();
  }));
});
