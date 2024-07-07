import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-income',
  templateUrl: './income.component.html',
  styleUrl: './income.component.scss'
})
export class IncomeComponent {
  incomeForm! : FormGroup
  dropdownSettings = {
    // if we need to add multiple categories you just need to make false to singleSelection
    singleSelection: true,
    idField: 'item_id',
    textField: 'item_text',
    selectAllText: 'Select All',
    unSelectAllText: 'UnSelect All',
    itemsShowLimit: 3,
    allowSearchFilter: true
  };
  dropdownList = [
    { item_id: 1, item_text: 'Ammi ne Diye' },
    { item_id: 2, item_text: 'Abu se Liye' },
    { item_id: 3, item_text: 'Rashan me se bache' },
    { item_id: 4, item_text: 'Papa ki pocket mari' },
    { item_id: 5, item_text: 'Choti sister se cheene' }
  ];

  constructor(
    private fb: FormBuilder,
  ) {

  }

  ngOnInit(){
    

    this.incomeForm = this.fb.group({
      title: [null, Validators.required],
      amount: [null, Validators.required],
      date: [null, Validators.required],
      category: [null],
      description: [null, Validators.required]
    })
  }
  submitForm() {
    
  }
}
