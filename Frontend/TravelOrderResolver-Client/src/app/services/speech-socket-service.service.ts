import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { io } from 'socket.io-client';

@Injectable({
  providedIn: 'root'
})
export class SpeechSocketServiceService {

  private socket;

  constructor() {
    this.socket = io('http://localhost:5000');
  }

  // Méthodes pour envoyer et recevoir des messages
  sendVocalMessage() {
    this.socket.emit('start_recording');
  }

  stopVocalMessage() {
    this.socket.emit('stop_recording');
  }

  onRecordingStatusChange() {
    return new Observable((observer) => {
      this.socket.on('status_recording', (data) => {
        observer.next(data);
      });
    });
  }

  onRecordingStatusApprove() {
    return new Observable((observer) => {
      this.socket.on('status_recording_approve', (data) => {
        observer.next(data);
      });
    });
  }

  onRecordingError() {
    return new Observable((observer) => {
      this.socket.on('status_recording_error', (data) => {
        observer.next(data);
      });
    });
  }

  onRecognizedText() {
    return new Observable((observer) => {
      this.socket.on('recognized_text', (data) => {
        observer.next(data);
      });
    });
  }

}
