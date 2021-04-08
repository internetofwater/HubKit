import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SetupformComponent } from './setupform.component';

describe('SetupformComponent', () => {
  let component: SetupformComponent;
  let fixture: ComponentFixture<SetupformComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SetupformComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SetupformComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
