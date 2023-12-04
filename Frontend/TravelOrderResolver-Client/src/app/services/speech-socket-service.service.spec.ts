import { TestBed } from '@angular/core/testing';

import { SpeechSocketServiceService } from './speech-socket-service.service';

describe('SpeechSocketServiceService', () => {
  let service: SpeechSocketServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SpeechSocketServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
