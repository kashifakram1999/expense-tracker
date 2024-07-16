import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  title = 'expense-tracker';

  activeLink: string = '';

  setActiveLink(link: string) {
    this.activeLink = link;
  }

  ngOnInit() {
    // Ensure 'dashboard' is selected by default
    this.setActiveLink('dashboard');
  }
}
