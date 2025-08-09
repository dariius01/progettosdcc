import { TestBed } from '@angular/core/testing';

import { ArticoliManualiService } from './articoli-manuali.service';

describe('ArticoliManuali', () => {
  let service: ArticoliManualiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ArticoliManualiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
