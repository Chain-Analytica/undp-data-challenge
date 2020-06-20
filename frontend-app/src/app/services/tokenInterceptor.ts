import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor} from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import {environment} from 'src/environments/environment';
import { MainService } from './mian.service'

@Injectable()
export class TokenInterceptor implements HttpInterceptor {

  constructor(private mainService:MainService) {}

  private totalRequests = 0;
  loaderToShow: any;


  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    
     // show loading true
     this.mainService.showLoader = true;
     this.totalRequests++;

    if(request.url === environment.baseUrl+'get-result'){
        request = request.clone({
            setHeaders: {
            }
          });
     }
    
   
    return next.handle(request).finally(() => {
      this.totalRequests--;
      if (this.totalRequests === 0) {
        this.mainService.showLoader = false;
      }
    });


  }

}
