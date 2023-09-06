import { Component, OnInit } from '@angular/core';
import { SpeechSocketServiceService } from './services/speech-socket-service.service';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  
  messages: any[] = [];
  recognizedText: string = '';
  statusText: string = '';
  positions = NbGlobalPhysicalPosition;
  SpeakButtonIsDisable = false;

  constructor(private socketService: SpeechSocketServiceService,
    private toastrService: NbToastrService) {}


  ngOnInit() {
    // Écoutez les nouveaux messages
    this.socketService.onRecognizedText().subscribe((message: any) => {
      this.recognizedText = message.text;
    });
    this.socketService.onRecordingStatusChange().subscribe((status: any) => {
      this.SpeakButtonIsDisable = true;
      this.showToast(this.positions.TOP_RIGHT, 'info',"Commencer à parler !", status.status, 6000);
    })

    this.socketService.onRecordingStatusApprove().subscribe((status: any) => {
      this.SpeakButtonIsDisable = false;
      this.showToast(this.positions.TOP_RIGHT, 'success',"Vous pouvez envoyer votre itinaire !", status.status, 6000);
    })

    this.socketService.onRecordingError().subscribe((status_error: any) => {
      this.SpeakButtonIsDisable = false;
      this.showToast(this.positions.TOP_RIGHT, 'warning', "Oupss ... vueillez réessayer",status_error.status, 6000);
    })
  }

  StartRecognition() {
    this.socketService.sendVocalMessage();
  }

  showToast(position: any, status: any, message: string, title: string, duration: number) {
    this.toastrService.show(`${message}`, title, { position, status, duration });
  }

  sendMessage(event: any) {
    console.log(event.message);
    this.messages.push({
      text: event.message,
      date: new Date(),
      reply: true,
      user: {
        name: 'Jonh Doe',
        avatar: 'https://i.gifer.com/no.gif',
      },
    });
  }
}
