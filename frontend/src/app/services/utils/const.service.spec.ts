import { TestBed, inject } from '@angular/core/testing';

import { ConstService } from './const.service';

describe('ConstService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ConstService]
    });
  });

  it('should be created', inject([ConstService], (service: ConstService) => {
    expect(service).toBeTruthy();
  }));
});
