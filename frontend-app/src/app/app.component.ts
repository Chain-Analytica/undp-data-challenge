import { Component } from '@angular/core';
import { MainService } from './services/mian.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'vison-front-end';
  mainService;
  constructor(
    private mainServicep:MainService,
  ) {
    
    this.mainService = this.mainServicep;
  }
}
