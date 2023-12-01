import { Component, OnInit } from '@angular/core';
import { SpeechSocketServiceService } from './services/speech-socket-service.service';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';
import { PredictionIaService } from './services/prediction-ia.service';

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

  sentence: string = "";
  prediction: string = "";

  constructor(private socketService: SpeechSocketServiceService,
    private toastrService: NbToastrService,
    private predictionService: PredictionIaService) {}


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

  predict(sentence: any) {
    this.predictionService.predictCityPresence(sentence).subscribe(data => {
      this.prediction = data.result;

      // Ajoutez la réponse de la prédiction en tant que message
      this.messages.push({
        //type: "file",
        text: this.prediction,
        date: new Date(),
        reply: false, // Indiquez que c'est une réponse du système, donc reply est à false
        //file: [ { url: 'https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTNuN2hwYWNrNmx2NGxreHc5YXJobDFhNGUwNGlla2Rmcno1OTZmciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/q34aUDUNhwdpKUR8Gy/giphy.gif', type: 'image/gif' } ],
        user: {
          name: 'IA Travel Order',
          avatar: 'https://i.gifer.com/no.gif', // Vous pouvez définir une image d'avatar pour le système
        },
      });

    });
  }

  sendMessage(event: any) {
    console.log(event.message);
    this.predict(event.message);
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
