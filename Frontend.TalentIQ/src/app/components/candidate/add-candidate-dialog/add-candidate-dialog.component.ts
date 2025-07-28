import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'app-add-candidate-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
  ],
  templateUrl: './add-candidate-dialog.component.html',
  styleUrl: './add-candidate-dialog.component.scss',
})
export class AddCandidateDialogComponent {
  private fb = inject(FormBuilder);
  private dialogRef = inject(MatDialogRef<AddCandidateDialogComponent>);

  form = this.fb.group({
    name: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    phone: [
      '',
      [
        Validators.required,
        Validators.pattern('^[0-9]+$'),
        Validators.minLength(10),
        Validators.maxLength(10),
      ],
    ],
    jobId: ['', Validators.required],
  });

  resume: File | null = null;

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      const allowedTypes = [
        'application/pdf',
        'text/plain',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      ];

      if (allowedTypes.includes(file.type)) {
        this.resume = file;
      } else {
        alert('Only PDF, TXT, DOC, and DOCX files are allowed.');
        this.resume = null; // Clear resume on invalid file
        input.value = ''; // Reset the input
      }
    }
  }

  submit(): void {
    if (this.form.valid && this.resume) {
      this.dialogRef.close({ form: this.form.value, resume: this.resume });
    }
  }

  close(): void {
    this.resume = null; // Clear resume on close
    this.dialogRef.close();
  }
}
