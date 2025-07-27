using Microsoft.AspNetCore.Http;
using TalentIQ.Common.Models;

namespace TalentIQ.Repository.Interface
{
    public interface ICandidateRepository
    {
        Task<List<Candidate>> GetCandidatesAsync();
        Task AddCandidateAsync(Candidate candidate);
        Task<string> SaveResumeAsync(IFormFile resume);
    }
}
