import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class PredictionIaService {
  
  private apiUrl = 'http://localhost:5000/detect_city'; // Remplacez par l'URL de votre API Flask

  constructor(private http: HttpClient) { }

  predictCityPresence(sentence: string) {
    const body = { sentence };
    console.log(body);
    return this.http.post<any>(this.apiUrl, body);
  }
}
