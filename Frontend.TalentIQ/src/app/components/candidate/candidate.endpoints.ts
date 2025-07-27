export const CANDIDATE_ENDPOINTS = {
  getAll: '/api/candidate/getCandidateList',
  add: '/api/candidate/addCandidate',
  byId: (id: number) => `/api/candidates/${id}`,
};