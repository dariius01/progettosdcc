import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DettagliNotiziaComponent } from './dettagli-notizia.component';

describe('DettagliNotiziaComponent', () => {
  let component: DettagliNotiziaComponent;
  let fixture: ComponentFixture<DettagliNotiziaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DettagliNotiziaComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DettagliNotiziaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
