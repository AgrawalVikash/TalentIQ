export interface Candidate {
  id: number;
  name: string;
  email: string;
  phone: string;
  jobId: string;
  resumePath: string;
  status: string;
  createdAt: string;
  interviewLink?: string;
  interviewLinkExpiry?: string;
}