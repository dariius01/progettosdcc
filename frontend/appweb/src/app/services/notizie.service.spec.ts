import { TestBed } from '@angular/core/testing';

import { NotizieService } from './notizie.service';

describe('Notizie', () => {
  let service: NotizieService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NotizieService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
