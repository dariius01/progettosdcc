import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AggiuntaManualeComponent } from './aggiunta-manuale.component';

describe('AggiuntaManualeComponent', () => {
  let component: AggiuntaManualeComponent;
  let fixture: ComponentFixture<AggiuntaManualeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AggiuntaManualeComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AggiuntaManualeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
