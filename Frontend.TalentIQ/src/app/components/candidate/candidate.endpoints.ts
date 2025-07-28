export const CANDIDATE_ENDPOINTS: {
  getAll: string;
  add: string;
  byId: (id: number) => string;
  update: (id: number) => string;
  delete: (id: number) => string;
} = {
  getAll: '/api/candidate/getCandidateList',
  add: '/api/candidate/addCandidate',
  byId: (id: number) => `/api/candidate/${id}`,
  update: (id: number) => `/api/candidate/updateCandidate/${id}`,
  delete: (id: number) => `/api/candidate/deleteCandidate/${id}`,
};
