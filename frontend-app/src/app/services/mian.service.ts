import {Injectable} from '@angular/core';
import {map} from 'rxjs/operators';
import {ApiService} from './api.service';
import 'rxjs/Rx';
import { Observable ,  throwError } from 'rxjs';
import { HttpHeaders, HttpClient, HttpParams } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import {environment} from 'src/environments/environment';

const HttpUploadOptions = {
  headers: new HttpHeaders({ 'Content-Type': undefined })
}

@Injectable({
    providedIn: 'root'
})
export class MainService {

  constructor(private apiService: ApiService, private http: HttpClient) {
  }

  showLoader = false;
  private formatErrors(error: any) {
    return  throwError(error.error);
  }
 
  getResults(formData){
    console.log(formData)
    return this.http.post("http://31177464-d60d-4ebc-b596-e232097540f1.southeastasia.azurecontainer.io/score" , formData)
      .pipe(
        catchError(this.formatErrors)
      );
  }

  getResultsByUrl(url){
    return this.apiService.get(environment.baseUrl+'/get-result-by-url/'+encodeURIComponent(url))
      .pipe(
        catchError(this.formatErrors)
      );
  }

  
    
}
