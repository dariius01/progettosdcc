import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModificaNotiziaComponent } from './modifica-notizia.component';

describe('ModificaNotiziaComponent', () => {
  let component: ModificaNotiziaComponent;
  let fixture: ComponentFixture<ModificaNotiziaComponent>;

  beforeEach(async () => {  
    await TestBed.configureTestingModule({
      imports: [ModificaNotiziaComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ModificaNotiziaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
