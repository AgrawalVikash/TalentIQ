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
    'resume',
    'status',
    'createdAt',
    'interview',
    'actions',
  ];

  ngOnInit() {
    this.loadCandidates();
  }

  loadCandidates() {
    this.candidateService
      .getCandidates()
      .subscribe((data) => this.candidates.set(data));
  }

  openAddDialog() {
    this.dialog
      .open(AddCandidateDialogComponent, {
        width: '45vw',
        maxWidth: '90vw',
      })
      .afterClosed()
      .subscribe((res) => {
        if (res) {
          this.candidateService
            .addCandidate(res.form, res.resume)
            .subscribe((c) => {
              this.snackBar.open('Candidate added successfully!', 'Close', {
                duration: 3000,
              });
              this.loadCandidates();
            });
        }
      });
  }

  // generatLink(candidate: Candidate) {
  //   this.candidateService
  //     .generateInterviewLink(candidate.id)
  //     .subscribe((linkData) => {
  //       this.candidates.update((list) =>
  //         list.map((c) => (c.id === candidate.id ? { ...c, ...linkData } : c))
  //       );
  //     });
  // }

  getResumeUrl(path: string) {
    return `https://localhost:5001${path}`;
  }

  generateLink(candidate: Candidate) {
    this.candidateService
      .generateInterviewLink(candidate.id)
      .subscribe((linkData) => {
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
      });
  }
}
