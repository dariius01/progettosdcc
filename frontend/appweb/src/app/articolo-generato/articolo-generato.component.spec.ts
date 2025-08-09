import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticoloGeneratoComponent } from './articolo-generato.component';

describe('ArticoloGenerato', () => {
  let component: ArticoloGeneratoComponent;
  let fixture: ComponentFixture<ArticoloGeneratoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ArticoloGeneratoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ArticoloGeneratoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
