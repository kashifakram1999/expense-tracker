import { Component, OnInit } from '@angular/core';
import * as am5 from '@amcharts/amcharts5';
import * as am5percent from '@amcharts/amcharts5/percent';
import am5themes_Spirited from '@amcharts/amcharts5/themes/Spirited'

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit { 
  currentDate: string;
totalIncome: number = 1000;
totalExpenses: number = 500;
balance: number = this.totalIncome - this.totalExpenses;
  
  constructor() {
    const today = new Date();
    const monthNames = [
      'January', 'February', 'March', 'April', 'May', 'June', 'July',
      'August', 'September', 'October', 'November', 'December'
    ];
    const monthIndex = today.getMonth();
    this.currentDate = `${monthNames[monthIndex]} ${today.getFullYear()}`;
  }

  ngOnInit(): void {
    let root = am5.Root.new('chartdiv');

    // Set themes
    // https://www.amcharts.com/docs/v5/concepts/themes/
    root.setThemes([am5themes_Spirited.new(root)]);

    // Create chart
    // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/
    let chart = root.container.children.push(
      am5percent.PieChart.new(root, {
        endAngle: 360,
        radius: am5.percent(20)
      })
    );

    // Create series
    // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Series
    let series = chart.series.push(
      am5percent.PieSeries.new(root, {
        valueField: 'value',
        categoryField: 'category',
        endAngle: 270,
      })
    );

    series.states.create('hidden', {
      endAngle: -90,
    });

    // Set data
    // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Setting_data
    series.data.setAll([
      {
        category: 'Lithuania',
        value: 501.9,
      },
      {
        category: 'Czechia',
        value: 301.9,
      },
      {
        category: 'Ireland',
        value: 201.1,
      },
      {
        category: 'Germany',
        value: 165.8,
      },
      {
        category: 'Australia',
        value: 139.9,
      },
      {
        category: 'Austria',
        value: 128.3,
      },
      {
        category: 'UK',
        value: 99,
      },
    ]);

    series.appear(1000, 100);

    var legend = chart.children.push(am5.Legend.new(root, {
      centerX: am5.percent(0),
      x: am5.percent(0),
      layout: root.verticalLayout
    }));
    
    legend.data.setAll(series.dataItems);
  }
}
