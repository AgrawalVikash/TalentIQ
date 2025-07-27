import { Observable } from 'rxjs';

import { HttpClient } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';

import { ENVIRONMENT_CONSTANTS } from '../../constants/environment.constants';
import { Candidate } from '../../models/candidate.model';
import { CANDIDATE_ENDPOINTS } from './candidate.endpoints';

@Injectable({ providedIn: 'root' })
export class CandidateService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = ENVIRONMENT_CONSTANTS.apiBaseUrl;

  // readonly candidates = signal<Candidate[]>([]);

  getCandidates(): Observable<Candidate[]> {
    return this.http.get<Candidate[]>(this.getUrl(CANDIDATE_ENDPOINTS.getAll));
  }

  addCandidate(data: Partial<Candidate>, resume: File): Observable<Candidate> {
    const formData = this.createFormData(data, resume);
    return this.http.post<Candidate>(this.getUrl(CANDIDATE_ENDPOINTS.add), formData);
  }

  generateInterviewLink(
    id: number
  ): Observable<{ interviewLink: string; interviewLinkExpiry: string }> {
    return this.http.post<{
      interviewLink: string;
      interviewLinkExpiry: string;
    }>(`${this.baseUrl}/${id}/generate-link`, {});
  }

  private createFormData(data: Record<string, any>, file: File): FormData {
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (value != null) formData.append(key, String(value));
    });
    formData.append('resume', file);
    return formData;
  }

  private getUrl(endpoint: string): string {
    return `${this.baseUrl}${endpoint}`;
  }
}
