import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private isLoggedIn = signal(false);

  login(username: string, password: string): boolean {
    const valid = username === 'admin' && password === 'admin';
    this.isLoggedIn.set(valid);
    return valid;
  }

  get loggedIn() {
    return this.isLoggedIn.asReadonly();
  }
}