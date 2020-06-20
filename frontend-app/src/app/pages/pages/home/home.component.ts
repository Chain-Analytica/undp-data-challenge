import { Component, OnInit, ViewChild } from '@angular/core';
import {FormBuilder, FormGroup, Validators,FormArray} from '@angular/forms';
import {MainService} from'../../../services/mian.service'; 
import * as uuid from 'uuid';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { Color, BaseChartDirective, Label } from 'ng2-charts';
import * as pluginAnnotations from 'chartjs-plugin-annotation';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  showFileUpload = true;
  fileToUpload=undefined;
  result;
  url="";


  public lineChartDataW: ChartDataSets[] = [
    { data: [27, 25, 25, 24, 24, 25, 25, 25,25 ], label: 'Nitrogen level (mg/kg)' },
  ];

  public lineChartData: ChartDataSets[] = [
    { data: [29, 31, 28, 29, 32, 30, 26, 27,28 ], label: 'Temperature (°C)' },
  ];


  public lineChartDataH: ChartDataSets[] = [
    { data: [50, 60, 65, 66, 70, 72, 68, 60,55 ], label: 'Humidity (%)' },
  ];

  public lineChartLabels: Label[] = ['02.00', '05.00', '08.00','11.00','14.00', '17.00', '20.00', '23.00'];
  public lineChartOptions: (ChartOptions & { annotation: any }) = {
    responsive: true,
    scales: {
      // We use this empty structure as a placeholder for dynamic theming.
      xAxes: [{}],
      yAxes: [
        {
          id: 'y-axis-0',
          position: 'left',
        },
        
      ]
    },
    annotation: {
      annotations: [
        {
          type: 'line',
          mode: 'vertical',
          scaleID: 'x-axis-0',
          value: 'March',
          borderColor: 'orange',
          borderWidth: 2,
          label: {
            enabled: true,
            fontColor: 'orange',
            content: 'LineAnno'
          }
        },
      ],
    },
  };
  public lineChartColors: Color[] = [
    { // grey
      backgroundColor: 'rgba(148,159,177,0.2)',
      borderColor: 'rgba(148,159,177,1)',
      pointBackgroundColor: 'rgba(148,159,177,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(148,159,177,0.8)'
    },
    { // dark grey
      backgroundColor: 'rgba(77,83,96,0.2)',
      borderColor: 'rgba(77,83,96,1)',
      pointBackgroundColor: 'rgba(77,83,96,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(77,83,96,1)'
    },
    { // red
      backgroundColor: 'rgba(255,0,0,0.3)',
      borderColor: 'red',
      pointBackgroundColor: 'rgba(148,159,177,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(148,159,177,0.8)'
    }
  ];
  public lineChartLegend = true;
  public lineChartType = 'line';
  public lineChartPlugins = [pluginAnnotations];

  @ViewChild(BaseChartDirective, { static: true }) chart: BaseChartDirective;
   

  constructor(private mainService:MainService) { }

  
  ngOnInit() {
  }

  

  fileChangeEvent($event): void {

    const type = $event.target.files[0].type;
    if(type == "image/png" || type == "image/jpg" || type == "image/jpeg"){

      const file: File = $event.target.files[0];
      const myReader: FileReader = new FileReader();


      var reader = new FileReader();
      var fileByteArray = [];
      reader.readAsArrayBuffer(file);
      reader.onloadend =  (evt:any) => {

          if (evt.target.readyState == FileReader.DONE) {
            var arrayBuffer = evt.target.result,
                array = new Uint8Array(arrayBuffer);
            for (var i = 0; i < array.length; i++) {
                fileByteArray.push(array[i]);
            }
          }
           this.mainService.getResults({data:fileByteArray}).subscribe(res => {
              console.log("adasdasd")
              console.log(this.result)
              this.showFileUpload = false;
            })

            this.showFileUpload = false;
            console.log(JSON.stringify(fileByteArray))
      }

     

    }else{
      alert("file should be a image (.png, .jpg, .jpeg)")
    }

   }

   getClickedData(val){

    

   }
  

}

