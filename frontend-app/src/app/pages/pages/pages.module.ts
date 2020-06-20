import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PagesComponent } from './pages.component';
import { RouterModule } from '@angular/router';
import {PagesRoutingModule} from './page-routing.module';
import { HomeComponent } from './home/home.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import {NgbPaginationModule, NgbAlertModule,NgbTabsetModule} from '@ng-bootstrap/ng-bootstrap';
import { ChartsModule } from 'ng2-charts';

@NgModule({
  declarations: [PagesComponent, HomeComponent],
  imports: [
    CommonModule,
    RouterModule,
    PagesRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    NgbTabsetModule,
    ChartsModule
  ]
})
export class PagesModule { }
