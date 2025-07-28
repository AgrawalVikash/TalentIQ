import { take } from 'rxjs';

import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTableModule } from '@angular/material/table';
import { MatToolbarModule } from '@angular/material/toolbar';

import { Candidate } from '../../../models/candidate.model';
import { AddCandidateDialogComponent } from '../add-candidate-dialog/add-candidate-dialog.component';
import { CandidateService } from '../candidate.service';

@Component({
  selector: 'app-candidate-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatTableModule,
    MatDialogModule,
  ],
  templateUrl: './candidate-dashboard.component.html',
  styleUrls: ['./candidate-dashboard.component.scss'],
})
export class CandidateDashboardComponent implements OnInit {
  private candidateService = inject(CandidateService);
  private readonly dialog = inject(MatDialog);
  private readonly snackBar = inject(MatSnackBar);

  candidates = signal<Candidate[]>([]);
  displayedColumns = [
    'name',
    'email',
    'phone',
    'jobId',
    'status',
    'createdAt',
    'interview',
    'actions',
  ];
  loading = false;

  ngOnInit(): void {
    this.loadCandidates();
  }

  loadCandidates(): void {
    this.loading = true;
    this.candidateService
      .getCandidates()
      .pipe(take(1))
      .subscribe({
        next: (data) => {
          this.candidates.set(data);
          this.loading = false;
        },
        error: () => {
          this.snackBar.open('Failed to load candidates.', 'Close', {
            duration: 3000,
          });
          this.loading = false;
        },
      });
  }

  openAddDialog(): void {
    this.dialog
      .open(AddCandidateDialogComponent, {
        width: '45vw',
        maxWidth: '90vw',
      })
      .afterClosed()
      .pipe(take(1))
      .subscribe((res) => {
        if (res) {
          this.loading = true;
          this.candidateService
            .addCandidate(res.form, res.resume)
            .pipe(take(1))
            .subscribe({
              next: () => {
                this.snackBar.open('Candidate added successfully!', 'Close', {
                  duration: 3000,
                });
                this.loadCandidates();
              },
              error: () => {
                this.snackBar.open('Failed to add candidate.', 'Close', {
                  duration: 3000,
                });
                this.loading = false;
              },
            });
        }
      });
  }

  getResumeUrl(path: string): string {
    return `https://localhost:5001${path}`;
  }

  generateLink(candidate: Candidate): void {
    this.loading = true;
    this.candidateService
      .generateInterviewLink(candidate.id)
      .pipe(take(1))
      .subscribe({
        next: (linkData) => {
          this.candidates.update((list) =>
            list.map((c) =>
              c.id === candidate.id
                ? {
                    ...c,
                    interviewLink: linkData.interviewLink,
                    interviewLinkExpiry: linkData.interviewLinkExpiry,
                  }
                : c
            )
          );
          this.snackBar.open('Interview link generated!', 'Close', {
            duration: 3000,
          });
          this.loading = false;
        },
        error: () => {
          this.snackBar.open('Failed to generate interview link.', 'Close', {
            duration: 3000,
          });
          this.loading = false;
        },
      });
  }
}
