import { TestBed } from '@angular/core/testing';

import { PredictionIaService } from './prediction-ia.service';

describe('PredictionIaService', () => {
  let service: PredictionIaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PredictionIaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
