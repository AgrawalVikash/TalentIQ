import { CommonModule } from '@angular/common';
import { Component, computed, signal } from '@angular/core';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    MatProgressSpinnerModule,
  ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  readonly email = new FormControl('', [Validators.required, Validators.email]);
  readonly password = new FormControl('', [Validators.required]);

  readonly loginForm = new FormGroup({
    email: this.email,
    password: this.password,
  });

  readonly emailInvalid = computed(
    () => this.email.touched && this.email.invalid
  );
  readonly passwordInvalid = computed(
    () => this.password.touched && this.password.invalid
  );
  readonly isSubmitting = signal<boolean>(false);
  readonly loginError = signal<string | null>(null);

  constructor(private router: Router) {}

  onSubmit(): void {
    if (!this.loginForm.valid || this.isSubmitting()) return;

    this.isSubmitting.set(true);
    this.loginError.set(null);

    setTimeout(() => {
      this.isSubmitting.set(false);
      this.router.navigate(['/dashboard']);
      this.loginForm.reset();
    }, 1500);
  }
}
